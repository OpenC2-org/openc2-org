#JSON Abstract Encoding Notation

JSON Abstract Encoding Notation (JAEN, pronounced Jane) is a JSON document
format for defining abstract schemas.  Unlike concrete schema languages
such as XSD and JSON Schema, JAEN defines the structure of datatypes
independently of the serialization used to communicate or store data objects.

JAEN Abstract Syntax (JAS) is a source format used to create JAEN files.
Although JAEN can be edited directly, JAS is simpler to read and write,
eliminating the boilerplate (quotes, braces, and brackets) required by JSON.

Note: The following changes were made based on feedback from the 29 September
OpenC2 Forum meeting:

1. Change name to JAEN to avoid phonetic confusion with JSON
2. Add "Description" column to structure definitions
3. Change "Options" column from string to list of strings

This folder includes:

1. JAS source files for Openc2 and CybOX 2.1
2. JAEN files for OpenC2 and CybOX 2.1 generated from JAS sources
3. Property Table files for OpenC2 and Cybox 2.1, generated from JAEN sources
4. Tools folder containing JAEN translation software
