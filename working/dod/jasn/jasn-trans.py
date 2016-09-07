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
                    "patternProperties": {
                        "^\\S+$": {
                            "type": "array",
                            "additionalItems": False,
                            "items": [
                                {"type": "string"},
                                {"type": "string"}
                            ]
                        }
                    }
                },
                "root": {"type": "string"},
                "sources": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {
                        "^\\w+$": {"type": "string"}
                    }
                },
                "targetNamespace": {
                    "type": "array",
                    "additionalitems": False,
                    "items": [
                        {"type": "string"},
                        {"type": "string"}
                    ]
                },
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

def load_jasn(fname):
    with open(fname) as f:
        jasn = json.load(f)
    jsonschema.Draft4Validator(jasn_schema).validate(jasn)
    return jasn

def dump(jasn):
    for t in jasn["types"]:
        tname, ttype, topts, tdata = t
        print(tname + ": " + ttype + "(" + topts + ")")
        for d in tdata:
            print("  ", d)

def to_python(jasn):
    pass

def to_pasn(jasn):
    pass

def to_tables(jasn):
    pass

def check(jasn):
    pass

if __name__ == '__main__':
    jasn = load_jasn('cybox.jasn')
    check(jasn)
    dump(jasn)
