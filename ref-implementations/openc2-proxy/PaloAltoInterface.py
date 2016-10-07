# Copyright 2016 DoD - jmbrule@nsa.gov
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import xml.etree.ElementTree as ET
import time

'''
This file interfaces with the Palo Alto on the Shortstop network.  If a different Palo Alto instance is 
desired, the only thing that should be necessary is to update the APIKEY and HOSTNAME constants.

There are three public methonds:
    def addIPsToGroup(self, ipAddresses)
        IN: The ipAddresses must be a list of text IP addresses.  Examples are ['1.2.3.4'] and ['1.2.3.4','5.6.7.8']
        OUT: This will return three values:
            statusCode, statusName, statusDescription: These are the values from the ErrorCodes table constant
            that reflect the final commit response.  Intermediate responses are lost.
        DESCRIPTION: This adds the specified IPs to the hard coded group.  The group can be changed by changing
        the GROUP and NAME_PREFIX constants.  The GROUP is the Palo Alto Address Group that is created/updated.
        The NAME_PREFIX specifies the prefix for the named IP address.  The full name is created as
        <NAME_PREFIX>_<IP>.  These full names are added to the GROUP.
        THE USER MUST MANUALLY APPLY THE GROUP TO THE POLICY DESIRED! This will only add IPs to the group, it 
        will NOT assign the group to any specific policy.
        There are several timeouts in the process, currently hard coded to no more than 1 minute.  Therefore, 
        it may take many seconds, up to a few minutes, to complete.

    def removeIPsFromGroup(self, ipAddresses)
        IN: The ipAddresses must be a list of text IP addresses.  Examples are ['1.2.3.4'] and ['1.2.3.4', '5.6.7.8']
        OUT: This will return three values:
            statusCode, statusName, statusDescription: These are the values from the ErrorCodes table constant
            that reflect the final commit response.  Intermediate responses are lost.
        DESCRIPTION: This removes the specified IPs from the hard coded group.  The group can be changed by 
        changing the GROUP and NAME_PREFIX constants.  The GROUP is the Palo Alto Address Group that is
        created/updated.
        The NAME_PREFIX specifies the prefix for the named IP address.  The full name is created as
        <NAME_PREFIX>_<IP>.  These are the full names removed from the GROUP.
        THE USER MUST MANUALLY APPLY THE GROUP TO THE POLICY DESIRED! This will only remove IPs from the group, it 
        will NOT remove the group from any specific policy.
        There are several timeouts in the process, currently hard coded to no more than 1 minute.  Therefore, 
        it may take many seconds, up to a few minutes, to complete.

    def retrieveIPsinGroup(self)
        IN: Nothing
        OUT: This will return a list of text IPs in the hard coded group.
        Examples are: ['1.2.3.4'] and ['1.2.3.4','5.6.7.8']
        DESCRIPTION: This retrieves all the IP addresses in the hard coded group.  The group can be changed by 
        changing the GROUP constant.  The GROUP is the Palo Alto Address Group that is queried.
        
        
Example use is shown below.  This may be copied and pasted into a different script and executed.

from PaloAltoInterface import PaloAlto

PAinstance = PaloAlto()

# First get the current blocked list
blockedList = PAinstance.retrieveIPsinGroup()

print('Blocked list: {0}\n\n'.format(blockedList))

#Try to add a new address
statusCode, statusName, statusDescription = PAinstance.addIPsToGroup(['1.2.3.4','5.6.7.8','9.10.11.12'])
print('Result from BLOCK: {0} {1} {2}\n\n'.format(statusCode, statusName, statusDescription))

#Get the current blocked list
blockedList = PAinstance.retrieveIPsinGroup()

print('Blocked list: {0}\n\n'.format(blockedList))

#Remove some of the address just added
statusCode, statusName, statusDescription = PAinstance.removeIPsFromGroup(['9.10.11.12','1.2.3.4'])
print('Result from UNBLOCK: {0} {1} {2}\n\n'.format(statusCode, statusName, statusDescription))

#Get the current blocked list
blockedList = PAinstance.retrieveIPsinGroup()

print('Blocked list: {0}\n\n'.format(blockedList))

'''
class PaloAlto():

    ErrorCodes = {1:   ('Unknown command', 'The specific config or operational command is not recognized.'),
              2:   ('Internal errors', 'Check with technical support when seeing these errors.'),
              3:   ('Internal errors', 'Check with technical support when seeing these errors.'),
              4:   ('Internal errors', 'Check with technical support when seeing these errors.'),
              5:   ('Internal errors', 'Check with technical support when seeing these errors.'),
              6:   ('Bad Xpath', 'The xpath specified in one or more attributes of the command is invalid. Check the API browser for proper xpath values.'),
              7:   ('Object not present', 'Object specified by the xpath is not present. For example, entry[@name=.value.] where no object with name .value. is present.'),
              8:   ('Object not unique', 'For commands that operate on a single object, the specified object is not unique.'),
              9:   ('Internal error', 'Check with technical support when seeing these errors.'),
              10:  ('Reference count not zero', 'Object cannot be deleted as there are other objects that refer to it. For example, address object still in use in policy.'),
              11:  ('Internal error', 'Check with technical support when seeing these errors.'),
              12:  ('Invalid object', 'Xpath or element values provided are not complete.'),
              13:  ('Operation failed', 'A descriptive error message is returned in the response.'),
              14:  ('Operation not possible', 'Operation is not possible. For example, moving a rule up one position when it is already at the top.'),
              15:  ('Operation denied', 'For example, Admin not allowed to delete own account, Running a command that is not allowed on a passive device.'),
              16:  ('Unauthorized', 'The API role does not have access rights to run this query.'),
              17:  ('Invalid command', 'Invalid command or parameters.'),
              18:  ('Malformed command', 'The XML is malformed.'),
              19:  ('Success', 'Command completed successfully.'),
              20:  ('Success', 'Command completed successfully.'),
              21:  ('Internal error', 'Check with technical support when seeing these errors.'),
              22:  ('Session timed out', 'The session for this query timed out.'),
              }

    # The following API Key was generated by Mike Smith (msmith) on 8/29/2016 for the Palo Alto on the Shortstop network.
    APIKEY = 'LUFRPT1ueDFhVmh5aHgwdWUzem9ON21Ibzg4L1JhNzA9dEV5bjh0aDVGUmQ2cm5YdzF1Zks1WW1GRm5CUzQ3a3ZzWDJHWmcrRno2UT0='
    GROUP = 'OC2_BLOCKED'
    NAME_PREFIX = 'OC2'
    #HOSTNAME = 'pan'
    HOSTNAME = '192.168.0.33'
    VERIFYSSL = False
    MAXRESPONSETIME = 60  # Number of seconds to wait for the Palo Alto to respond before giving up.
    LOGLEVEL = 1

    URL = 'https://' + HOSTNAME + '/api/'
    
    if not VERIFYSSL:
        requests.packages.urllib3.disable_warnings()

    def __init__(self):
        self._log('\nEntered __init__')

        
    def addIPsToGroup(self, ipAddresses):
        self._log('addIPsToBlockList')
        # ipAddresses must be a list, even if only one address is provided.
        
        xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address-group/entry[@name='{group}']/static".format(group=self.GROUP)
        element = None
        
        allRawData = []
        
        for ipAddress in ipAddresses:
        
            # ADD THE IP ADDRESS WE WANT TO BLOCK
            xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address/entry[@name='{prefix}_{ip}']".format(prefix=self.NAME_PREFIX, ip=ipAddress)
            element = "<ip-netmask>{ip}</ip-netmask><description>Added from OC2 command</description>".format(ip=ipAddress)
            responseData, rawData = self._queryDevice(xPath, element, "set")
            
            # ADD THE GROUP WE WANT TO PUT THE ADDRESS IN
            xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address-group/entry[@name='{group}']".format(group=self.GROUP)
            element = "<static><member>{prefix}_{ip}</member></static>".format(ip=ipAddress, prefix=self.NAME_PREFIX)
            responseData, rawData = self._queryDevice(xPath, element, "set")

        # COMMIT THE CONFIGURATION
        statusCode, statusName, statusDescription = self._commitConfiguration()
        
        return statusCode, statusName, statusDescription        
        
    # End addIPsToBlockList 

    def removeIPsFromGroup(self, ipAddresses):
        self._log('removeIPsFromBlockList')
        # ipAddresses must be a list, even if only one address is provided.
        
        for ipAddress in ipAddresses:
        
            # DELETE THE IP ADDRESS WE WANT TO UNBLOCK
            xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address-group/entry[@name='{group}']/static/member[text()='{prefix}_{ip}']".format(ip=ipAddress,group=self.GROUP,prefix=self.NAME_PREFIX)
            element = None
            responseData, rawData = self._queryDevice(xPath, element, "delete")

            # REMOVE THE ADDRESS FROM THE GROUP
            xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address/entry[@name='{prefix}_{ip}']".format(ip=ipAddress,prefix=self.NAME_PREFIX)
            element = None
            responseData, rawData = self._queryDevice(xPath, element, "delete")
  
        # COMMIT THE CONFIGURATION
        statusCode, statusName, statusDescription = self._commitConfiguration()
        
        return statusCode, statusName, statusDescription

        
    def retrieveIPsinGroup(self):
        self._log('retrieveBlockedEntries')
        
        xPath = "/config/devices/entry/vsys/entry[@name='vsys1']/address-group/entry[@name='{group}']/static".format(group=self.GROUP)
        element = None
        
        responseData, rawData = self._queryDevice(xPath, element, "get")
        
        self._log('RESPONSE DATA = {0}'.format(responseData.text))
        if len(responseData) > 0:
            addressList = []
            entry = responseData.find(".//result/static")
                
            try:
                members = entry.findall("./member")
            except AttributeError:
                members = []

            for member in members:
                
                # Query for the IP Address
                xPath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/address/entry[@name='{addressName}']".format(addressName=member.text)
                element=None
                                
                responseData, rawData = self._queryDevice(xPath, element, "get")
                
                if len(responseData) > 0:
                    entry = responseData.find("./result/entry")
                    for element in entry.iter():
                        if element.tag == "ip-netmask":
                            addressList.append(element.text)
                                    
        return addressList        
        
    # End showBlockList 

    def _queryDevice(self, xPath, element, action):
        self._log('_queryDevice')
        params = ([("type", "config"),
                  ("key", self.APIKEY), 
                  ("action", action),
                  ("xpath", xPath),
                  ("element", element),
                  ])
                  
        response = requests.get(self.URL, params=params, verify=self.VERIFYSSL)
        rawData = response.text

        self._log(response.status_code)
        self._log(response.url)
        root = ET.fromstring(response.content)
        if response.status_code == requests.codes.ok:            
            self._log('response.text    = {0}'.format(response.text))
            self._log('response.content = {0}'.format(response.content))
            
        statusCode, statusName, statusDescription = self._isError(root)
        
        return root, rawData
    #end _queryDevice
    
    
    def _commitConfiguration(self):
        self._log('_commitConfiguration')
        statusCode = 0
        statusName = 'No Result'
        statusDescription = 'Command not executed by target device'
        commitTryCount = 60
        commitRoot = None

        params = {"type": "commit",
                  "key":  self.APIKEY,
                  "cmd": "<commit></commit>"
                  }
                  
        while commitTryCount > 0:
            response = requests.get(self.URL, params=params, verify=self.VERIFYSSL)
                      
            commitRaw = response.text

            if response.status_code == requests.codes.ok:            
                commitRoot = ET.fromstring(response.content)
                
            statusCode, statusName, statusDescription = self._isError(commitRoot)
            if commitRaw.find('Please try again later') < 0:
                commitTryCount = 0
            else:
                time.sleep(1)
                commitTryCount -= 1
                
        return statusCode, statusName, statusDescription
    #end _commitConfiguration

   
    def _isError(self, xmlRoot):
        self._log('_isError')
        statusName = 'No Result'
        statusDescription = 'Command not executed by target device'
        foundError = False
        status = xmlRoot.get("status", None)
        statusCode = int(xmlRoot.get("code", "0"))
        statusName = self.ErrorCodes[statusCode][0]
        statusDescription = self.ErrorCodes[statusCode][1]
        
        self._log('Got Status {0}   Error Code {1} Name {2}  Description {3}'.format(status, statusCode, statusName, statusDescription))

        # Determine if the job is queued.
        jobId = xmlRoot.findtext(".//job")
        if jobId:
            
            success = self._jobQueued(jobId, self.MAXRESPONSETIME)
            if not success:
                statusCode = 13
                statusName = self.ErrorCodes[statusCode][0]
                statusDescription = self.ErrorCodes[statusCode][1]
        else: 
            foundError = True

        # look for error message in msg or msg/line
        lines = xmlRoot.findall(".//msg/line")
        msg = "\n".join([line.text for line in lines])

        if msg:
            self._log(msg)

        lines = xmlRoot.findall(".//msg")
        if lines:
            msg = "\n".join([line.text for line in lines if line.text])
            if msg:
                self._log(msg)

        # Determine if the last request has been queued
        jobId = xmlRoot.findtext(".//job")
        if jobId:
            
            success = self._jobQueued(jobId, self.MAXRESPONSETIME)
            if not success:
                statusCode = 13
                statusName = self.ErrorCodes[statusCode][0]
                statusDescription = self.ErrorCodes[statusCode][1]
                
        return statusCode, statusName, statusDescription

    #end _isError

    def _jobQueued(self, jobId, timeRemaining):
        self._log('_jobQueued: {0}'.format(jobId))
        status = True
        if timeRemaining > 0:
            timeRemaining -= 1
            time.sleep(1)
            
            params = {'type': 'op',
                      "key":  self.APIKEY,
                      'cmd': '<show><jobs><id>{job}</id></jobs></show>'.format(job=jobId)
                      }
                      
            response = requests.get(self.URL, params=params, verify=self.VERIFYSSL)
                      
            responseRaw = response.text
            self._log(responseRaw)

            if response.status_code == requests.codes.ok:            
                responseRoot = ET.fromstring(response.content)
      
            #Determine if the job is done by looking at the end time.  If "0", then it is not done.
            stillActive = responseRaw.find('Still Active')
            self._log('Status from query for job to finish: {0}'.format(stillActive))
            if stillActive > 0:
                status = self._jobQueued(jobId, timeRemaining)
            else:
                ok = responseRaw.find('<result>OK')
                self._log('Quesed job done, OK found at {0}'.format(ok))
                if ok < 0:
                    status = False
                    
        return status
                
    def _log(self, message):
        if self.LOGLEVEL > 0:
            print(message)
            
    #end _jobQueued
