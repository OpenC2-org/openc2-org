import json

msg_jv1 = '''
{"mitigate": {
"target": {"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}}
'''

msg_jv2 = '''
{"deny": {
"target": {
    "type": "cybox:Network_Connection",
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

msg_jv3 = '''
{"DENY": {
"TARGET": {"type": "cybox:Network_Connection",
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

def flatten(cmd, path="", lines=[]):
    if isinstance(cmd, dict):
        for k,v in cmd.items():
            k = k.split(sep=':')[1] if ':' in k else k
            flatten(v, '.'.join((path, k)) if path else k, lines)
    else:
        lines.append('  "' + path + '":' + ('"' + cmd + '"' if isinstance(cmd, str) else str(cmd)))
    return(lines)

for msg in (msg_jv1, msg_jv2, msg_jv3):
    cmd = json.loads(msg)
    lines = flatten(cmd, lines=[])
    print("\n{\n" + ',\n'.join(lines) + "\n}")
