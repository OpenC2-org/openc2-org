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
        ('cybox2:Address', cybox.AddressObjectType, ''),
        ('cybox2:Hostname', cybox.HostnameObjectType, ''),
        ('cybox2:Network_Connection', cybox.NetworkConnectionObjectType, '')]

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
