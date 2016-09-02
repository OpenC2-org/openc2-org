from codec import Enumerated, Map, Record, Attribute, Choice
from codec import String, Integer
import cybox

"""
OpenC2 Command Definition

Classes that define the content of OpenC2 commands.  These classes are used with
an Encoder/Decoder (codec) to serialize and deserialize commands for transmission
in a format such as JSON, XML, or CBOR, or to generate format-specific message schemas.
"""

class Action(Enumerated):
    ns = "openc2"
    vals = [
        "scan",        #  1
        "locate",      #  2
        "query",       #  3
        "report",      #  4
        "get",         #  5
        "notify",      #  6
        "deny",        #  7
        "contain",     #  8
        "allow",       #  9
        "start",       # 10
        "stop",        # 11
        "restart",     # 12
        "pause",       # 13
        "resume",      # 14
        "cancel",      # 15
        "set",         # 16
        "update",      # 17
        "move",        # 18
        "redirect",    # 19
        "delete",      # 20
        "snapshot",    # 21
        "detonate",    # 22
        "restore",     # 23
        "save",        # 24
        "modify",      # 25
        "throttle",    # 26
        "delay",       # 27
        "substitute",  # 28
        "copy",        # 29
        "sync",        # 30
        "distill",     # 31
        "augment",     # 32
        "investigate", # 33
        "mitigate",    # 34
        "remediate",   # 35
        "response",    # 36
        "alert"        # 37
    ]

class TargetTypeValue(Enumerated):
    ns = "cybox"                    # Default ns - most types are from CybOX 2
    vals = [
        "Address",          #  1
        "Device",           #  2
        "Disk",             #  3
        "Disk_Partition"    #  4
        "Domain_Name",      #  5
        "Email_Message",    #  6
        "File",             #  7
        "Hostname",         #  8
        "Memory",           #  9
        "Network_Connection",   # 10
        "Network_Flow",     # 11
        "Network_Packet",   # 12
        "Network_Subnet",   # 13
        "Port",             # 14
        "Process",          # 15
        "Product",          # 16
        "Socket_Address",   # 17
        "System",           # 18
        "URI",              # 19
        "User_Account",     # 20
        "User_Session",     # 21
        "Volume",           # 22
        "Windows_Registry_Key", # 23
        "Windows_Service",  # 24
        "X509_Certificate", # 25
        "OpenC2:Data"       #  1
    ]

class Target(Record):
    ns = "openc2"
    vals = [
        ("type", TargetTypeValue, ""),              # TODO: import from cybox choice types?
        ("specifiers", cybox.CyboxObject, "?,{type}")]

class NetworkActuatorObjectType(Record):
    ns = "openc2"
    vals = [
        ("port", String, "?"),
        ("asset_id", String, "?")]

class ActuatorSpecifiers(Attribute):
    ns = "openc2"
    vals = [
    ("network.firewall", NetworkActuatorObjectType, ""),
    ("network.router", NetworkActuatorObjectType, "")]

class ActuatorType(Enumerated):
    ns = "openc2"
    vals = [
        "Network.Firewall", "Network.Router"
    ]
class Actuator(Record):
    ns = "openc2"
    vals = [
        ("type", ActuatorType, ""),
        ("specifiers", ActuatorSpecifiers, "?,{type}")]

class ResponseValue(Enumerated):
    ns = "openc2"
    vals = ["ack", "status"]

class MethodValue(Enumerated):
    ns = "openc2"
    vals = ["acl", "blackhole", "sinkhole", "blacklist", "whitelist"]

class WhereValue(Enumerated):
    ns = "openc2"
    vals = ["internal", "perimeter"]

class Modifiers(Map):
    ns = "openc2"
    vals = [
        ("delay", String, "?,<timeinterval>"),
        ("duration", String, "?,<timeinterval>"),
        ("frequency", String, "?,<timerecurrence>"),
        ("response", ResponseValue, "?"),
        ("time", String, "?,<time>"),
        ("method", MethodValue, "?"),
        ("where", WhereValue, "?"),
        ("context_ref", Integer, "?")]

class OpenC2Command(Record):
    ns = "openc2"
    vals = [
        ("action", Action, ""),
        ("target", Target, ""),
        ("actuator", Actuator, "?"),
        ("modifiers", Modifiers, "?")]
