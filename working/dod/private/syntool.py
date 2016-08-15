import codec, inspect
from importlib import import_module

'''
Translate among abstract syntax formats

Abstract Formats:
  Abstract Syntax Tree - internal data structure
  JASN - JSON Abstract Syntax Notation (AST in JSON format)
  Python Classes - Python source code for class definitions
  Pseudo ASN.1 - ASN.1-like language with added Map and Attribute types

Concrete Formats:
  JSON-Verbose - Structures encoded as objects (named keyword fields)
  JSON-Concise - Structures encoded as arrays (positional fields)
  JSON-Minimized - JSON-Concise plus field names and enumerated values replaced by tags
  Binary - Mapping of JSON-Minimized to a TBD JSON-Binary format
  XSD - XML Schema Definition
'''

class Element:
    def __init__(self, name="", type=None, namespace="", module="", fields=[]):
        self.name = name            # identifier
        self.type = type            # datatype: Element - builtin or defined
        self.namespace = namespace  # identifier
        self.module = module        # identifier
        self.fields = fields        # list of field: (name, Element, modifiers)
                                    #    or list of Enumerated values: (name, tag) or name

class ASDefs:
    def __init__(self, root=None):
        self.terminals = {k: v for k, v in inspect.getmembers(codec, inspect.isclass)}
