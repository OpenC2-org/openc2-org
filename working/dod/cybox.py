from codec import Enumerated

"""
Cyber Observables (cybox) definitions used by OpenC2
"""

class NsEnumerated(Enumerated):
    namespace = 'cybox'

class AddressObjectType(NsEnumerated):
    vals = [
        'Address_Value', 'VLAN_Name', 'VLAN_Num'
    ]
class NetworkConnectionObjectType(Enumerated):
    namespace = 'cybox'
    vals = [
        'Layer3Protocol', 'Layer4Protocol', 'SourceSocketAddress',
        'DestinationSocketAddress'
    ]

class X509CertificateObjectType(Enumerated):
    namespace = 'cybox'
    vals = [
        'Certificate', 'RawCertificate', 'CertificateSignature'
    ]

class TargetTypeValue(Enumerated):
    namespace = 'cybox'
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
