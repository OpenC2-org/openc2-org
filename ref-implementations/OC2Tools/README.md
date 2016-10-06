##Reference Implementation bits & pieces
This folder contains various files that may become part of the reference implementation.
It is not a project folder; files may be copied into project builds.

###Current content:
* OpenC2 message decoder/validator
* Demo producer - send a hardcoded command 
* Demo consumer - receive a command and reply
* Demo commands - JSON commands to be used in Phase 1 demo: Mitigate and Allow/Deny
* Test commands - good and bad

###Planned content:
* Codec encoder methods
* Codec test suite (tox)
* JSON Abstract Encoding Notation (JAEN) format converter and grammars - Python classes, PseudoASN
* JAEN codec with dynamically loadable message syntax
* Concrete schema generators - translate JAEN into language-specific schemas (JSON, XML, CBOR, Proto, ...)
* Toy actuator - receives and validates messages and returns dummy status/content

###Using the message decoder/validator:
* Install Python 3 if not already available.
    * Code tested on version 3.5.2.  Python 2 not yet supported.
* Download:
    * codec.py - encoder/decoder classes
    * openc2.py - OpenC2 command definitions
    * cybox.py - CybOX v2.1 object definitions
    * oc2test.py - Example code to decode, validate and print an OpenC2 command
* Run oc2test.py - prints example JSON string, decoded command dict, and individual fields of the command.

###Demo producer/consumer:
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