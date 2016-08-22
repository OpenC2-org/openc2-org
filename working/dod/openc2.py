from codec import Enumerated, Map, Record, Attribute, Choice
from codec import VString, VInteger
import cybox

"""
OpenC2 Command Definition

Classes that define the content of OpenC2 commands.  These classes are used with
an Encoder/Decoder (codec) to serialize and deserialize commands for transmission
in a format such as JSON, XML, or CBOR, or to generate format-specific message schemas.
"""

class Action(Enumerated):
    ns = 'openc2'
    vals = [
        'scan',        #  1
        'locate',      #  2
        'query',       #  3
        'report',      #  4
        'get',         #  5
        'notify',      #  6
        'deny',        #  7
        'contain',     #  8
        'allow',       #  9
        'start',       # 10
        'stop',        # 11
        'restart',     # 12
        'pause',       # 13
        'resume',      # 14
        'cancel',      # 15
        'set',         # 16
        'update',      # 17
        'move',        # 18
        'redirect',    # 19
        'delete',      # 20
        'snapshot',    # 21
        'detonate',    # 22
        'restore',     # 23
        'save',        # 24
        'modify',      # 25
        'throttle',    # 26
        'delay',       # 27
        'substitute',  # 28
        'copy',        # 29
        'sync',        # 30
        'distill',     # 31
        'augment',     # 32
        'investigate', # 33
        'mitigate',    # 34
        'remediate',   # 35
        'response',    # 36
        'alert'        # 37
    ]

class Target(cybox.CyboxObject):
    pass

#class TargetSpecifiers(Attribute):
#    ns = 'openc2'
#    vals = [
#        ('cybox:Address', cybox.AddressObjectType, ''),
#        ('cybox:Device', cybox.DeviceObjectType, ''),
#        ('cybox:Hostname', cybox.HostnameObjectType, ''),
#        ('cybox:Network_Connection', cybox.NetworkConnectionObjectType, '')]
#
#class Target(Record):
#    ns = 'openc2'
#    vals = [
#        ('type', cybox.TargetTypeValue, ''),        # TODO: change to CyboxObjectType - cybox doesn't know openc2 target
#        ('specifiers', TargetSpecifiers, '?,{type}')]

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

class OpenC2Command(Record):
    ns = 'openc2'
    vals = [
        ('action', Action, ''),
        ('target', Target, ''),
        ('actuator', Actuator, '?'),
        ('modifiers', Modifiers, '?')]
