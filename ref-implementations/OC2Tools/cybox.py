"""
Cyber Observable Expression 2.1 definitions

Selected CybOX 2.1 objects used by OpenC2.  Abstract syntax information extracted from XSD source documents.
"""

__version__ = "0.1"
__meta__ = {
    "namespace": "http://cybox.mitre.org/objects",
    "sources": {"HostnameObject": "Hostname_Object.xsd",
                "NetworkConnectionObject": "Network_Connection_Object.xsd",
                "Layer3ProtocolType": "Network_Connection_Object.xsd",
                "Layer4ProtocolType": "Cybox_common.xsd"
                }
}

from codec import Attribute, Choice, Enumerated, Map, Record, Boolean, Integer, String

class Layer3ProtocolType(Enumerated):      # Network_Connection_Object.xsd
    ns = "cybox"
    vals = ["IPv4", "IPv6", "ICMP", "IGMP", "IGRP", "CLNP",
            "EGP", "EIGRP", "IPSec", "IPX", "Routed-SMLT", "SCCP"]

class Layer4ProtocolType(Enumerated):       # Cybox_common.xsd
    ns = "cybox"
    vals = ["TCP", "UDP", "AH", "ESP", "GRE", "IL", "SCTP", "Sinec H1", "SPX", "DCCP"]

class AddressObjectType(Record):
    ns = "AddressObj"
    vals = [
        ("Address_Value", String, "?"),
        ("VLAN_Name", String, "?"),
        ("VLAN_Num", Integer, "?")]

class DeviceObjectType(Map):
    ns = "DeviceObj"
    vals = [
        ("Description", String, "?"),
        ("Device_Type", String, "?"),
        ("Manufacturer", String, "?"),
        ("Model", String, "?"),
        ("Serial_Number", String, "?"),
        ("Firmware_Version", String, "?"),
        ("System_Details", String, "?")]

class DiskObjectType(Record):
    ns = "DiskObj"
    vals = []                          # TODO: fill in

class DiskPartitionObjectType(Record):
    ns = "DiskPartitionObj"
    vals = []                          # TODO: fill in

class DomainNameTypeEnum(Enumerated):
    ns = "DomainNameObj"
    vals = ["FQDN", "TLD"]

class DomainNameObjectType(Record):
    ns = "DomainNameObj"
    vals = [
        ("type", DomainNameTypeEnum, ""),
        ("Value", String, "")]

class EmailMessageObjectType(Record):
    ns = "EmailMessageObj"
    vals = []                          # TODO: fill in

class FileObjectType(Record):
    ns = "FileObj"
    vals = []                          # TODO: fill in

class HostnameObjectType(Record):      # Hostname_Object.xsd - unspecified string object - FQDN?
    ns = "HostnameObj"
    vals = [
        ("Hostname_Value", String, ""),    # Optional in cybox, required in OpenC2
        ("Naming_System", String, "?")]

class MemoryObjectType(Record):
    ns = "MemoryObj"
    vals = []                          # TODO: fill in

class NetworkFlowObjectType(Record):
    ns = "NetworkFlowObj"
    vals = []                          # TODO: fill in

class NetworkPacketObjectType(Record):
    ns = "NetworkPacketObj"
    vals = []                          # TODO: fill in

class NetworkSubnetObjectType(Record):
    ns = "NetworkSubnetObj"
    vals = []                          # TODO: fill in

class PortObjectType(Record):
    ns = "PortObj"
    vals = [
        ("Port_Value", Integer, "?,[1:]"),
        ("Layer4_Protocol", Layer4ProtocolType, "?")]

class ProcessObjectType(Record):
    ns = "ProcessObj"
    vals = []                          # TODO: fill in

class ProductObjectType(Record):
    ns = "ProductObj"
    vals = []                          # TODO: fill in

class SocketAddressChoice1(Choice):
    ns = "SocketAddressObj"
    vals = [
        ("IP_Address", AddressObjectType, ""),
        ("Hostname", HostnameObjectType, "")]

