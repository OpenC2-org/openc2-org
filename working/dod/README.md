##Reference Implementation bits & pieces
This folder contains various files that may become part of the reference implementation.
It is not a project folder; files may be copied into project builds.

####Current content:
* OpenC2 message decoder/validator
* Demo producer - send a hardcoded command 
* Demo consumer - receive a command and reply
* Cybox schemas and schema summaries (condensed version with one line per element)
* Demo commands - JSON commands to be used in Phase 1 demo: Mitigate and Allow/Deny
* Example commands - good and bad, for validator test suite and interop testing

####Planned content:
* Codec encoder methods
* OpenC2 abstract message grammar and format converter - JASN, PseudoASN, ASN.1
* Concrete schema generator - translate grammar into language-specific schemas (JSON, XML, ...)
* Toy actuator - receives and validates messages and returns dummy status/content

####Using the message decoder/validator:
* Install Python 3 if not already available.
    * Code tested on version 3.5.2.  Python 2 not yet supported.
* Download:
    * codec.py - encoder/decoder classes
    * openc2.py - OpenC2 command definitions
    * cybox.py - CybOX v2.1 object definitions
    * oc2test.py - Example code to decode, validate and print an OpenC2 command
* Run oc2test.py - prints example JSON string, decoded command dict, and individual fields of the command.

####Demo producer/consumer:
* Install Python dependencies:
    * Bottle (web server)
    * Requests (web client)
* Download files to working directory
    * codec.py - encoder/decoder classes
    * openc2.py - OpenC2 command definitions
    * cybox.py - CybOX v2.1 object definitions
    * consume.py - Web server / consumer
    * produce-cmd.py - Command generator
* Run consume.py (starts up consumer on localhost, listens for commands)
* Run produce-cmd.py (sends a command and prints response from consumer)

Edit produce-cmd.py to change consumer IP address (default is localhost:8080) or to change the message to be sent.