import json, jsonschema, re
from collections import OrderedDict

class JCodec:
    '''
    Syntax of a JSON Abstract Syntax Notation (JASN) file

    $Namespace: array of [name, URI]
    $Types: datatype definitions:
        Containers: array of [type name, datatype, container options, array of fields]
        Fields: array of [field name, datatype, field options]
        Simple types: array of [type name, datatype, value options]
        Enumerated: array of values
    '''
    jasn_schema = {
        "type": "object",
        "required": ["meta", "types"],
        "additionalProperties": False,
        "properties": {
            "meta": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "description": {"type": "string"},
                    "import": {
                        "type": "object",
                        "patternproperties": {
                            "<uri/uniqueid>": {
                                "type": "array",
                                "items": {"type": "string"}}}},  # [alias, url]
                    "sources": {
                        "type": "object",
                        "additionalProperties": False,
                        "patternProperties": {
                            "^\w+$": {"type": "string"}}}}},
            "types": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": ["array", "string"],
                        "items": {
                            "type": ["array", "string"],
                            "items": {"type": "string"}}}}}}}

    def __init__(self, debug=False, verbose_record=False, verbose_enum=True, case_match=False, case_produce='upper'):
        self.vtree = None
        self.debug = debug
        self.verbose_record = verbose_record
        self.verbose_enum = verbose_enum
        self.case_match = case_match
        self.case_produce = case_produce
        jsonschema.Draft4Validator.check_schema(self.jasn_schema)

    # Validating property setter for case_produce options
    @property
    def case_produce(self):
        return self._case_produce

    @case_produce.setter
    def case_produce(self, value):
        options = ('pass', 'lower', 'upper', 'proper')
        if value.lower() in options:
            self._case_produce = value.lower()
        else:
            raise ValueError("case_produce must be one of: " + str(options))

    def read_jasn(self, fname):
        with open(fname) as f:
            fs = f.read()
        defs = json.loads(fs)
        jsonschema.Draft4Validator(self.jasn_schema).validate(defs)
        return defs

if __name__ == '__main__':
    oc2 = JCodec(case_produce='lower')
    oc2_types = oc2.read_jasn('openc2.jasn')
    for t in oc2_types:
        print(t + ':')
        tdata = oc2_types[t]
        if isinstance(tdata, list):
            for td in tdata:
                print('  ', td)
        else:
            for td, tv in tdata.items():
                print('  ', td + ':', tv)

# TODO: Migrate codec functions from class-based to schema-based

class Codec:

    def from_json(self, valstr, auto_verbose=True):
        self.vtree = json.loads(valstr)
        if auto_verbose:
            Codec.verbose_record = isinstance(self.vtree, dict)
        return self.decode(self.vtree, '')

    def dlog(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def parse_field_opts(self, ostring):
        """
        Parse options included in field definitions of compound datatypes

        Field definitions consist of 1) field name, 2) datatype class, and 3) options string
        Options is a string containing a comma separated list of values.  Return a dict of
        options, including:
        String   Dict key   Dict val  Option
        ------   --------   -------  ------------
        '?'      'optional' Boolean  Field is optional
        '#n'     'choice'   Integer  Field is member of choice group 'n'
        '{key}'  'atfield'  String   Field name of type of an Attribute field
        '[n:m]'  'range'    Tuple    Min and max lengths for arrays and strings
        """
        opts = {'optional':False}
        for o in ostring.split(','):    # TODO: better validation of parse options
            if o == '?':
                opts['optional'] = True
            elif o[:1] == '#':
                opts['choice'] = int(o[1:])
            else:
                m = re.match('{(\w+)}$', o)
                if m:
                    opts['atfield'] = m.group(1)
        return opts

    def printattrs(self, level=0):
        print(type(self))

class VBoolean(Codec):
    def decode(self, val, opts):
        if not isinstance(val, bool):
            print("ValidationError: %r is not boolean" % val)
        return val

    def encode(self):
        pass

class VInteger(Codec):
    def decode(self, val, opts):
        if not isinstance(val, int):
            print("ValidationError: %r is not int" % val)
        return val

    def encode(self):
        pass

class Enumerated(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        ns = self.__module__
        v = val[len(ns)+1:] if val.startswith(ns+':') else val
        assert v in self.vals, "%s: %s not in %s" % (type(self).__name__, v, self.vals)
        return val

    def encode(self):
        pass

class VString(Codec):
    def decode(self, val, opts):
        if not isinstance(val, str):
            print("ValidationError: %r is not a string" % val)
        return val

    def encode(self):
        pass

def check_unknown_fields(self, vtree):
    ft = set(vtree.keys())
    fv = {f[0] for f in self.vals}
    if ft - fv:
        print("ValidationError: %s: unrecognized key %s, should be in %s" % (type(self).__name__, ft - fv, fv))

class Map(Codec):           # TODO: exactly 1 match (choice), undefined values
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict):
            print("Map: Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+'...'))
            return

        check_unknown_fields(self, vtree)
        map = {}
        for n, f in enumerate(self.vals):
            opts = self.parse_field_opts(f[2])
            x = f[0]
            if x in vtree:
                field = f[1]()
                self.dlog('  Map field#', x, type(field).__name__, vtree[x], opts)
                map[x] = field.decode(vtree[x], opts)
            else:
                if not opts['optional']:
                    print("ValidationError: %s: missing Map element '%s' %s" % (type(self).__name__, x, opts))
        return map

    def encode(self):
        pass

class OrderedMap(Codec):
    def decode(self, vtree, opts):
        pass

    def encode(self):
        pass

class Record(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("%r is not a %s" % (str(vtree)[:20]+'...', 'dict' if self.verbose_record else 'list'))
        if isinstance(vtree, dict):
            check_unknown_fields(self, vtree)
#        rec = {f[0]: None for f in self.vals}
        rec = {}
        choice = None
        choicen = 0
        for n, f in enumerate(self.vals):
            fopts = self.parse_field_opts(f[2])
            if 'choice' in fopts and choice == fopts['choice']:
                self.dlog("  Rec Choice: skipping", self.vals[n])
                choicen += 1
                continue
            if self.verbose_record:
                x = f[0]
                exists = x in vtree
            else:
                x = n - choicen
                exists = x < len(vtree) and vtree[x] is not None
            if exists:
                if 'choice' in fopts:
                    choice = fopts['choice']
                field = f[1]()
                if 'atfield' in fopts:
                    fopts['atype'] = rec[fopts['atfield']]
                self.dlog('  Rec Field#', x, type(field).__name__, vtree[x], opts)
                rec[f[0]] = f[1]().decode(vtree[x], fopts)
            else:
                if not fopts['optional']:
                    print("ValidationError: %s: missing Record element '%s' %r" % (type(self).__name__, f[0], opts))
        return rec

    def encode(self):
        pass

class Attribute(Codec):
    """
    Attribute value with external type selector
    """
    def decode(self, vtree, opts):
        self.dlog('Attribute#', type(self).__name__, vtree, opts)
        atype = opts['atype']
        if atype in self.vals:
            cls, copts = self.vals[opts['atype']]
            self.field = cls()
            self.dlog('Attribute:', self, cls, vtree, copts, opts['atype'])
            return self.field.decode(vtree, copts)
        else:
            print("ValidationError: %s: attribute '%s' not in %s" % (type(self).__name__, atype, [k for k in self.vals]))

    def encode(self):
        pass