class SocketAddressObjectType(Record):
    ns = "SocketAddressObj"
    vals = [
        ("*", SocketAddressChoice1, ""),
        ("Port", PortObjectType, "?")]

class NetworkConnectionObjectType(Record):      # Network_Connection_Object.xsd
    ns = "NetworkConnectionObj"
    vals = [                                 # TODO: fill in all fields of xsd.
        ("Layer3Protocol", Layer3ProtocolType, "?"),
        ("Layer4Protocol", Layer4ProtocolType, "?"),
        ("SourceSocketAddress", SocketAddressObjectType, "?"),
        ("DestinationSocketAddress", SocketAddressObjectType, "?")]

class SystemObjectType(Record):
    ns = "SystemObj"
    vals = []                          # TODO: fill in

class URITypeEnum(Enumerated):
    ns = "cybox"
    vals = ["URL", "General URN", "Domain Name"]

class URIObjectType(Record):
    ns = "URIObj"
    vals = [
        ("type", URITypeEnum, ""),
        ("Value", String, "")]        # cyboxCommon:AnyURIObjectPropertyType

class UserAccountObjectType(Record):
    ns = "UserAccountObj"
    vals = []                          # TODO: fill in

class UserSessionObjectType(Record):
    ns = "UserSessionObj"
    vals = [
        ("Effective_Group", String, "?"),
        ("Effective_Group_ID", String, "?"),
        ("Effective_User", String, "?"),
        ("Effective_User_ID", String, "?"),
        ("Login_Time", String, "?"),       # cyboxCommon:DateTimeObjectPropertyType
        ("Logout_Time", String, "?")]      # cyboxCommon:DateTimeObjectPropertyType

class VolumeObjectType(Record):
    ns = "VolumeObj"
    vals = []                          # TODO: fill in

class WindowsRegistryKeyObjectType(Record):
    ns = "WindowsRegistryKeyObj"
    vals = []                          # TODO: fill in

class WindowsServiceObjectType(Record):
    ns = "WindowsServiceObj"
    vals = []                          # TODO: fill in

class X509CertificateObjectType(Enumerated):
    ns = "cybox"
    vals = ["Certificate", "RawCertificate", "CertificateSignature"]

class CyboxObject(Attribute):
    ns = "cybox"
    vals = [
        ("Address", AddressObjectType, ""),                         #  1
        ("Device", DeviceObjectType, ""),                           #  2
        ("Disk", DiskObjectType, ""),                               #  3
        ("Disk_Partition", DiskPartitionObjectType, ""),            #  4
        ("Domain_Name", DomainNameObjectType, ""),                  #  5
        ("Email_Message", EmailMessageObjectType, ""),              #  6
        ("File", FileObjectType, ""),                               #  7
        ("Hostname", HostnameObjectType, ""),                       #  8
        ("Memory", MemoryObjectType, ""),                           #  9
        ("Network_Connection", NetworkConnectionObjectType, ""),    # 10
        ("Network_Flow", NetworkFlowObjectType, ""),                # 11
        ("Network_Packet", NetworkPacketObjectType, ""),            # 12
        ("Network_Subnet", NetworkSubnetObjectType, ""),            # 13
        ("Port", PortObjectType, ""),                               # 14
        ("Process", ProcessObjectType, ""),                         # 15
        ("Product", ProductObjectType, ""),                         # 16
        ("Socket_Address", SocketAddressObjectType, ""),            # 17
        ("System", SystemObjectType, ""),                           # 18
        ("URI", URIObjectType, ""),                                 # 19
        ("User_Account", UserAccountObjectType, ""),                # 20
        ("User_Session", UserSessionObjectType, ""),                # 21
        ("Volume", VolumeObjectType, ""),                           # 22
        ("Windows_Registry_Key", WindowsRegistryKeyObjectType, ""), # 23
        ("Windows_Service", WindowsServiceObjectType, ""),          # 24
        ("X509_Certificate", X509CertificateObjectType, "")]        # 25