import requests

device = 'http://localhost:8080/openc2/'
# JSON-concise and JSON-verbose test messages

msg_jc1 = '["mitigate",["cybox:Hostname",["cdn.badco.org"]]]'

msg_jv1 = '{"action":"mitigate","target":' \
          '{"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}'

msg_jc2 = '["deny",' \
          '["cybox:Network_Connection",[null,"UDP",null,[["1.2.3.4"],"443"]]],' \
          '["openc2:network.router","port:2"],' \
          '{"response":"ack","where":"perimeter"}]'

msg_jv2 = '{"action":"deny",' \
          '"target":{"type":"cybox:Network_Connection","specifiers":{"Layer4Protocol":"UDP",' \
          '"DestinationSocketAddress":{"IP_Address":{"Address_Value":"1.2.3.4"},"Port":"443"}}},' \
          '"actuator":{"type":"openc2:network.router","specifiers":"port:2"},' \
          '"modifiers":{"response":"ack","where":"perimeter"}}'

cmd = msg_jc2

print('Send ('+str(len(cmd))+'):', cmd)
hdr = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.post(device, headers=hdr, data=cmd)
print('Response (' + r.encoding + '):')
print('  sent hdr:', r.request.headers)
print('  resp hdr:', r.headers)
print(' resp body:', r.text)
