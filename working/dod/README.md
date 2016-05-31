##Reference Implementation bits & pieces
This folder contains various files that may become part of the reference implementation.
It is not a project folder; files may be copied into project builds.

####Current content:
* OpenC2 message encoder/decoder (work in progress)
* Demo producer - send a hardcoded command
* Demo consumer - receive a command and reply
* Demo command - verbose and concise JSON encoding
* Cybox schemas and schema summaries (condensed version with one line per element)

####Planned content:
* OpenC2 message grammar - ASN.1
* Schema generator - translate grammar into language-specific schemas (JSON, XML, ...)
* Validator to check messages against schema
* Example commands - good and bad, for validator test suite and interop testing
* Toy actuator - receives and validates messages and returns dummy status/content
