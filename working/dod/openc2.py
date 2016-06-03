from codec import Enumerated, Map, Record
from codec import VString, VTime, VTimeInterval, VTimeRecurrence
from cybox import TargetTypeValue

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
    vals = [('type', '', TargetTypeValue),
            ('specifiers', '?', VString)]

class ActuatorTypeValue(Enumerated):
    namespace = 'openc2'
    vals = [
        'endpoint', 'endpoint.digital-telephone-handset', 'endpoint.laptop',
        'endpoint.pos-terminal', 'endpoint.printer', 'endpoint.sensor'
        'endpoint.server', 'endpoint.smart-meter', 'endpoint.smart-phone',
        'endpoint.tablet', 'endpoint.workstation',
        'network', 'network.bridge', 'network.firewall', 'network.gateway',
        'network.guard', 'network.hips', 'network.hub', 'network.ids',
        'network.ips', 'network.modem', 'network.nic', 'network.proxy',
        'network.router', 'network.security_manager', 'network.sense_making',
        'network.sensor', 'network.switch', 'network.vpn', 'network.wap',
        'process', 'process.aaa-server', 'process.anti-virus-scanner',
        'process.connection-scanner', 'process.directory-service', 'process.dns-server',
        'process.email-service', 'process.file-scanner', 'process.location-service',
        'process.network-scanner', 'process.remediation-service', 'process.sandbox',
        'process.virtualization-service', 'process.vulnerability-scanner'
    ]

class Actuator(Record):
    vals = [('type', '', ActuatorTypeValue),
            ('specifiers', '?', VString)]

class ResponseValue(Enumerated):
    vals = ['ack', 'status']

class MethodValue(Enumerated):
    vals = ['acl', 'blackhole', 'sinkhole', 'blacklist', 'whitelist']

class WhereValue(Enumerated):
    vals = ['internal', 'perimeter']

class Modifiers(Map):
    vals = [
        ('delay',     '?', VTimeInterval),
        ('duration',  '?', VTimeInterval),
        ('frequency', '?', VTimeRecurrence),
        ('response',  '?', ResponseValue),
        ('time',      '?', VTime),
        ('method',    '?', MethodValue),
        ('where',     '?', WhereValue)
    ]

class OpenC2Command(Record):
    vals = [('action', '', Action),
            ('target', '', Target),
            ('actuator', '?', Actuator),
            ('modifiers', '?', Modifiers)]


# Test the OpenC2 classes using example serializations of the same content
if __name__ == '__main__':
    # JSON-verbose message
    msg_jv1 = '{"action":"deny",' \
            '"target":{"type":"cybox:Network_Connection","specifiers":{"foo":"1.2.3.4"},' \
            '"actuator":{"type":"openc2:network.router","specifiers":{}},' \
            '{"response":"ack","where":"perimeter"}}'

    msg_jv2 = '{"action":"mitigate",' \
        '"target":{"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}'

    # JSON-concise message
    msg_jc1 = '["deny",["cybox:Network_Connection","1.2.3.4"],["openc2:network.router",""],{"response":"ack","where":"perimeter"}]'

    msg_jc2 = '["mitigate",["cybox:Hostname",{"Hostname_Value":"cdn.badco.org"}]]'

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    cmd = OpenC2Command()
    cmd.from_json(msg_jc1)
    print("Action:", cmd.action)
    print("Target:", cmd.target.type, cmd.target.specifiers)
    print("Actuator:", cmd.actuator.type, cmd.actuator.specifiers)
    print("Modifiers:")
    for key, value in cmd.modifiers:
        print("    ", key + ": ", value)
