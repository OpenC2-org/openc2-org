import json, jsonschema, os
from textwrap import fill
from datetime import datetime

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties

jasn_schema = {
    "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "required": ["module"],
            "additionalProperties": False,
            "properties": {
                "description": {"type": "string"},
                "import": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {"^\\S+$": {"type": "string"}}
                },
                "module": {"type": "string"},
                "root": {"type": "string"},
                "sources": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {
                        "^\\w+$": {"type": "string"}
                    }
                },
                "namespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"},
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "additionalItems": False,
                "items": [
                    {   "type": "string"},
                    {   "type": "string"},
                    {   "type": "string"},
                    {   "type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 4,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}

def jasn_check(jasn):
    jsonschema.Draft4Validator(jasn_schema).validate(jasn)
    for t in jasn["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-item list
        n = 2 if t[1].lower() == "enumerated" else 4
        for i in t[3]:          # item definition: 0-tag, 1-name, 2-type, 3-options
            if len(i) != n:
                print("Item format error:", t[0], t[1], i[1], "-", len(i), "!=", n)
    return jasn                 # TODO: check tag collisions

def jasn_load(fname):
    with open(fname) as f:
        jasn = json.load(f)
    jasn_check(jasn)
    return jasn

def jasn_dumps(jasn):
    return json.dumps(jasn, indent=2)

def jasn_dump(jasn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jasn_dumps(jasn))

def pasn_dumps(jasn):
    pasn = "/*\n"
    hdrs = jasn["meta"]
    hlist = ["module", "title", "version", "description", "namespace", "root", "import", "sources"]
    for h in hlist + list(set(hdrs) - set(hlist)):
        if h in hdrs:
            if h == "description":
                pasn += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h + ":"), subsequent_indent=15*" ") + "\n"
            elif h == "import" or h == "sources":
                hh = "{:14} ".format(h + ":")
                for k, v in hdrs[h].items():
                    pasn += hh + k + ": " + v + "\n"
                    hh = 15*" "
            else:
                pasn += "{0:14} {1:}\n".format(h + ":", hdrs[h])
    pasn += "*/\n"

    pasn += "\n" + jasn["meta"]["module"] + " ::=\nBEGIN\n"

    asn1type = {"String": "UTF8STRING", "Integer": "INTEGER", "Boolean": "BOOLEAN"}
    for t in jasn["types"]:
        tname, ttype, topts, titems = t
        for i in titems:
            if len(i) > 2:
                if i[2] in asn1type:        # Translate primitive types to ASN.1
                    i[2] = asn1type[i[2]]
        pasn += "\n" + tname + " ::= " + ttype.upper() + ("(" + topts + ")" if topts else "") + " {\n"
        flen = min(32, max(12, max([len(i[1]) for i in titems], default=0)))    # TODO: No default in Python 2
        if ttype.lower() == "enumerated":
            fmt = "    {1:" + str(flen) + "} ({0:d})"
        else:
            fmt = "    {1:" + str(flen) + "} [{0:d}] {2}{3}"
        pasn += ",\n".join([fmt.format(*i) for i in titems])
        pasn += ("\n}\n" if titems else "}\n")
    pasn += "END\n"
    return pasn

def pasn_dump(jasn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(pasn_dumps(jasn))

def python_dumps(jasn, fname):
    pass

def tables_dumps(jasn, fname):
    pass

if __name__ == "__main__":
    fname = "cybox"
    source = fname + ".jasn"
    jasn = jasn_load(source)
    pasn_dump(jasn, fname + "_gen.pasn", source)
    jasn_dump(jasn, fname + "_gen.jasn", source)
