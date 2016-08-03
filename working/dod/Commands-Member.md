
## Phase I command examples - JSON format
###Action_Member syntax.
**Concise** and **Verbose** encodings are transmitted over the wire between systems.
The decoder will accept and validate a message using either format and
return the same information to the application.  
 
**Flattened** encoding is used internally by some applications.  The codec API
can return a command as either a nested dictionary with the same structure
as the Verbose encoding or as a single dictionary as shown for the Flattened
encoding.

These examples reflect an abstract syntax where Action is a **member** of
an OpenC2 command along with Target, Actuator and Modifiers.  Other examples
reflect an abstract syntax where the Action value is the single **root**
element of an OpenC2 command.

Specifiers shown here are derived from CybOX version 2.1 XML definitions.  These
will be updated to use CybOX 3.0 JSON defintions when a stable spec is released.

### MITIGATE
#### Concise
```
["mitigate",
["cybox:Hostname",["cdn.badco.org"]]]
```
#### Verbose
```
{"action": "mitigate",
 "target": {
    "type":"cybox:Hostname",
    "specifiers":{"Hostname_Value":"cdn.badco.org"}}}
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
["DENY",
["cybox:Network_Connection",["IPv4","TCP",[["ip_address",["any"]]],[["ip_address",["10.10.10.2"]]]]],
["network.firewall",[null,"30"]],
{"context_ref": 91}]
```
#### Verbose
```
{"ACTION": "DENY",
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
      "context_ref": 91}}
```
#### Flattened
```
{ "ACTION": "deny",
  "TARGET.type": "cybox:Network_Connection",
  "TARGET.specifiers.Layer3Protocol": "IPv4",
  "TARGET.specifiers.Layer4Protocol": "TCP",
  "TARGET.specifiers.SourceSocketAddress.IP_Address.Address_Value": "any",
  "TARGET.specifiers.DestinationSocketAddress.IP_Address.Address_Value": "10.10.10.2",
  "ACTUATOR.type": "openc2:network.firewall",
  "ACTUATOR.specifiers.asset_id": "30",
  "MODIFIERS.context_ref": 91}
```
