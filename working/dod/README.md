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

####Demo producer/consumer:
* Install Python dependencies:
    * Bottle (web server)
    * Requests (web client)
* Download files to working directory
    * codec.py - encoder/decoder base classes
    * cybox.py - selected CybOX datatype definitions
    * openc2.py - OpenC2 command definitions
    * consume.py - Web server / consumer
    * produce-cmd.py - Command generator
* Run consume.py (starts up consumer on localhost, listens for commands)
* Run produce-cmd.py (generates a command and prints response)

Edit produce-cmd to change consumer IP address (default is localhost:8080) or to change the message to be sent.