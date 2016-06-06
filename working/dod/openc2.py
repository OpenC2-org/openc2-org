from codec import Enumerated, Map, Record, Choice
from codec import VString, VTime, VTimeInterval, VTimeRecurrence
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

class TargetSpecifiers(Choice):
    vals = {
        'cybox:Hostname': (cybox.Hostname_Value, '[1:]'),
        'cybox:Network_Connection': (VString, ''),
    }

class Target(Record):
    vals = [
        ('type', cybox.TargetTypeValue, ''),
        ('specifiers', TargetSpecifiers, '?,{type}')]

class ActuatorSpecifiers(Map):
    pass

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
        ('delay', VTimeInterval, '?'),
        ('duration', VTimeInterval, '?'),
        ('frequency', VTimeRecurrence, '?'),
        ('response', ResponseValue, '?'),
        ('time', VTime, '?'),
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
    msg_jc1a = '["mitigate",["cybox:Hostname",["cdn.badco.org","xyz.foo.com"]]]'
    msg_jc1 = '["mitigate",["cybox:Hostname","cdn.badco.org"]]'

    msg_jv1a = '{"action":"mitigate","target":'\
        '{"type":"cybox:Hostname","specifiers":["cdn.badco.org","xyz.foo.com"]}}'
    msg_jv1 = '{"action":"mitigate","target":'\
        '{"type":"cybox:Hostname","specifiers":"cdn.badco.org"}}'

    msg_jc2 = '["deny",'\
        '["cybox:Network_Connection",{"foo":"1.2.3.4"}],'\
        '["openc2:network.router",{"bar":"port:2"}],'\
        '{"response":"ack","where":"perimeter"}]'

    msg_jv2 = '{"action":"deny",'\
        '"target":{"type":"cybox:Network_Connection","specifiers":{"foo":"1.2.3.4"}},'\
        '"actuator":{"type":"openc2:network.router","specifiers":{"foo":"port:2"}},'\
        '"modifiers":{"response":"ack","where":"perimeter"}}'

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    cmd = OpenC2Command()
    cmd.from_json(msg_jv1)
    cmd.printattrs()

    print("Action:", cmd.action)
    print("Target:", cmd.target.type, cmd.target.specifiers.value)  # TODO: change to cmd.target.value
    if cmd.actuator:
        print("Actuator:", cmd.actuator.type, cmd.actuator.specifiers)
    else:
        print("Actuator: None")
    if cmd.modifiers:
        print("Modifiers:")
        for key, value in cmd.modifiers:
            print("    ", key + ": ", value)
    else:
        print("Modifiers: None")
