import json

class Codec:

# Settings class attributes
    verbose_record = False  # Record values serialized with string field names if True, else as arrays
    verbose_enum = True     # Enumerated values serialized as name strings.
    case_match = False      # Case-sensitive string matching for field names and enums if True
    _case_produce = 'upper' # Field names and enums serialized as given ('pass'), as lower, or as upper

    def __init__(self, verbose_record=None, verbose_enum=None, case_match=None, case_produce=None):
        self.vtree = None
        if verbose_record is not None:
            self.verbose_record = verbose_record
        if verbose_enum is not None:
            self.verbose_enum = verbose_enum
        if case_match is not None:
            self.case_match = case_match
        if case_produce is not None:
            self.case_produce = case_produce

    def from_json(self, valstr, auto_verbose=True):
        vtree = json.loads(valstr)
        if auto_verbose:
            self.verbose_record = isinstance(vtree, dict)
        self.decode(vtree)

    def _decode_base(self, vtree):
        self.vtree = vtree

# Validating property setter for case_produce options
    @property
    def case_produce(self):
        return self._case_produce

    @case_produce.setter
    def case_produce(self, value):
        options = ('pass', 'lower', 'upper')
        if value.lower() in options:
            self._case_produce = value.lower()
        else:
            raise ValueError("case_produce must be one of: " + str(options))

class Enumerated(Codec):
    def decode(self, val):
        assert(isinstance(val, str))
        assert(val in self.vals)
        return val

    def encode(self):
        pass

class VString(Codec):
    def decode(self, val):
        assert(isinstance(val, str))
        return val

    def encode(self):
        pass

class VTime(Codec):
    def decode(self, val):
        assert(isinstance(val, str))
        return val

    def encode(self):
        pass

class VTimeInterval(Codec):
    def decode(self, val):
        assert(isinstance(val, str))
        return val

    def encode(self):
        pass

class VTimeRecurrence(Codec):
    def decode(self, val):
        assert(isinstance(val, str))
        return val

    def encode(self):
        pass


class Map(Codec):
    def decode(self, vtree):
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
        self._decode_base(vtree)
        assert isinstance(self.vtree, dict if self.verbose_record else list), \
            "%r is not a %s" % (str(self.vtree)[:10]+'..', 'dict' if self.verbose_record else 'list')
        for n, f in enumerate(self.vals):
            x = f[0] if self.verbose_record else n
#            print('  ', f[0] + ':', self.vtree[x], '#', f[2])
            field = f[2]()
            val = field.decode(self.vtree[x])
            setattr(self, f[0], val)
        return self

    def encode(self):
        pass
