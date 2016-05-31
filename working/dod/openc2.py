import Codec, json

class Target(Codec):
    type = 'record'
    vals = [('type', '', Codec.Vstring),
            ('specifiers', '?', Codec.Vstring)]

class Actuator(Codec):
    type = 'record'
    vals = [('type', '', Codec.Vstring),
            ('specifiers', '?', Codec.Vstring)]

class Modifiers(Codec):
    type = 'map'
    vals = [('response', '?', Codec.Vstring),
            ('time', '?', Codec.Vtime),
            ('delay', '?', Codec.Vtimeinterval)]

class OpenC2Command(Codec):
    type = 'record'
    vals = [('action', '', Codec.Vstring),
            ('target', '', Target),
            ('actuator', '?', Actuator),
            ('modifiers', '?', Modifiers)]


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
