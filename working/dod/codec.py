import json, re
from collections import OrderedDict

class Codec:

# Class attributes for settings
    verbose_record = False  # Record values serialized with string field names if True, else as arrays
    verbose_enum = True     # Enumerated values serialized as name strings.
    case_match = False      # Case-sensitive string matching for field names and enums if True
    _case_produce = 'upper' # Field names and enums capitalization (pass/lower/upper/proper)

    def __init__(self, verbose_record=None, verbose_enum=None, case_match=None, case_produce=None):
        self.vtree = None
        self.extras = []
        if verbose_record is not None:
            Codec.verbose_record = verbose_record
        if verbose_enum is not None:
            Codec.verbose_enum = verbose_enum
        if case_match is not None:
            Codec.case_match = case_match
        if case_produce is not None:
            Codec.case_produce = case_produce

    def from_json(self, valstr, auto_verbose=True):
        self.vtree = json.loads(valstr)
        if auto_verbose:
            Codec.verbose_record = isinstance(self.vtree, dict)
        return self.decode(self.vtree, '')

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

    def parse_field_opts(self, ostring):
        """
        Parse options included in field definitions of compound datatypes

        Field definitions consist of 1) field name, 2) datatype class, and 3) options string
        Options is a string containing a comma separated list of values.  Return a dict of
        options, including:
        String   Dict key   Dict val  Option
        ------   --------   -------  ------------
        '?'      'optional' Boolean  Field is optional
        '{key}'  'atfield'  String   Field name of type of an Attribute field
        '[n:m]'  'range'    Tuple    Min and max lengths for arrays and strings
        """
        opts = {'optional':False}
        for o in ostring.split(','):
            if o == '?':
                opts['optional'] = True
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
                print('  Map field#', x, type(field).__name__, vtree[x], opts)
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
        for n, f in enumerate(self.vals):
            fopts = self.parse_field_opts(f[2])
            if self.verbose_record:
                x = f[0]
                exists = x in vtree
            else:
                x = n
                exists = x < len(vtree) and vtree[x] is not None
            if exists:
                field = f[1]()
                if 'atfield' in fopts:
                    fopts['atype'] = rec[fopts['atfield']]
                print('  Rec Field#', x, type(field).__name__, vtree[x], opts)
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
        print('Attribute#', type(self).__name__, vtree, opts)
        atype = opts['atype']
        if atype in self.vals:
            cls, copts = self.vals[opts['atype']]
            self.field = cls()
            print('Attribute:', self, cls, vtree, copts, opts['atype'])
            return self.field.decode(vtree, copts)
        else:
            print("ValidationError: %s: attribute '%s' not in %s" % (type(self).__name__, atype, [k for k in self.vals]))

    def encode(self):
        pass
