import requests

device = 'http://localhost:8080/openc2/'
cmd_v = [
    '{"action":"deny","target":"foo"}',  # bad
    '{"action":"deny",'
    '"target":{"type":"ipaddr","specifiers":"1.2.3.4"},'
    '"actuator":{"type":"router","specifiers":"port:2"},'
    '"modifiers":{"response":"ack"}}'
]
cmd_c = [
    '["deny","foo"]',                    # bad
    '["deny",["ipaddr","1.2.3.4"],["router","port:2"],{"response":"ack"}]'
]
cmd = cmd_c[1]

print('Send ('+str(len(cmd))+'):', cmd)
hdr = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.post(device, headers=hdr, data=cmd)
print('Response (' + r.encoding + '):')
print('  sent hdr:', r.request.headers)
print('  resp hdr:', r.headers)
print(' resp body:', r.text)
