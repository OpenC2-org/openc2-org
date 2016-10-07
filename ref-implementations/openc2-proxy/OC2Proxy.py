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

from PaloAltoInterface import PaloAlto
import json

class OpenC2Proxy():
    def commandReceived(self, object):
        
        PAinstance = PaloAlto()
        
        action = object.ACTION
        target = json.loads(object.TARGET.replace("u'","\"").replace("'","\""))
        actuator = json.loads(object.ACTUATOR.replace("u'","\"").replace("'","\""))
        modifiers = json.loads(object.MODIFIERS.replace("u'","\"").replace("'","\""))
        
        if action == "DENY":
            IPAddress = target['specifiers']['DestinationSocketAddress']['IP_Address']['Address_Value']
            statusCode, statusName, statusDescription = PAinstance.addIPsToGroup([IPAddress])
        elif action == "ALLOW":
            IPAddress = target['specifiers']['DestinationSocketAddress']['IP_Address']['Address_Value']
            statusCode, statusName, statusDescription = PAinstance.removeIPsFromGroup([IPAddress])
        
