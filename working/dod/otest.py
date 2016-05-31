from openc2 import OpenC2Command

cmd_v = '{"action":"deny",' \
    '"target":{"type":"ipaddr","specifiers":"1.2.3.4"},' \
    '"actuator":{"type":"router","specifiers":"port:2"},' \
    '{"response":"ack"}}'

cmd_c = '["deny",["ipaddr","1.2.3.4"],["router","port:2"],{"response":"ack"}]'

cmd = OpenC2Command()
cmd.fromJSON(cmd_c)
print(cmd.action, cmd.target.type, cmd.target.specifier)
