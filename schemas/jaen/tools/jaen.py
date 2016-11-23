"""
Load, validate, prettyprint, and dump JSON Abstract Encoding Notation (JAEN) schemas
"""

import json
import jsonschema
from datetime import datetime
from codec_utils import opts_s2d

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties
# TODO: Update JAEN file to be array of namespaces ( {meta, types} pairs )

jaen_schema = {
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
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 3,
                        "items": [
                            {"type": "integer"},
                            {"type": "string"},
                            {"type": "string"}
                        ]
                    }
                },
                "module": {"type": "string"},
                "root": {"type": "string"},
                "namespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"}
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 4,
                "maxItems": 5,
                "items": [
                    {"type": "string"},
                    {"type": "string"},
                    {"type": "array",
                        "items": {"type": "string"}
                    },
                    {"type": "string"},
                    {"type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "array",
                                 "items": {"type": "string"}
                                },
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}


def jaen_check(jaen):
    """
    Check JAEN structure against schema, then perform additional checks on type definitions
    """

    jsonschema.Draft4Validator(jaen_schema).validate(jaen)

    for t in jaen["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-description, 4-item list
        if t[1] in ("String", "Integer", "Number", "Boolean"):
            if len(t) != 4:    # TODO: trace back to base type
                print("Type format error:", t[0], "- primitive type", t[1], "cannot have items")
        else:
            if len(t) != 5:
                print("Type format error:", t[0], "- missing items from compound type", t[1])
        for o, v in opts_s2d(t[2]).items():
            if o not in ["pattern"] and o == "optional" and v:      # "optional" not present when value = False
                print("Invalid typedef option:", t[0], o)
        if len(t) > 4:
            n = 3 if t[1].lower() == "enumerated" else 5
            tags = set()
            record = t[1].lower() == "record"
            for k, i in enumerate(t[4]):        # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                tags.update(set([i[0]]))        # or (enumerated): 0-tag, 1-name, 2-description
                if record and i[0] != k + 1 and i[0] != 0:
                    print("Item tag error:", t[1], i[0], i[1], "should be", k)
                if len(i) != n:
                    print("Item format error:", t[0], t[1], i[1], "-", len(i), "!=", n)
                for o in opts_s2d(i[3]) if n > 3 else []:
                    if o not in ["atfield", "optional", "range"]:
                        print("Invalid field option:", t[0], i[1], o)
            if len(t[4]) != len(tags):
                print("Tag collision", t[0], len(t[4]), "items,", len(tags), "unique tags")
    return jaen


def jaen_load(fname):
    with open(fname) as f:
        jaen = json.load(f)
    jaen_check(jaen)
    return jaen


def jaen_dumps(jaen, level=0, indent=1):
    sp = level * indent * " "
    sp2 = (level + 1) * indent * " "
    if isinstance(jaen, dict):
        sep = ",\n" if level > 0 else ",\n\n"
        lines = []
        for k in sorted(jaen):
            lines.append(sp2 + "\"" + k + "\": " + jaen_dumps(jaen[k], level + 1, indent))
        return "{\n" + sep.join(lines) + "\n" + sp + "}"
    elif isinstance(jaen, list):
        sep = ",\n" if level > 1 else ",\n\n"
        vals = []
        nest = jaen and isinstance(jaen[0], list)
        sp4 = ""
        for v in jaen:
            sp3 = sp2 if nest else ""
            sp4 = sp if v and isinstance(v, list) else ""
            vals.append(sp3 + jaen_dumps(v, level + 1, indent))
        if nest:
            return "[\n" + sep.join(vals) + "]\n"
        return "[" + ", ".join(vals) + sp4 + "]"
    elif isinstance(jaen, (bool, int, str)):
        return json.dumps(jaen)
    return "???"


def jaen_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jaen_dumps(jaen) + "\n")
