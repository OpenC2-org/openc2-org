import codec

"""
OpenC2 Command Tests
"""

# Test the OpenC2 classes using example serializations of the same content
if __name__ == '__main__':
    # JSON-concise and JSON-verbose test messages
    #   TODO: Is cybox:Hostname_Value maxOccurs 1 or unbounded?  Not specified in Hostname_Object.xsd.

    msg_jc1 = '["mitigate",["cybox2:Hostname",["cdn.badco.org"]]]'

    msg_jv1 = '{"action":"mitigate","target":'\
        '{"type":"cybox2:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}'

    msg_jc2 = '["deny",'\
        '["cybox2:Network_Connection",[null,"UDP",null,[["1.2.3.4"],"443"]]],'\
        '["openc2:network.router","port:2"],'\
        '{"response":"ack","where":"perimeter"}]'

    msg_jv2 = '{"action":"deny",'\
        '"target":{"type":"cybox2:Network_Connection","specifiers":{"Layer4Protocol":"UDP",'\
        '"DestinationSocketAddress":{"IP_Address":{"Address_Value":"1.2.3.4"},"Port":"443"}}},'\
        '"actuator":{"type":"openc2:network.router","specifiers":"port:2"},'\
        '"modifiers":{"response":"ack","where":"perimeter"}}'

    # XML message
    msg_xc = '<...>'

    # Deserialize a message and print its content

    oc2 = codec.load("openc2.jasn", "OpenC2Command")
    msg = msg_jc1
    print("   Raw Command:", msg)
    cmd = oc2.from_json(msg)
    print("Parsed Command:", cmd)

    print("Action:", cmd['action'])
    t = cmd['target']
    print("Target:", t['type'], t['specifiers'])
    if 'actuator' in cmd:
        act = cmd['actuator']['type']
        acs = cmd['actuator']['specifiers']
    else:
        act = 'None'
        acs = ''
    print("Actuator:", act, acs)
    if 'modifiers' in cmd:
        print("Modifiers:")
        for key, value in cmd['modifiers'].items():
            print("    ", key + ": ", value)
    else:
        print("Modifiers: None")
