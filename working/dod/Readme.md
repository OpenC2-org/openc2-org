##Reference Implementation bits & pieces
This folder contains various files that may become part of the reference implementation.
It is not a project folder; files may be copied into project builds.

####Potential Content:
* OpenC2 message grammar - ASN.1
* Schema generator - translate grammar into language-specific schemas (JSON, XML, ...)
* Validator to check messages against schema
* Example messages - good and bad, for validator test suite and interop testing
* Toy actuator - receives and validates messages and returns dummy status/content
