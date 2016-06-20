from codec import Enumerated, Map, Record, VBoolean, VInteger, VString

"""
Cyber Observables (cybox) definitions used by OpenC2
"""

class TargetTypeValue(Enumerated):
    ns = 'cybox'
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
    ns = 'cybox'
    vals = ['Certificate', 'RawCertificate', 'CertificateSignature']

class Layer3ProtocolType(Enumerated):      # Network_Connection_Object.xsd
    ns = 'cybox'
    vals = ['IPv4', 'IPv6', 'ICMP', 'IGMP', 'IGRP', 'CLNP',
            'EGP', 'EIGRP', 'IPSec', 'IPX', 'Routed-SMLT', 'SCCP']

class Layer4ProtocolType(Enumerated):       # Cybox_common.xsd
    ns = 'cybox'
    vals = ['TCP', 'UDP', 'AH', 'ESP', 'GRE', 'IL', 'SCTP', 'Sinec H1', 'SPX', 'DCCP']


class AddressObjectType(Record):
    ns = 'AddressObj'
    vals = [
        ('Address_Value', VString, '?'),
        ('VLAN_Name', VString, '?'),
        ('VLAN_Num', VInteger, '?')]

class HostnameObjectType(Record):      # Hostname_Object.xsd - string object.  FQDN?  IPAddr?
    ns = 'HostnameObj'
    vals = [
        ('Hostname_Value', VString, ''),    # Optional in cybox, required in OpenC2
        ('Naming_System', VString, '?')]

class PortObjectType(VString):          # TODO: fill this in
    ns = 'PortObj'
    vals = []

class SocketAddressObjectType(Record):
    ns = 'SocketAddressObj'
    vals = [
        ('IP_Address', AddressObjectType, '#1'),
        ('Hostname', HostnameObjectType, '#1'),
        ('Port', PortObjectType, '?')]

class NetworkConnectionObjectType(Record):      # Network_Connection_Object.xsd
    ns = 'NetworkConnectionObj'
    vals = [                                 # TODO: fill in all fields of xsd.
        ('Layer3Protocol', Layer3ProtocolType, '?'),
        ('Layer4Protocol', Layer4ProtocolType, '?'),
        ('SourceSocketAddress', SocketAddressObjectType, '?'),
        ('DestinationSocketAddress', SocketAddressObjectType, '?')]
