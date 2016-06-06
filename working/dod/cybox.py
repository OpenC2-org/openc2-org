from codec import Enumerated, VString

"""
Cyber Observables (cybox) definitions used by OpenC2
"""

class AddressObjectType(Enumerated):
    vals = [
        'Address_Value', 'VLAN_Name', 'VLAN_Num'
    ]
class NetworkConnectionObjectType(Enumerated):
    vals = [
        'Layer3Protocol', 'Layer4Protocol', 'SourceSocketAddress',
        'DestinationSocketAddress'
    ]

class X509CertificateObjectType(Enumerated):
    vals = [
        'Certificate', 'RawCertificate', 'CertificateSignature'
    ]

class Hostname_Value(VString):
    pass

class TargetTypeValue(Enumerated):
    vals = [
        'Address',              'Device',          'Disk',
        'Disk_Partition',       'Domain_Name',     'Email_Message',
        'File',                 'Hostname',        'Memory',
        'Network_Connection',   'Network_Flow',    'Network_Packet'
        'Network_Subnet',       'Port',            'Process',
        'Product',              'System',          'URI',
        'User_Account',         'User_Session'     'Volume',
        'Windows_Registry_Key', 'Windows_Service', 'X509_Certificate'
    ]
