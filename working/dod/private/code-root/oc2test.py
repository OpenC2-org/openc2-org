from openc2 import OpenC2Command
from codec import flatten

'''
Test the OpenC2 decoder/validator using good and bad example commands
'''

if __name__ == '__main__':
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

# Bad messages - should generate meaningful validation errors

    # command body should be a list [target, actuator, modifiers]
    msg_jc1bad1 = '''
["mitigate",
    "cybox2:Hostname",["cdn.badco.org"]]
    '''

    # target should be a list [type, specifiers]
    msg_jc1bad2 = '''
["mitigate",[
    "cybox2:Hostname",["cdn.badco.org"]]]
    '''

    # specifiers should be a list
    msg_jc1bad3 = '''
["mitigate",[
    "cybox2:Hostname","cdn.badco.org"]]
    '''

    # command body should be a dict under action
    msg_jv1bad1 = '''
{"action": "mitigate",
    "target": {"type":"cybox2:Hostname","Hostname_Value":"cdn.badco.org"}}
    '''

    # specifiers should be a dict
    msg_jv1bad2 = '''
{"mitigate": {
    "target": {"type":"cybox2:Hostname","Hostname_Value":"cdn.badco.org"}}}
    '''

    # missing choice specifier "ip_address"
    msg_jc2bad1 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,[["1.2.3.4"],[443]]]],
    ["openc2:network.router",["port","2"]],
    {"response":"ack","where":"perimeter"}]]
    '''

    # missing ip_address list
    msg_jc2bad2 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,["ip_address",["1.2.3.4"],[443]]]],
    ["openc2:network.router",["port","2"]],
    {"response":"ack","where":"perimeter"}]]
    '''

    # missing socketaddressobj list
    msg_jc2bad3 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,["ip_address",["1.2.3.4"]],[443]]],
    ["openc2:network.router",["port","2"]],
    {"response":"ack","where":"perimeter"}]]
    '''

    # address_value not a list
    msg_jc2bad4 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,["ip_address","1.2.3.4"],[443]]],
    ["openc2:network.router",["port","2"]],
    {"response":"ack","where":"perimeter"}]]
    '''

    # port_value not list, not integer
    msg_jc2bad5 = '''
["deny", [
    ["cybox2:Network_Connection",[null,"UDP",null,[["ip_address",["1.2.3.4"]],"443"]]],
    ["openc2:network.router",["2"]],
    {"response":"ack","where":"perimeter"}]]
    '''

    msg_jc3bad1 = '''
["DENY", [
    ["cybox2:Network_Connection",["IPv4","TCP",["ip_address",["any"]],["ip_address",["10.10.10.2"]]]],
    ["network.firewall",[null,"30"]],
    {"context_ref": 91}]]
    '''

    # XML test messages
    msg_xc = '<...>'

    msglist = [
        msg_jc1, msg_jv1, msg_jc2, msg_jv2, msg_jc3, msg_jv3,
        msg_jc1bad1, msg_jc1bad2, msg_jc1bad3,
        msg_jc2bad1, msg_jc2bad2, msg_jc2bad3, msg_jc2bad4, msg_jc2bad5,
        msg_jc3bad1,
    ]

    # Deserialize a message and print its content
    oc2 = OpenC2Command(debug=True)
    msg = msg_jv2
    cmd = oc2.from_json(msg)        # Convert message to nested dict
    fcmd = flatten(cmd)             # Convert nested dict to flat dict

    print("Transmitted Message:", msg)
    print("Decoded Command:", cmd)                         # Data structure API
#    print("Command:", cmd.name, cmd.type, cmd.value)       # Class attribute API

# Print fields from nested dict format

    cmdname = next(iter(cmd))
    cmdval = cmd[cmdname]
    print("\nCommand:", cmdname)

    t = cmdval['target']
    print("  Target: type =", t['type'])
    for k, v in t['specifiers'].items():
        print('    ', k + ':', v)

    a = cmdval['actuator'] if 'actuator' in cmdval else None
    if a:
        act = a['type']
        acs = a['specifiers']
    else:
        act = 'None'
        acs = {}
    print("  Actuator: type =", act)
    for k, v in acs.items():
        print('    ', k + ':', v)

    print("  Modifiers:")
    if 'modifiers' in cmdval:
        for k, v in cmdval['modifiers'].items():
            print("    ", k + ":", v)
    else:
        print("    None")

# Print fields from flattened dict format

    print("\nCommand (flat format): {")
    for k, v in sorted(fcmd.items()):
        print("  ", k + ":", v)
    print("}")