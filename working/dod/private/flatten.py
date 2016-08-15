import json
from functools import reduce

def _dmerge(x, y):
    k, v = next(iter(y.items()))
    if k in x:
        _dmerge(x[k], v)
    else:
        x[k] = v
    return x

def _hdict(keys, value, sep):
    return reduce(lambda v, k: {k: v}, reversed(keys.split(sep)), value)

def fluff(src, sep='.'):
    '''
    Convert a flat dict with hierarchical keys to a nested dict

    :param src: flat dict - e.g., {"a.b.c": 1, "a.b.d": 2}
    :param sep: separator character for keys
    :return: nested dict - e.g., {"a": {"b": {"c": 1, "d": 2}}}
    '''
    return reduce(lambda x, y: _dmerge(x, y), [_hdict(k, v, sep) for k, v in src.items()], {})

def flatten(cmd, path="", fc={}, sep='.'):
    '''
    Convert a nested dict to a flat dict with hierarchical keys
    '''
    fcmd = fc.copy()
    if isinstance(cmd, dict):
        for k,v in cmd.items():
            k = k.split(':')[1] if ':' in k else k
            fcmd = flatten(v, sep.join((path, k)) if path else k, fcmd)
    else:
        fcmd[path] = ('"' + cmd + '"' if isinstance(cmd, str) else str(cmd))
    return(fcmd)


msg_jv1 = '''
{"mitigate": {
"target": {"type":"cybox2:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}}
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

def ppr(data, name='', level=0, indent=4):
    sp = level * indent * ' '
    spn = sp + (name + ': ' if name else '')
    if isinstance(data, dict):
        print(spn + '{')
        for k in sorted(data):
            ppr(data[k], k, level + 1, indent)
        print(sp + '}')
    elif isinstance(data, list):
        print(sp + '[')
        for v in data:
            ppr(v, '', level + 1, indent)
        print(sp + ']')
    else:
        print(spn + str(data))

for msg in (msg_jv1, msg_jv2, msg_jv3):
    cmd = json.loads(msg)
    cmdf = flatten(cmd)
    cmdff = fluff(cmdf)
    ppr(cmdf, indent=2)
    ppr(cmdff, indent=2)

