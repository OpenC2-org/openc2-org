##Reference Implementation bits & pieces
This folder contains various files that may become part of the reference implementation.
It is not a project folder; files may be copied into project builds.

####Current content:
* OpenC2 message encoder/decoder
* Demo producer - send a hardcoded command 
* Demo consumer - receive a command and reply
* Cybox schemas and schema summaries (condensed version with one line per element)
* Demo commands - JSON commands to be used in Phase 1 demo: Mitigate and Allow/Deny
* Example commands - good and bad, for validator test suite and interop testing

####Planned content:
* OpenC2 message grammar - ASN.1
* Schema generator - translate grammar into language-specific schemas (JSON, XML, ...)
* Validator to check messages against schema
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
* Run produce-cmd.py (sends a command and prints response from consumer)

Edit produce-cmd to change consumer IP address (default is localhost:8080) or to change the message to be sent.