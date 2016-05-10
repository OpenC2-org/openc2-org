## OpenC2 Message Syntax
The *OpenC2 Language Description* documents the conceptual abstract syntax
of an OpenC2 command as:

```
<ACTION> (
  TARGET (
    type = <TARGET_TYPE>,
    [<target-specifier>]
  ),
  [ACTUATOR (
    type = <ACTUATOR_TYPE>,
    [<actuator-specifier>]
  )],
  [<modifiers>]
)
```

Applications process and store OpenC2 messages using application-specific
data structures, but in order to communicate between applications messages
must be serialized in a format understood by both producer and consumer.
Numerous standard serialization formats exist, including XML, JSON, BER,
Protocol Buffers, and many others.  Developers typically select
a transmission format and then define protocols in terms of messages in
that format.  But when the goal is to accommodate multiple transmission
formats, it is preferable to define the protocol using a formal abstract
syntax and then map that abstract syntax to one or more transmission formats,
each of which has its own concrete message syntax.

### JSON Alternatives
Because at least some of the OpenC2 reference implementations (e.g., openc2-edge)
use the libucl library which supports multiple configuration file formats
(nginx-like, json-like, yaml), the messages used by that software can serve
as a starting point for defining an OpenC2 JSON syntax, if made available
to the Forum.  In the absence of software-generated message examples, there
are several possibilities for interpreting the conceptual syntax as applied
to JSON encoding:
#### #1 Flat Array, fixed length
The OpenC2 message is a fixed-length list of 4 elements where one or both
of the last 2 may be empty.  This is the most straightforward interpretation
of the conceptual abstract syntax from a processing standpoint.
```
[
  "SCAN",
  ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
  ["network.sensor"],
  {"delay": "1h", "response": "ack"}
]

[
  "SCAN",
  ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
  [],
  {}
]
```
#### #2 Flat Array, variable length
The OpenC2 message is a list of 2, 3, or 4 elements (ACTION and TARGET mandatory,
ACTUATOR and MODIFIERS optional).  If ACTUATOR and MODIFIERS are different types
(array and object respectively), a parser can determine unambiguously which is
present in a 3 element list.  This is the most compact interpretation, but requires
more logical complexity than the fixed length array.
```
[
  "SCAN",
  ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
  {"delay": "1h", "response": "ack"}
]
```
#### #3 Flat Object
```
{
  "ACTION": "SCAN",
  "TARGET": ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
  "ACTUATOR": ["network.sensor"],
  "MODIFIERS": {"delay": "1h", "response": "ack"}
}
```
The object format uses names for each of the fields as shown in the conceptual abstract
syntax, but the names are unnecessary baggage for messages where the 4 top-level
fields are fixed.  Names would be useful if OpenC2 expected to expand the message to contain
more or different top-level fields.  But this is not necessary, as modifiers provide
a completely general expansion mechanism.
```
{
  "ACTION": "SCAN",
  "TARGET": ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
  "ACTUATOR": ["network.sensor"],
  "delay": "1h",
  "response": "ack"
}
```
This is the fully-flattened object format, with modifiers moved to the top level.
#### #4 Nested Object
```
{
  "SCAN": {
    "TARGET": ["cybox:Device",{"cybox:DeviceObjectType:SerialNumber":"34XR05289"}],
    "ACTUATOR": ["network.sensor"],
    {"delay": "1h", "response": "ack"}
  }
}
```
This is the most literal interpretation of the conceptual abstract syntax, but
there is no apparent benefit to nesting the target, actuator, and modifier fields
within an outer action field.
### Substructure
For all top-level alternatives, the TARGET and ACTUATOR fields are shown as two-element
arrays consisting of a required type and an optional object containing one or more
specifiers.  The modifiers field is an object containing an arbitrary number of name-value
pairs.  Other formats are possible but these appear to be optimal.
## Recommendation
Designate option #1 as the OpenC2 JSON message format, with substructure as shown in the
examples.  After the JSON format is selected, a formal abstract syntax can be specified,
and other encodings can be derived from the abstract syntax.
