msg_jc1a = '["mitigate",["cybox2:Hostname",["cdn.badco.org","xyz.foo.com"]]]'

msg_jv1a = '{"action":"mitigate","target":' \
           '{"type":"cybox2:Hostname","specifiers":["cdn.badco.org","xyz.foo.com"]}}'

msg_jv2_bad = '{"action":"deny",' \
    '"target":{"type":"cybox2:Network_Connection","specifiers":{"Layer4Protocol":"UDP",' \
    '"DestinationSocketAddress":{{"IP_Address":"1.2.3.4"},"Port":"443"}},' \
    '"actuator":{"type":"openc2:network.router","specifiers":"port:2"},' \
    '"modifiers":{"response":"ack","where":"perimeter"}}'
