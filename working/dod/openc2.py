from codec import Map, OrderedMap, Record
from codec import VString, VTime, VTimeInterval

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

# Test the classes using example messages
if __name__ == '__main__':
    cmd_v = '{"action":"deny",' \
            '"target":{"type":"ipaddr","specifiers":"1.2.3.4"},' \
            '"actuator":{"type":"router","specifiers":"port:2"},' \
            '{"response":"ack"}}'

    cmd_c = '["deny",["ipaddr","1.2.3.4"],["router","port:2"],{"response":"ack"}]'

    cmd = OpenC2Command()
    cmd.from_json(cmd_c)
    print("Action:", cmd.action, "Target:", cmd.target.type, cmd.target.specifier)
    print("  Actuator:", cmd.actuator.type, cmd.actuator.specifier)
    print("  Modifiers:", cmd.modifiers)
