
## Phase I command examples - JSON format
Concise and verbose wire encodings.  Flattened encoding used internally by some applications.

### MITIGATE
#### Concise
```
["mitigate",[
    ["cybox:Hostname",["cdn.badco.org"]]]]
```
#### Verbose
```
{"mitigate": {
    "target": {
        "type":"cybox:Hostname",
        "specifiers":{"Hostname_Value":"cdn.badco.org"}}}}
```
#### Flattened
```
{ "mitigate.target.type": "cybox:Hostname",
  "mitigate.target.specifiers.Hostname_Value": "cdn.badco.org"}
```
### ALLOW / DENY
#### Concise
```
["DENY", [
    ["cybox:Network_Connection",["IPv4","TCP",[["ip_address",["any"]]],[["ip_address",["10.10.10.2"]]]]],
    ["network.firewall",[null,"30"]],
    {"context_ref": 91}]]
```
#### Verbose
```
{"DENY": {
    "TARGET": {"type": "cybox:Network_Connection",
        "specifiers": {
            "Layer3Protocol": "IPv4",
            "Layer4Protocol": "TCP",
            "SourceSocketAddress": {
                "IP_Address": {
                    "Address_Value": "any"}},
            "DestinationSocketAddress": {
                "IP_Address": {
                    "Address_Value": "10.10.10.2"}}}},
     "ACTUATOR": {"type": "openc2:network.firewall",
         "specifiers": {
             "asset_id": "30"}},
     "MODIFIERS": {
         "context_ref": 91}}}
```
#### Flattened
```
{ "deny.target.type": "cybox:Network_Connection",
  "deny.target.specifiers.Layer3Protocol": "IPv4",
  "deny.target.specifiers.Layer4Protocol": "TCP",
  "deny.target.specifiers.SourceSocketAddress.IP_Address.Address_Value": "any",
  "deny.target.specifiers.DestinationSocketAddress.IP_Address.Address_Value": "10.10.10.2",
  "deny.actuator.type": "openc2:network.firewall",
  "deny.actuator.specifiers.asset_id": "30",
  "deny.modifiers.context_ref": 91}
```
