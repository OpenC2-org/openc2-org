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
        ('scan',        BaseCmd, ''),     #  1
        ('locate',      BaseCmd, ''),     #  2
        ('query',       BaseCmd, ''),     #  3
        ('report',      BaseCmd, ''),     #  4
        ('get',         BaseCmd, ''),     #  5
        ('notify',      BaseCmd, ''),     #  6
        ('deny',        BaseCmd, ''),     #  7
        ('contain',     BaseCmd, ''),     #  8
        ('allow',       BaseCmd, ''),     #  9
        ('start',       BaseCmd, ''),     # 10
        ('stop',        BaseCmd, ''),     # 11
        ('restart',     BaseCmd, ''),     # 12
        ('pause',       BaseCmd, ''),     # 13
        ('resume',      BaseCmd, ''),     # 14
        ('cancel',      BaseCmd, ''),     # 15
        ('set',         BaseCmd, ''),     # 16
        ('update',      BaseCmd, ''),     # 17
        ('move',        BaseCmd, ''),     # 18
        ('redirect',    BaseCmd, ''),     # 19
        ('delete',      BaseCmd, ''),     # 20
        ('snapshot',    BaseCmd, ''),     # 21
        ('detonate',    BaseCmd, ''),     # 22
        ('restore',     BaseCmd, ''),     # 23
        ('save',        BaseCmd, ''),     # 24
        ('modify',      BaseCmd, ''),     # 25
        ('throttle',    BaseCmd, ''),     # 26
        ('delay',       BaseCmd, ''),     # 27
        ('substitute',  BaseCmd, ''),     # 28
        ('copy',        BaseCmd, ''),     # 29
        ('sync',        BaseCmd, ''),     # 30
        ('distill',     BaseCmd, ''),     # 31
        ('augment',     BaseCmd, ''),     # 32
        ('investigate', BaseCmd, ''),     # 33
        ('mitigate',    BaseCmd, ''),     # 34
        ('remediate',   BaseCmd, ''),     # 35
        ('response',    BaseCmd, ''),     # 36
        ('alert',       BaseCmd, '')]     # 37