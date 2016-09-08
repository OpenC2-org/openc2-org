import json, jsonschema, re

jasn_schema = {
    "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "additionalProperties": False,
            "required": ["targetNamespace"],
            "properties": {
                "description": {"type": "string"},
                "import": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {"^\\S+$": {"type": "string"}}
                },
                "root": {
                    "type": "array",
                    "items": [
                        {"type": "string"},
                        {"type": "string"}
                    ]
                },
                "sources": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {
                        "^\\w+$": {"type": "string"}
                    }
                },
                "targetNamespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"},
            }
        },
        "types": {
            "type": "array",
            "items": [
                {
                    "type": "array",
                    "additionalItems": False,
                    "items": [
                        {   "type": "string"},
                        {   "type": "string"},
                        {   "type": "string"},
                        {   "type": "array",
                            "items": {
                                "oneOf": [
                                    {   "type": "array",
                                        "minItems": 2,
                                        "maxItems": 2,
                                        "items": [
                                            {"type": "integer"},
                                            {"type": "string"}
                                        ]
                                    },
                                    {   "type": "array",
                                        "minItems": 4,
                                        "maxItems": 4,
                                        "items": [
                                            {"type": "integer"},
                                            {"type": "string"},
                                            {"type": "string"},
                                            {"type": "string"}
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
}

def jasn_check(jasn):
    jsonschema.Draft4Validator(jasn_schema).validate(jasn)
    for t in jasn["types"]:
        if t[3]:
            tmax = max([len(i) for i in t[3]])
            tmin = min([len(i) for i in t[3]])
            if tmin != tmax or tmax != (2 if t[1].lower() == 'enumerated' else 4):
                print("Item length error:", t[0], t[1], t[2], tmin, tmax)
    return jasn

def jasn_load(fname):
    with open(fname) as f:
        jasn = json.load(f)
    jasn_check(jasn)
    return jasn

def jasn_dumps(jasn, fname):
    return json.dumps(jasn, indent=2)

def pasn_dumps(jasn, fname):
    pasn = ""
    for t in jasn["types"]:
        tname, ttype, topts, titems = t
        pasn += "\n" + tname + " ::= " + ttype.upper() + ("(" + topts + ")" if topts else "") + " {\n"
        flen = min(32, max(12, max([len(i[1]) for i in titems], default=0)))    # TODO: No default in Python 2
        if ttype.lower() == "enumerated":
            fmt = "    {1:" + str(flen) + "} ({0:d})"
        else:
            fmt = "    {1:" + str(flen) + "} [{0:d}] {2}{3}"
        pasn += ",\n".join([fmt.format(*i) for i in titems]) + "\n}\n"
    return pasn

def python_dumps(jasn, fname):
    pass

def tables_dumps(jasn, fname):
    pass

if __name__ == "__main__":
    fname = "cybox"
    jasn = jasn_load(fname + ".jasn")
    print(pasn_dumps(jasn, fname + ".pasn"))
    print(jasn_dumps(jasn, fname + "_saved.jasn"))
