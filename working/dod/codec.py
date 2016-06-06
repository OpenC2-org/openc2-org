import json, re

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
        self.decode(self.vtree, '')

    def _decode_init(self, vtree):      # Instance called more than once - encode, decode ?
        self.extras = []

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
        '{key}'  'csfield'  String   Field name of selector used in Choice types
        '[n:m]'  'range'    Tuple    Min and max lengths for arrays and strings
        """
        opts = {'optional':False}
        for o in ostring.split(','):
            if o == '?':
                opts['optional'] = True
            else:
                m = re.match('{(\w+)}$', o)
                if m:
                    opts['csfield'] = m.group(1)
        return opts

    def printattrs(self, level=0):
        print(type(self))

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
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTime(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTimeInterval(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTimeRecurrence(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass


class Map(Codec):
    def decode(self, vtree, opts):
        self._decode_init(vtree)
        assert isinstance(vtree, dict), \
            "Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+'...')
        for k,v in vtree:
            if k in self.vals:      # TODO: check for required properties, or iterate over vals
                setattr(self, k, v)
        return {}

    def encode(self):
        pass

class OrderedMap(Codec):
    def decode(self, vtree, opts):
        pass

    def encode(self):
        pass

class Record(Codec):
    def decode(self, vtree, opts):
        self._decode_init(vtree)
        assert isinstance(vtree, dict if self.verbose_record else list), \
            "%r is not a %s" % (str(vtree)[:20]+'...', 'dict' if self.verbose_record else 'list')
        fx = {}
        for n, f in enumerate(self.vals):
            x = f[0] if self.verbose_record else n
#            print('  ', f[0] + ':', self.vtree[x], '#', f[1])
            field = f[1]()
            fx[f[0]] = field
            opts = self.parse_field_opts(f[2])
            if 'csfield' in opts:
                opts['csel'] = getattr(self, opts['csfield'])
            try:
                val = field.decode(vtree[x], opts)
                setattr(self, f[0], val)
            except KeyError:
                if not opts['optional']:
                    print("%s: missing field '%s'" % (type(self).__name__, f[0]))
                setattr(self, f[0], None)
        return self

    def encode(self):
        pass

class Choice(Codec):
    def decode(self, vtree, opts):
        self._decode_init(vtree)
        cls, copts = self.vals[opts['csel']]
        print('Choice:', self, cls, vtree, copts, opts['csel'])
        val = cls().decode(vtree, copts)
        setattr(self, 'value', val)
        return self

    def encode(self):
        pass