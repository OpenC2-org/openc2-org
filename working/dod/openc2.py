from codec import Enumerated, Map, Record, Attribute, Choice
from codec import String, Integer
import cybox

"""
OpenC2 Command Definitions

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

class TargetType(Enumerated):
    ns = "cybox"        # Default ns - most types are from CybOX 2
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

class ActuatorType(Enumerated):
    ns = "openc2"       # Temporary types until an authoritative vocabulary is identified
    vals = [
        "endpoint",                     #  1
        "endpoint-digital-telephone-handset",   #  2
        "endpoint-laptop",              #  3
        "endpoint-pos-terminal",        #  4
        "endpoint-printer",             #  5
        "endpoint-sensor",              #  6
        "endpoint-server",              #  7
        "endpoint-smart-meter",         #  8
        "endpoint-smart-phone",         #  9
        "endpoint-tablet",              # 10
        "endpoint-workstation",         # 11
        "network",                      # 12
        "network-bridge",               # 13
        "network-firewall",             # 14
        "network-gateway",              # 15
        "network-guard",                # 16
        "network-hips",                 # 17
        "network-hub",                  # 18
        "network-ids",                  # 19
        "network-ips",                  # 20
        "network-modem",                # 21
        "network-nic",                  # 22
        "network-proxy",                # 23
        "network-router",               # 24
        "network-security-manager",     # 25
        "network-sense-making",         # 26
        "network-sensor",               # 27
        "network-switch",               # 28
        "network-vpn",                  # 29
        "network-wap",                  # 30
        "process",                      # 31
        "process-aaa-server",           # 32
        "process-anti-virus-scanner",   # 33
        "process-connection-scanner",   # 34
        "process-directory-server",     # 35
        "process-dns-server",           # 36
        "process-email-service",        # 37
        "process-file-scanner",         # 38
        "process-location-service",     # 39
        "process-network-scanner",      # 40
        "process-remediation-service",  # 41
        "process-reputation-service",   # 42
        "process-sandbox",              # 43
        "process-virtualization-service",   # 44
        "process-vulnerability-scanner",    # 45
    ]

class Target(Record):
    ns = "openc2"
    vals = [
        ("type", TargetType, ""),
        ("specifiers", cybox.CyboxObject, "?,{type}")]

class ActuatorSpecifiers(Record):
    ns = "openc2"
    vals = [
        ("port", String, "?"),
        ("asset_id", String, "?")]

class ActuatorObject(Attribute):            # TODO: define datatypes for each actuator
    ns = "openc2"
    vals = [
        ("endpoint", ActuatorSpecifiers, ""),
        ("endpoint-digital-telephone-handset", ActuatorSpecifiers, ""),
        ("endpoint-laptop", ActuatorSpecifiers, ""),
        ("endpoint-pos-terminal", ActuatorSpecifiers, ""),
        ("endpoint-printer", ActuatorSpecifiers, ""),
        ("endpoint-sensor", ActuatorSpecifiers, ""),
        ("endpoint-server", ActuatorSpecifiers, ""),
        ("endpoint-smart-meter", ActuatorSpecifiers, ""),
        ("endpoint-smart-phone", ActuatorSpecifiers, ""),
        ("endpoint-tablet", ActuatorSpecifiers, ""),
        ("endpoint-workstation", ActuatorSpecifiers, ""),
        ("network", ActuatorSpecifiers, ""),
        ("network-bridge", ActuatorSpecifiers, ""),
        ("network-firewall", ActuatorSpecifiers, ""),
        ("network-gateway", ActuatorSpecifiers, ""),
        ("network-guard", ActuatorSpecifiers, ""),
        ("network-hips", ActuatorSpecifiers, ""),
        ("network-hub", ActuatorSpecifiers, ""),
        ("network-ids", ActuatorSpecifiers, ""),
        ("network-ips", ActuatorSpecifiers, ""),
        ("network-modem", ActuatorSpecifiers, ""),
        ("network-nic", ActuatorSpecifiers, ""),
        ("network-proxy", ActuatorSpecifiers, ""),
        ("network-router", ActuatorSpecifiers, ""),
        ("network-security-manager", ActuatorSpecifiers, ""),
        ("network-sense-making", ActuatorSpecifiers, ""),
        ("network-sensor", ActuatorSpecifiers, ""),
        ("network-switch", ActuatorSpecifiers, ""),
        ("network-vpn", ActuatorSpecifiers, ""),
        ("network-wap", ActuatorSpecifiers, ""),
        ("process", ActuatorSpecifiers, ""),
        ("process-aaa-server", ActuatorSpecifiers, ""),
        ("process-anti-virus-scanner", ActuatorSpecifiers, ""),
        ("process-connection-scanner", ActuatorSpecifiers, ""),
        ("process-directory-server", ActuatorSpecifiers, ""),
        ("process-dns-server", ActuatorSpecifiers, ""),
        ("process-email-service", ActuatorSpecifiers, ""),
        ("process-file-scanner", ActuatorSpecifiers, ""),
        ("process-location-service", ActuatorSpecifiers, ""),
        ("process-network-scanner", ActuatorSpecifiers, ""),
        ("process-remediation-service", ActuatorSpecifiers, ""),
        ("process-reputation-service", ActuatorSpecifiers, ""),
        ("process-sandbox", ActuatorSpecifiers, ""),
        ("process-virtualization-service", ActuatorSpecifiers, ""),
        ("process-vulnerability-scanner", ActuatorSpecifiers, "")
    ]

class Actuator(Record):
    ns = "openc2"
    vals = [
        ("type", ActuatorType, ""),
        ("specifiers", ActuatorObject, "?,{type}")]

class ResponseValue(Enumerated):
    ns = "openc2"
    vals = ["ack", "status"]

class MethodValue(Enumerated):
    ns = "openc2"
    vals = ["acl", "blackhole", "sinkhole", "blacklist", "whitelist"]

class WhereValue(Enumerated):
    ns = "openc2"
    vals = ["internal", "perimeter"]

class Duration(String):
    pattern = "^\d+$"

class DateTime(String):
    pattern = "^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{1,6})?Z|[-+]\d\d:\d\d$"

class Modifiers(Map):
    ns = "openc2"
    vals = [
        ("delay", Duration, "?"),
        ("duration", Duration, "?"),
        ("frequency", Duration, "?"),
        ("response", ResponseValue, "?"),
        ("time", DateTime, "?"),
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
