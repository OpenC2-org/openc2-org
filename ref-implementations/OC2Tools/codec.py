import json, re
from functools import reduce

"""
Abstract Object Encoder/Decoder

Classes used to define Datatypes using an abstract syntax, and
encode/decode instances of those types using a concrete message format.

Datatypes are specified in JSON Abstract Syntax Notation (JASN) schemas,
or Python classes, or "Pseudo ASN" documemnts, all of which represent and can
be generated from the same abstract schema.

Currently supports three JSON-based concrete message formats (verbose, concise,
and minimized) but can be extended to support XML-based and binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

# TOTO: replace static classes with dynamically loaded JASN schemas
# TODO: replace error messages with ValidationError exceptions
# TODO: parse field options at initialization

# Dict conversion utilities

def _dmerge(x, y):
    k, v = next(iter(y.items()))
    if k in x:
        _dmerge(x[k], v)
    else:
        x[k] = v
    return x

def hdict(keys, value, sep="."):
    """
    Convert a hierarchical-key value pair to a nested dict
    """
    return reduce(lambda v, k: {k: v}, reversed(keys.split(sep)), value)

def fluff(src, sep="."):
    """
    Convert a flat dict with hierarchical keys to a nested dict

    :param src: flat dict - e.g., {"a.b.c": 1, "a.b.d": 2}
    :param sep: separator character for keys
    :return: nested dict - e.g., {"a": {"b": {"c": 1, "d": 2}}}
    """
    return reduce(lambda x, y: _dmerge(x, y), [hdict(k, v, sep) for k, v in src.items()], {})

def flatten(cmd, path="", fc={}, sep="."):
    """
    Convert a nested dict to a flat dict with hierarchical keys
    """
    fcmd = fc.copy()
    if isinstance(cmd, dict):
        for k, v in cmd.items():
            k = k.split(":")[1] if ":" in k else k
            fcmd = flatten(v, sep.join((path, k)) if path else k, fcmd)
    else:
        fcmd[path] = ('"' + cmd + '"' if isinstance(cmd, str) else str(cmd))
    return (fcmd)

def parse_type_opts(ostr):
    """
    Parse options included in type definitions

    Type definitions consist of 1) type name, 2) parent type, 3) options string, 4) list of fields/items
    Returns a dict of options:
    String   Dict key   Dict val  Option
    ------   --------   -------  ------------
    ">*"     "pattern"  string   regular expression to match against String value
    """
    opts = {}
    if ostr[:1] == ">":
        opts["pattern"] = ostr[1:]
    elif ostr:
        print("Unknown type option", ostr)
    return opts

def parse_field_opts(ostring):
    """
    Parse options included in field definitions

    Field definitions consist of 1) field name, 2) datatype class, and 3) options string
    Ostring contains a comma separated list of values.  Return a dict of options, including:
    String   Dict key   Dict val  Option
    ------   --------   -------  ------------
    "?"      "optional" Boolean  Field is optional, equivalent to [0:1]
    "{key}"  "atfield"  String   Field name of type of an Attribute field
    "[n:m]"  "range"    Tuple    Min and max lengths for arrays and strings
    """
    opts = {"optional": False}
    for o in ostring.split(","):  # TODO: better validation ("," in string, etc)
        if o == "?":
            opts["optional"] = True
        elif o:
            m = re.match("{(\w+)}$", o)
            if m:
                opts["atfield"] = m.group(1)
            else:
                print("Unknown field option '", o, "'")
    return opts

class Codec:

# Class attributes for settings
    verbose_record = False  # Record values serialized with string field names if True, else as arrays
    verbose_enum = True     # Enumerated values serialized as name strings.
    case_match = False      # Case-sensitive string matching for field names and enums if True
    _case_produce = "upper" # Field names and enums capitalization (pass/lower/upper/proper)
    debug = False           # Print debugging info if True

    def __init__(self, debug=None, verbose_record=None, verbose_enum=None, case_match=None, case_produce=None):
        self.vtree = None
        if debug is not None:
            Codec.debug = debug
        if verbose_record is not None:
            Codec.verbose_record = verbose_record
        if verbose_enum is not None:
            Codec.verbose_enum = verbose_enum
        if case_match is not None:
            Codec.case_match = case_match
        if case_produce is not None:
            Codec.case_produce = case_produce
        if hasattr(self, "ns"):
            self._ns = self.ns if Codec.case_match else self.ns.lower()
        if hasattr(self, "vals") and self.vals:
            assert(isinstance(self.vals, list) and isinstance(self.vals[0], (tuple, str)))
            ns = self._ns + ":" if hasattr(self, "_ns") else ""
            if isinstance(self.vals[0], tuple):
                self._fields = [f[0] if ":" in f[0] else ns + f[0] for f in self.vals]
            else:
                self._fields = [f if ":" in f else ns + f for f in self.vals]
            if not Codec.case_match:
                self._fields = [f.lower() for f in self._fields]
            self._fx = {v:n for n, v in enumerate(self._fields)}
            self.dlog("init: %s %d %s" % (type(self).__name__, len(self.vals), self._fx))
        else:
            self.dlog("init: %s" % (type(self).__name__))

    def from_json(self, valstr, auto_verbose=True):
        self.vtree = json.loads(valstr)
        if auto_verbose:
            Codec.verbose_record = isinstance(self.vtree, dict)
        return self.decode(self.vtree, "")

    def dlog(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

# Validating property setter for case_produce options
    @property
    def case_produce(self):
        return self._case_produce

    @case_produce.setter
    def case_produce(self, value):
        options = ("pass", "lower", "upper", "proper")
        if value.lower() in options:
            self._case_produce = value.lower()
        else:
            raise ValueError("case_produce must be one of: " + str(options))

    def norm(self, v):
        fv = v if self.case_match else v.lower()
        return fv if ":" in fv else self._ns + ":" + fv

    def normalize_fields(self, vtree):
        """
        Normalize field names to lower case and explicit namespace

        :return: dict mapping normalized value to original value
        """
        nfields = {}
        if isinstance(vtree, dict):
            nfields = {self.norm(k):k for k in vtree}
        elif isinstance(vtree, str):
            nfields = {self.norm(vtree):vtree}
        return nfields

    def check_fields(self, nfields):
        """
        Check decoded normalized field names against class fields
        """
        if isinstance(nfields, dict):
            nf = set(nfields)
            cf = set(self._fields)
            if nf - cf:                     # TODO: don't flag wildcard as mismatch for Choice objects
                print("ValidationError: %s: Unrecognized var %s, should be in %s" % (type(self).__name__, nf - cf, cf))


class Boolean(Codec):
    def decode(self, val, opts):
        if not isinstance(val, bool):
            print("ValidationError: %r is not boolean" % val)
        return val

    def encode(self):
        pass

class Integer(Codec):
    def decode(self, val, opts):
        if not isinstance(val, int):
            print("ValidationError: %r is not int" % val)
        return val

    def encode(self):
        pass

class String(Codec):
    def decode(self, val, opts):
        if not isinstance(val, str):
            print("ValidationError: %r is not a string" % val)
        return val

    def encode(self):
        pass

class Enumerated(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        ns = self.__module__
        v = val if ":" in val else self._ns + ":" + val
        v = v if self.case_match else v.lower()
        assert v in self._fields, "%s: %s not in %s" % (type(self).__name__, v, self._fields)
        return val

    def encode(self):
        pass

class Map(Codec):           # TODO: handle Choice fields?  Which key?
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict):
            print("Map: Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+"..."))
            return

        nfields = self.normalize_fields(vtree)
        map = {}
        for n, f in enumerate(self.vals):
            opts = parse_field_opts(f[2])
            x = f[0]
            if x in vtree:
                field = f[1]()
                self.dlog("  Map field#", x, type(field).__name__, vtree[x], opts)
                map[x] = field.decode(vtree[x], opts)
            else:
                if not opts["optional"]:
                    print("ValidationError: %s: missing Map element '%s' %s" % (type(self).__name__, x, opts))
        return map

    def encode(self):
        pass

class Record(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("%r is not a %s" % (str(vtree)[:20]+"...", "dict" if self.verbose_record else "list"))
        nfields = self.normalize_fields(vtree)
        self.check_fields(nfields)
        rec = {}
        for n, f in enumerate(self.vals):
            fopts = parse_field_opts(f[2])
            field = f[1]()
            x = self._fields[n] if self.verbose_record else n
            if isinstance(field, Choice):
                if self.verbose_record:
                    rec.update(field.decode(vtree, fopts))  # Unordered - search all fields for matching key
                else:
                    rec.update(field.decode(vtree[x], fopts))
            else:
                if x in nfields if self.verbose_record else n < len(vtree) and vtree[n] is not None:    # Exists
                    if "atfield" in fopts:
                        fopts["atype"] = rec[fopts["atfield"]]
                    vx = nfields[x] if self.verbose_record else x
                    rec[f[0]] = field.decode(vtree[vx], fopts)
                else:
                    if not fopts["optional"]:
                        print("ValidationError: %s: missing Record element '%s' %r" % (type(self).__name__, f[0], opts))
        return rec

    def encode(self):
        pass

class Choice(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("ValidationError: %r is not a %s" % (str(vtree)[:20] + "...", "dict" if self.verbose_record else "list"))
        if self.verbose_record:
            nfields = self.normalize_fields(vtree)
            nf = set(self._fields) & set(nfields)
            if len(nf) > 1:
                print("ValidationError: %s Choice matches more than one element: %s" % (type(self).__name__, nf))
                return {"***": "Choice Error"}
            elif len(nf) < 1:
                print("ValidationError: %s Choice - no match for %s in %s" % (type(self).__name__, set(nfields), self._fields))
                return {"***": "Choice Error"}
            nf = next(iter(nf))
            val = vtree[nfields[nf]]
        elif len(vtree) == 2:
            nf = next(iter(self.normalize_fields(vtree[0])))
            val = vtree[1]
        else:
            print("ValidationError: %s: bad choice %s: %s" % (type(self).__name__, type(vtree), vtree))
            return
        self.dlog("Choice:", nf + "[" + str(self._fx[nf]+1) + "]", val)
        return {nf: self.vals[self._fx[nf]][1]().decode(val, "")}

    def encode(self):
        pass

class Attribute(Codec):
    """
    Attribute value with external type selector
    """
    def decode(self, vtree, opts):
        self.dlog("Attribute#", type(self).__name__, vtree, opts)
        atype = next(iter(self.normalize_fields(opts["atype"])))
        if atype in self._fields:
            field, cls, copts = self.vals[self._fx[atype]]
            self.field = cls()
            self.dlog("Attribute:", self, cls, vtree, copts, opts["atype"])
            return self.field.decode(vtree, copts)
        else:
            print("ValidationError: %s: attribute '%s' not in %s" % (type(self).__name__, atype, self._fields))

    def encode(self):
        pass

class Array(Codec):
    """
    List of values of same datatype (SEQUENCE OF)
    """
    def decode(self, vtree, opts):      # TODO: write array codec
        pass

    def encode(self):
        pass