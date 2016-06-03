import json

class Codec:

# Settings class attributes
    verbose_record = False  # Record values serialized with string field names if True, else as arrays
    verbose_enum = True     # Enumerated values serialized as name strings.
    case_match = False      # Case-sensitive string matching for field names and enums if True
    _case_produce = 'upper' # Field names and enums capitalization (pass/lower/upper/proper)

    def __init__(self, verbose_record=None, verbose_enum=None, case_match=None, case_produce=None):
        self.vtree = None
        self.extras = []
        if verbose_record is not None:
            self.verbose_record = verbose_record
        if verbose_enum is not None:
            self.verbose_enum = verbose_enum
        if case_match is not None:
            self.case_match = case_match
        if case_produce is not None:
            self.case_produce = case_produce

    def from_json(self, valstr, auto_verbose=True):
        self.vtree = json.loads(valstr)
        if auto_verbose:
            self.verbose_record = isinstance(self.vtree, dict)
        self.decode(self.vtree)

    def _decode_init(self, vtree):
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

class Enumerated(Codec):
    def decode(self, val):
        assert isinstance(val, str), "%r is not a string" % val
        assert val in self.vals, "%s not in %s" % (val, self.vals)
        return val

    def encode(self):
        pass

class VString(Codec):
    def decode(self, val):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTime(Codec):
    def decode(self, val):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTimeInterval(Codec):
    def decode(self, val):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass

class VTimeRecurrence(Codec):
    def decode(self, val):
        assert isinstance(val, str), "%r is not a string" % val
        return val

    def encode(self):
        pass


class Map(Codec):
    def decode(self, vtree):
        self._decode_init(vtree)
        assert isinstance(vtree, dict), \
            "Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+'...')
        return {}

    def encode(self):
        pass

class OrderedMap(Codec):
    def decode(self, vtree):
        pass

    def encode(self):
        pass

class Record(Codec):
    def decode(self, vtree):
        self._decode_init(vtree)
        assert isinstance(vtree, dict if self.verbose_record else list), \
            "%r is not a %s" % (str(vtree)[:20]+'...', 'dict' if self.verbose_record else 'list')
        for n, f in enumerate(self.vals):
            x = f[0] if self.verbose_record else n
#            print('  ', f[0] + ':', self.vtree[x], '#', f[1])
            field = f[1]()
            val = field.decode(vtree[x])
            setattr(self, f[0], val)
        return self

    def encode(self):
        pass
