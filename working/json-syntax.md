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

This is represented formally using Abstract Syntax Notation 1 (ASN.1) as
```
OpenC2Message ::= SEQUENCE {
    action    Action,
    target    Target,
    actuator  Actuator OPTIONAL,
    modifiers SET OF Modifier }

Target ::= SEQUENCE {
    type = TargetType,
    specifiers = SET OF TargetSpecifier }

Actuator ::= SEQUENCE {
    type = ActuatorType,
    specifiers = SET OF ActuatorSpecifier
}
```
where SEQUENCE is an ordered list of values of possibly different types
and SET OF is an unordered collection of values of the same type.

The ASN.1 grammar for OpenC2 commands will be progressively refined by
specifying the lower-level syntax details of Action, TargetType,
TargetSpecifier, etc:
```
Action ::= ENUMERATED {
    alert, allow, augment, contain, delay, delete, deny, detonate, distill,
    get, investigate, locate, mitigate, modify, move, notify, pause, query,
    redirect, remediate, report, response, restart, restore, resume, save,
    scan, set, snapshot, start, stop, substitute, sync, throttle, update, ... }

ModifierType ::= ENUMERATED {
    delay,       -- U: timeinterval
    duration,    -- U: timeinterval
    frequency,   -- U: recurrence
    response,    -- U: ResponseValue
    time,        -- U: datetime
    method,      -- DENY,ALLOW: MethodValue
    where,       -- DENY,ALLOW: WhereValue
    ...
}
ResponseValue ::= ENUMERATED { ack, status, ... }
MethodValue ::= ENUMERATED { acl, blackhole, sinkhole, blacklist, whitelist, ... }
WhereValue ::= ENUMERATED { internal, perimeter, ... }
```
Ellipses (...) denote an extension points to facilitate syntax evolution.  In
order to preserve backward compatibility, future syntax versions may define new
fields or enumerated values after an extension point, but must not modify elements
before the extension point.

Comments (-- to end-of-line) are ignored by ASN.1 applications.

###Encodings
Abstract values can be encoded for transmission in different ways, as specified
by encoding rules.  The ASN.1 standard defines several ASN.1-specific encoding
rules (BER, DER, PER) as well as encoding rules for XML.  There are no standard
JSON encoding rules yet, but the ITU-T has approved a work item to develop them.
XML encoding rules include encoding instructions that can specify details of how
an abstract data object is represented in XML.  It is reasonable to expect that
JSON encoding rules will also support encoding instructions, which would allow
the same abstract syntax to support multiple JSON encodings, including verbose
and concise representations of SEQUENCES and ENUMERATED lists.  A verbose encoding
transmits SEQUENCE field names as strings on the wire, while a concise encoding
does not.  The same absract OpenC2 command could be encoded as:
```
JSON-Verbose:

  {"mitigate": {
    "target": {"type":"cybox:Hostname","specifiers":{"Hostname_Value":"cdn.badco.org"}}}}

JSON-Concise:

  ["mitigate",[
    ["cybox:Hostname",["cdn.badco.org"]]]]

JSON-Min:

  [13,[[1:72,["cdn.badco.org"]]]]
```
The last example replaces enumerated values with ordinal indexes, similar to the
minimization process routinely applied to both Javascript code and JSON data
to optimize web execution.  Similar examples could be developed for verbose and
concise XML representations of the same OpenC2 command through use of encoding
instructions.

##Summary
OpenC2 commands will be defined using abstract syntax notation that is independent
of the language (JSON, XML, various binary options) and dialect (varying levels
of verbosity) used to encode and decode the commands for transmission.  The abstract
syntax can be translated into language-specific schemas (xsd, json-schema) used by
applications to validate messages.  Use of an abstract syntax ensures that production
software with binary transmission (e.g., Compact Binary Object Represenation - CBOR)
remains aligned with other OpenC2 applications as the schema evolves.
