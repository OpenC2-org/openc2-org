from codec import Enumerated, Map, Record
from codec import VString, VTime, VTimeInterval, VTimeRecurrence

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

class Target(Record):
    vals = [
        ('type', VString, ''),
        ('specifiers', VString, '?')]

class Actuator(Record):
    vals = [
        ('type', VString, ''),
        ('specifiers', VString, '?')]

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
    # JSON-verbose message
    msg_jv1 = '{"action":"mitigate",'\
        '"target":{"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}'

    msg_jv2 = '{"action":"deny",'\
        '"target":{"type":"cybox:Network_Connection","specifiers":{"foo":"1.2.3.4"}},'\
        '"actuator":{"type":"openc2:network.router","specifiers":{"foo":"port:2"}},'\
        '"modifiers":{"response":"ack","where":"perimeter"}}'

    # JSON-concise message
    msg_jc1 = '["mitigate",["cybox:Hostname",{"Hostname_Value":"cdn.badco.org"}]]'

    msg_jc2 = '["deny",'\
        '["cybox:Network_Connection",{"foo":"1.2.3.4"}],'\
        '["openc2:network.router",{"foo":"port:2"}],'\
        '{"response":"ack","where":"perimeter"}]'

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    cmd = OpenC2Command()
    cmd.from_json(msg_jc2)
    print("Action:", cmd.action)
    print("Target:", cmd.target.type, cmd.target.specifiers)
    print("Actuator:", cmd.actuator.type, cmd.actuator.specifiers)
    print("Modifiers:")
    for key, value in cmd.modifiers:
        print("    ", key + ": ", value)
