from codec import Enumerated, Map, Record, Attribute, Choice
from codec import VString, VInteger
import cybox

"""
OpenC2 Command Definition

Classes that define the content of OpenC2 commands.  These classes are used with
an Encoder/Decoder (codec) to serialize and deserialize commands for transmission
in a format such as JSON, XML, or CBOR, or to generate format-specific message schemas.
"""

class TargetSpecifiers(Attribute):
    ns = 'openc2'
    vals = [
        ('cybox:Address', cybox.AddressObjectType, ''),
        ('cybox:Hostname', cybox.HostnameObjectType, ''),
        ('cybox:Network_Connection', cybox.NetworkConnectionObjectType, '')]

class Target(Record):
    ns = 'openc2'
    vals = [
        ('type', cybox.TargetTypeValue, ''),
        ('specifiers', TargetSpecifiers, '?,{type}')]

class NetworkActuatorObjectType(Record):
    ns = 'openc2'
    vals = [
        ('port', VString, '?'),
        ('asset_id', VString, '?')]

class ActuatorSpecifiers(Attribute):
    ns = 'openc2'
    vals = [
    ('network.firewall', NetworkActuatorObjectType, ''),
    ('network.router', NetworkActuatorObjectType, '')]

class ActuatorType(Enumerated):
    ns = 'openc2'
    vals = [
        'Network.Firewall', 'Network.Router'
    ]
class Actuator(Record):
    ns = 'openc2'
    vals = [
        ('type', ActuatorType, ''),
        ('specifiers', ActuatorSpecifiers, '?,{type}')]

class ResponseValue(Enumerated):
    ns = 'openc2'
    vals = ['ack', 'status']

class MethodValue(Enumerated):
    ns = 'openc2'
    vals = ['acl', 'blackhole', 'sinkhole', 'blacklist', 'whitelist']

class WhereValue(Enumerated):
    ns = 'openc2'
    vals = ['internal', 'perimeter']

class Modifiers(Map):
    ns = 'openc2'
    vals = [
        ('delay', VString, '?,<timeinterval>'),
        ('duration', VString, '?,<timeinterval>'),
        ('frequency', VString, '?,<timerecurrence>'),
        ('response', ResponseValue, '?'),
        ('time', VString, '?,<time>'),
        ('method', MethodValue, '?'),
        ('where', WhereValue, '?'),
        ('context_ref', VInteger, '?')]

class BaseCmd(Record):
    ns = 'openc2'
    vals = [
        ('target', Target, ''),
        ('actuator', Actuator, '?'),
        ('modifiers', Modifiers, '?')]

class OpenC2Command(Choice):
    ns = 'openc2'
    vals = [
        ('alert',       BaseCmd, ''),      #  1
        ('allow',       BaseCmd, ''),      #  2
        ('augment',     BaseCmd, ''),      #  3
        ('contain',     BaseCmd, ''),      #  4
        ('delay',       BaseCmd, ''),      #  5
        ('delete',      BaseCmd, ''),      #  6
        ('deny',        BaseCmd, ''),      #  7
        ('detonate',    BaseCmd, ''),      #  8
        ('distill',     BaseCmd, ''),      #  9
        ('get',         BaseCmd, ''),      # 10
        ('investigate', BaseCmd, ''),      # 11
        ('locate',      BaseCmd, ''),      # 12
        ('mitigate',    BaseCmd, ''),      # 13
        ('modify',      BaseCmd, ''),      # 14
        ('move',        BaseCmd, ''),      # 15
        ('notify',      BaseCmd, ''),      # 16
        ('pause',       BaseCmd, ''),      # 17
        ('query',       BaseCmd, ''),      # 18
        ('redirect',    BaseCmd, ''),      # 19
        ('remediate',   BaseCmd, ''),      # 20
        ('report',      BaseCmd, ''),      # 21
        ('response',    BaseCmd, ''),      # 22
        ('restart',     BaseCmd, ''),      # 23
        ('restore',     BaseCmd, ''),      # 24
        ('resume',      BaseCmd, ''),      # 25
        ('save',        BaseCmd, ''),      # 26
        ('scan',        BaseCmd, ''),      # 27
        ('set',         BaseCmd, ''),      # 28
        ('snapshot',    BaseCmd, ''),      # 29
        ('start',       BaseCmd, ''),      # 30
        ('stop',        BaseCmd, ''),      # 31
        ('substitute',  BaseCmd, ''),      # 32
        ('sync',        BaseCmd, ''),      # 33
        ('throttle',    BaseCmd, ''),      # 34
        ('update',      BaseCmd, '')]      # 35


# Test the OpenC2 classes using example serializations of the same content
if __name__ == '__main__':
    # JSON-concise and JSON-verbose test messages

    msg_jc1 = '["mitigate",["cybox:Hostname",["cdn.badco.org"]]]'

    msg_jv1 = '''
        {"mitigate": {
            "target": {"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}} '''

    msg_jc2 = '''
        ["deny", [
            ["cybox:Network_Connection",[null,"UDP",null,[["1.2.3.4"],"443"]]],
            ["openc2:network.router",["port","2"]],
            {"response":"ack","where":"perimeter"}]] '''

    msg_jv2 = '''
        {"deny": {
            "target":{"type":"cybox:Network_Connection","specifiers":{"Layer4Protocol":"UDP",
            "DestinationSocketAddress":{"IP_Address":{"Address_Value":"1.2.3.4"},"Port":"443"}}},
            "actuator":{"type":"openc2:network.router","specifiers":{"port":"2"}},
            "modifiers":{"response":"ack","where":"perimeter"}}} '''

    msg_jc3 = '''
        ["DENY", [
            ["cybox:Network_Connection",["IPv4","TCP",[["any"]],[["10.10.10.2"]]]],
            ["network.firewall",["30"]],
            {"context_ref": 91}]] '''

    msg_jv3 = '''
        {"DENY": {
             "TARGET": {"type": "cybox:Network_Connection",
                "specifiers": {
  		    		"Layer3Protocol": "IPv4",
  			    	"NetworkConnectionObj:Layer4Protocol": "TCP",
  				    "NetworkConnectionObj:SourceSocketAddress": {
  					    "SocketAddressObj:IP_Address": {
  						    "AddressObj:Address_Value": "any"}},
      				"NetworkConnectionObj:DestinationSocketAddress": {
  	    				"SocketAddressObj:IP_Address": {
  		    				"AddressObj:Address_Value": "10.10.10.2"}}}},
             "ACTUATOR": {"type": "network.firewall", "specifiers": {"asset_id": "30"}},
             "MODIFIERS": {"context_ref": 91}}} '''

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    oc2 = OpenC2Command()
    msg = msg_jv3
    print("   Raw Command:", msg)
    cmd = oc2.from_json(msg)
    print("Parsed Command:", cmd)

#    print("Command:", cmd.name, cmd.type, cmd.value)
    cmdname = next(iter(cmd))
    cmdv = cmd[cmdname]
    print("Command:", cmdname)
    t = cmdv['target']
    print("Target:", t['type'], t['specifiers'])
    if 'actuator' in cmdv:
        act = cmdv['actuator']['type']
        acs = cmdv['actuator']['specifiers']
    else:
        act = 'None'
        acs = ''
    print("Actuator:", act, acs)
    if 'modifiers' in cmdv:
        print("Modifiers:")
        for key, value in cmdv['modifiers'].items():
            print("    ", key + ": ", value)
    else:
        print("Modifiers: None")
