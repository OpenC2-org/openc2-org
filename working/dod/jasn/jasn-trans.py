import json, jsonschema, re

jasn_schema = """
{   "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": false,
    "properties": {
        "meta": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "targetNamespace": {
                    "type": "array",
                    "additionalitems": false,
                    "items": [
                        {"type": "string"},
                        {"type": "string"}
                    ]
                },
                "version": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "root": {"type": "string"},
                "import": {
                    "type": "object",
                    "additionalProperties": false,
                    "patternProperties": {
                        "<uri/uniqueid>": {
                            "type": "array",
                            "items": {"type": "string"}}}},
                "sources": {
                    "type": "object",
                    "additionalProperties": false,
                    "patternProperties": {
                        "^\\w+$": {"type": "string"}}}}},
        "types": {
            "type": "array",
            "items": [
                {"type": "string"},
                {"type": "string"},
                {"type": "string"},
                {"type": "array",
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
            }]
        }
    }
}
"""