from codec import Enumerated, Map, Record, VBoolean, VInteger, VString

"""
Cyber Observables (cybox) definitions used by OpenC2
"""

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

class X509CertificateObjectType(Enumerated):
    vals = ['Certificate', 'RawCertificate', 'CertificateSignature']

class Layer3ProtocolType(Enumerated):      # Network_Connection_Object.xsd
    vals = ['IPv4', 'IPv6', 'ICMP', 'IGMP', 'IGRP', 'CLNP',
            'EGP', 'EIGRP', 'IPSec', 'IPX', 'Routed-SMLT', 'SCCP']

class Layer4ProtocolType(Enumerated):       # Cybox_common.xsd
    vals = ['TCP', 'UDP', 'AH', 'ESP', 'GRE', 'IL', 'SCTP', 'Sinec H1', 'SPX', 'DCCP']


class AddressObjectType(Record):
    vals = [
        ('Address_Value', VString, '?'),
        ('VLAN_Name', VString, '?'),
        ('VLAN_Num', VInteger, '?')]

class HostnameObjectType(Record):      # Hostname_Object.xsd - string object.  FQDN?  IPAddr?
    vals = [
        ('Hostname_Value', VString, ''),    # Optional in cybox, required in OpenC2
        ('Naming_System', VString, '?')]

class PortObjectType(VString):          # TODO: fill this in
    pass

class SocketAddressObjectType(Record):
    vals = [
        ('IP_Address', AddressObjectType, '#1'),
        ('Hostname', HostnameObjectType, '#1'),
        ('Port', PortObjectType, '?')]

class NetworkConnectionObjectType(Record):      # Network_Connection_Object.xsd
    vals = [                                 # TODO: fill in all fields of xsd.
        ('Layer3Protocol', Layer3ProtocolType, '?'),
        ('Layer4Protocol', Layer4ProtocolType, '?'),
        ('SourceSocketAddress', SocketAddressObjectType, '?'),
        ('DestinationSocketAddress', SocketAddressObjectType, '?')]
