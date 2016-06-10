
## Phase I command examples - JSON format
Concise and verbose wire encodings.  Flattened encoding used internally by some applications.

### MITIGATE
#### Concise
```
["mitigate",["cybox:Hostname",["cdn.badco.org"]]]
```
#### Verbose
```
{ "action": "mitigate",
  "target": {
	  "type": "cybox:Hostname",
	  "specifiers": {"Hostname_Value": "cdn.badco.org"}}}
```
#### Flattened
```
{ "action": "mitigate",
  "target.type": "cybox:Hostname",
  "target.specifiers.Hostname_Value": "cdn.badco.org"}
```
### ALLOW / DENY
#### Concise
```
["deny",
["cybox:Network_Connection", [null, "UDP", null, [["1.2.3.4"], "443"]]],
["openc2:network.router", "port:2"],
{"response": "ack", "where": "perimeter"}]
```
#### Verbose
```
{ "action": "deny",
  "target": {
    "type": "cybox:Network_Connection",
    "specifiers": {
      "Layer4Protocol": "UDP",
      "DestinationSocketAddress": {
        "IP_Address": {"Address_Value": "1.2.3.4"},
        "Port": "443"}}},
  "actuator": {
    "type": "openc2:network.router",
    "specifiers": "port:2"},
  "modifiers": {
    "response": "ack",
    "where": "perimeter"}}
```
#### Flattened
```
{ "action": "deny",
  "target.type": "cybox:Network_Connection",
  "target.specifiers.Layer4Protocol": "UDP",
  "target.specifiers.Layer4Protocol.DestinationSocketAddress.IP_Address.Address_Value": "1.2.3.4",
  "target.specifiers.Layer4Protocol.DestinationSocketAddress.IP_Address.Port": "443",
  "actuator.type": "openc2:network.router",
  "actuator.specifiers": "port:2",
  "modifiers.response": "ack",
  "modifiers.where": "perimeter"}
```
