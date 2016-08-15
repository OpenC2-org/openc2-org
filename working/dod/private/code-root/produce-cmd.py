import requests

device = 'http://localhost:8080/openc2/'
# JSON-concise and JSON-verbose test messages
#   decoder auto-detects format by default

msg_jc1 = '''
["mitigate",[
    ["cybox2:Hostname",["cdn.badco.org"]]]]
'''

msg_jv1 = '''
{"mitigate": {
    "target": {"type":"cybox2:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}}
'''

msg_jc2 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,[["ip_address",["1.2.3.4"]],[443]]]],
    ["openc2:network.router",["2"]],
    {"response":"ack","where":"perimeter"}]]
'''

msg_jv2 = '''
{"deny": {
    "target": {
        "type": "cybox2:Network_Connection",
        "specifiers": {
            "Layer4Protocol": "UDP",
            "DestinationSocketAddress": {
                "IP_Address": {
                    "Address_Value": "1.2.3.4"},
                "Port": {
                    "Port_Value": 443}}}},
    "actuator": {
        "type": "openc2:network.router",
        "specifiers": {"port": "2"}},
    "modifiers": {
        "response": "ack",
        "where": "perimeter"}}}
'''

msg_jc3 = '''
["DENY", [
    ["cybox2:Network_Connection",["IPv4","TCP",[["ip_address",["any"]]],[["ip_address",["10.10.10.2"]]]]],
    ["network.firewall",[null,"30"]],
    {"context_ref": 91}]]
'''

msg_jv3 = '''
{"DENY": {
    "TARGET": {"type": "cybox2:Network_Connection",
        "specifiers": {
            "Layer3Protocol": "IPv4",
            "NetworkConnectionObj:Layer4Protocol": "TCP",
            "NetworkConnectionObj:SourceSocketAddress": {
                "SocketAddressObj:IP_Address": {
                    "AddressObj:Address_Value": "any"}},
            "NetworkConnectionObj:DestinationSocketAddress": {
                "SocketAddressObj:IP_Address": {
                    "AddressObj:Address_Value": "10.10.10.2"}}}},
     "ACTUATOR": {"type": "network.firewall", "specifiers": {"asset_id": "30"}},
     "MODIFIERS": {"context_ref": 91}}}
'''

cmd = msg_jv3

print('Send ('+str(len(cmd))+'):', cmd)
hdr = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.post(device, headers=hdr, data=cmd)
print('Response (' + r.encoding + '):')
print('  sent hdr:', r.request.headers)
print('  resp hdr:', r.headers)
print(' resp body:', r.text)
