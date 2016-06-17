from codec import Enumerated, Map, Record, Attribute
from codec import VString
import cybox

"""
OpenC2 Command Definition

Classes that define the content of OpenC2 commands.  These classes are used with
an Encoder/Decoder (codec) to serialize and deserialize commands for transmission
in a format such as JSON, XML, or CBOR, or to generate format-specific message schemas.

Applications get and set the values of a command using class attributes.
"""

class Action(Enumerated):
    vals = [
        'alert',    'allow',    'augment',     'contain',
        'delay',    'delete',   'deny',        'detonate',
        'distill',  'get',      'investigate', 'locate',
        'mitigate', 'modify',   'move',        'notify',
        'pause',    'query',    'redirect',    'remediate',
        'report',   'response', 'restart',     'restore',
        'resume',   'save',     'scan',        'set',
        'snapshot', 'start',    'stop',        'substitute',
        'sync',     'throttle', 'update',
    ]

class TargetSpecifiers(Attribute):
    vals = {
        'cybox:Hostname': (cybox.HostnameObjectType, '[1:]'),
        'cybox:Network_Connection': (cybox.NetworkConnectionObjectType, '')}

class Target(Record):
    vals = [
        ('type', cybox.TargetTypeValue, ''),
        ('specifiers', TargetSpecifiers, '?,{type}')]

class ActuatorSpecifiers(Attribute):
    vals = {
        'foo': (VString, ''),
        'bar': (VString, ''),
        'openc2:network.router': (VString, '')}

class Actuator(Record):
    vals = [
        ('type', VString, ''),
        ('specifiers', ActuatorSpecifiers, '?,{type}')]

class ResponseValue(Enumerated):
    vals = ['ack', 'status']

class MethodValue(Enumerated):
    vals = ['acl', 'blackhole', 'sinkhole', 'blacklist', 'whitelist']

class WhereValue(Enumerated):
    vals = ['internal', 'perimeter']

class Modifiers(Map):
    vals = [
        ('delay', VString, '?,<timeinterval>'),
        ('duration', VString, '?,<timeinterval>'),
        ('frequency', VString, '?,<timerecurrence>'),
        ('response', ResponseValue, '?'),
        ('time', VString, '?,<time>'),
        ('method', MethodValue, '?'),
        ('where', WhereValue, '?')]

class OpenC2Command(Record):
    vals = [
        ('action', Action, ''),
        ('target', Target, ''),
        ('actuator', Actuator, '?'),
        ('modifiers', Modifiers, '?')]


# Test the OpenC2 classes using example serializations of the same content
if __name__ == '__main__':
    # JSON-concise and JSON-verbose test messages
    #   TODO: Is cybox:Hostname_Value maxOccurs 1 or unbounded?  Not specified in Hostname_Object.xsd.

    msg_jc1 = '["mitigate",["cybox:Hostname",["cdn.badco.org"]]]'

    msg_jv1 = '''
        {"action":"mitigate","target":
        {"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}} '''

    msg_jc2 = '''
        ["deny",
        ["cybox:Network_Connection",[null,"UDP",null,[["1.2.3.4"],"443"]]],
        ["openc2:network.router","port:2"],
        {"response":"ack","where":"perimeter"}] '''

    msg_jv2 = '''
        {"action":"deny",
         "target":{"type":"cybox:Network_Connection","specifiers":{"Layer4Protocol":"UDP",
         "DestinationSocketAddress":{"IP_Address":{"Address_Value":"1.2.3.4"},"Port":"443"}}},
         "actuator":{"type":"openc2:network.router","specifiers":"port:2"},
         "modifiers":{"response":"ack","where":"perimeter"}} '''

    msg_jv3 = '''
        {"ACTION": "DENY",
         "TARGET": {"type": "cybox:Network_Connection",
            "specifiers": {
  				"NetworkConnectionObj:Layer3_Protocol": "IPv4",
  				"NetworkConnectionObj:Layer4_Protocol": "TCP",
  				"NetworkConnectionObj:Source_Socket_Address": {
  					"SocketAddressObj:IP_Address": {
  						"AddressObj:Address_Value": "any"}},
  				"NetworkConnectionObj:Destination_Socket_Address": {
  					"SocketAddressObj:IP_Address": {
  						"AddressObj:Address_Value": "10.10.10.2"}}}},
         "ACTUATOR": {"type": "network.firewall", "asset_id": "30"},
         "MODIFIERS": {"context_ref": 91}} '''

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    oc2 = OpenC2Command()
    msg = msg_jv3
    print("   Raw Command:", msg)
    cmd = oc2.from_json(msg)
    print("Parsed Command:", cmd)

    print("Action:", cmd['action'])
    t = cmd['target']
    print("Target:", t['type'], t['specifiers'])
    if 'actuator' in cmd:
        act = cmd['actuator']['type']
        acs = cmd['actuator']['specifiers']
    else:
        act = 'None'
        acs = ''
    print("Actuator:", act, acs)
    if 'modifiers' in cmd:
        print("Modifiers:")
        for key, value in cmd['modifiers'].items():
            print("    ", key + ": ", value)
    else:
        print("Modifiers: None")
