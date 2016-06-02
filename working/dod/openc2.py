from codec import Map, Record
from codec import VString, VTime, VTimeInterval

"""
OpenC2 Command Definition

Classes that define the content of OpenC2 commands.  These classes are used with
an Encoder/Decoder (codec) to serialize and deserialize commands for transmission
in a format such as JSON, XML, or CBOR, or to generate format-specific message schemas.

Applications get and set the values of a command using class attributes.
"""

class Target(Record):
    vals = [('type', '', VString),
            ('specifiers', '?', VString)]

class Actuator(Record):
    vals = [('type', '', VString),
            ('specifiers', '?', VString)]

class Modifiers(Map):
    vals = [('response', '?', VString),
            ('time', '?', VTime),
            ('delay', '?', VTimeInterval)]

class OpenC2Command(Record):
    vals = [('action', '', VString),
            ('target', '', Target),
            ('actuator', '?', Actuator),
            ('modifiers', '?', Modifiers)]


# Test the OpenC2 classes using example serializations of the same content
if __name__ == '__main__':
    # JSON-verbose message
    msg_jv = '{"action":"deny",' \
            '"target":{"type":"ipaddr","specifiers":"1.2.3.4"},' \
            '"actuator":{"type":"router","specifiers":"port:2"},' \
            '{"response":"ack"}}'

    # JSON-concise message
    msg_jc = '["deny",["ipaddr","1.2.3.4"],["router","port:2"],{"response":"ack"}]'

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content
    cmd = OpenC2Command()
    cmd.from_json(msg_jc)
    print("Action:", cmd.action, "Target:", cmd.target.type, cmd.target.specifier)
    print("  Actuator:", cmd.actuator.type, cmd.actuator.specifier)
    print("  Modifiers:")
    for key, value in cmd.modifiers:
        print("    ", key + ": ", value)
