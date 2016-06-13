import json, os
from lxml import etree

xs = '{http://www.w3.org/2001/XMLSchema}'
jmeta = {}
jtypes = []
schemadir = 'data'
files = ['Address_Object.xsd']
for ifile in files:
    with open(os.path.join(schemadir, ifile)) as f:
        tree = etree.parse(f)
    schema = tree.getroot()
    atts = dict(schema.items())
    jmeta['targetNamespace'] = atts['targetNamespace']
    jmeta['version'] = atts['version']

    for el in tree.getroot():
        tag = str(el.tag).replace(xs, '')
        atts = dict(el.items())
        text = el.text.strip() if el.text else ''
        if tag == 'element':
            pass
        elif tag == 'import':
            pass
        elif tag == 'simpleType':
            pass
        elif tag == 'complexType':
            pass
        elif tag == 'annotation':
            pass
        elif tag == 'attributeGroup':
            pass
        else:
            print('ParseError: Unknown tag:', tag)
        if text:
            print('ParseError: Unexpected text:', text)

    jasn = {"meta": jmeta, "types": jtypes}
    print(json.dumps(jasn, indent=2))
