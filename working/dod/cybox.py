from codec import Enumerated, Record, Choice, VBoolean, VInteger, VString

"""
Cyber Observable Expression (cybox) definitions used by OpenC2
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

class HostnameObjectType(Record):      # Hostname_Object.xsd - unspecified string object - FQDN?
    ns = 'HostnameObj'
    vals = [
        ('Hostname_Value', VString, ''),    # Optional in cybox, required in OpenC2
        ('Naming_System', VString, '?')]

class PortObjectType(Record):
    ns = 'PortObj'
    vals = [
        ('Port_Value', VInteger, '?[1:]'),
        ('Layer4_Protocol', Layer4ProtocolType, '?')]

class SocketAddressChoice1(Choice):
    ns = 'SocketAddressObj'
    vals = [
        ('IP_Address', AddressObjectType, ''),
        ('Hostname', HostnameObjectType, '')]

class SocketAddressObjectType(Record):
    ns = 'SocketAddressObj'
    vals = [
        ('*', SocketAddressChoice1, '#'),
        ('Port', PortObjectType, '?')]

class NetworkConnectionObjectType(Record):      # Network_Connection_Object.xsd
    ns = 'NetworkConnectionObj'
    vals = [                                 # TODO: fill in all fields of xsd.
        ('Layer3Protocol', Layer3ProtocolType, '?'),
        ('Layer4Protocol', Layer4ProtocolType, '?'),
        ('SourceSocketAddress', SocketAddressObjectType, '?'),
        ('DestinationSocketAddress', SocketAddressObjectType, '?')]
