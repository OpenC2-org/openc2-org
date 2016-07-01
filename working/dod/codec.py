import json, re

# TODO: replace error messages with ValidationError exceptions
# TODO: parse field options at initialization

class Codec:

# Class attributes for settings
    verbose_record = False  # Record values serialized with string field names if True, else as arrays
    verbose_enum = True     # Enumerated values serialized as name strings.
    case_match = False      # Case-sensitive string matching for field names and enums if True
    _case_produce = 'upper' # Field names and enums capitalization (pass/lower/upper/proper)

    def __init__(self, debug=False, verbose_record=None, verbose_enum=None, case_match=None, case_produce=None):
        self.vtree = None
        self.debug = debug
        if verbose_record is not None:
            Codec.verbose_record = verbose_record
        if verbose_enum is not None:
            Codec.verbose_enum = verbose_enum
        if case_match is not None:
            Codec.case_match = case_match
        if case_produce is not None:
            Codec.case_produce = case_produce
        if hasattr(self, 'ns'):
            self._ns = self.ns if Codec.case_match else self.ns.lower()
        if hasattr(self, 'vals') and self.vals:
            assert(isinstance(self.vals, list) and isinstance(self.vals[0], (tuple, str)))
            ns = self._ns + ':' if hasattr(self, '_ns') else ''
            if isinstance(self.vals[0], tuple):
                self._fields = [f[0] if ':' in f[0] else ns + f[0] for f in self.vals]
            else:
                self._fields = [f if ':' in f else ns + f for f in self.vals]
            if not Codec.case_match:
                self._fields = [f.lower() for f in self._fields]
            self._fx = {v:n for n, v in enumerate(self._fields)}
            self.dlog("init: %s %d %s" % (type(self).__name__, len(self.vals), self._fx))
        else:
            self.dlog("init: %s" % (type(self).__name__))

    def from_json(self, valstr, auto_verbose=True):
        self.vtree = json.loads(valstr)
        if auto_verbose:
            Codec.verbose_record = isinstance(self.vtree, dict)
        return self.decode(self.vtree, '')

    def dlog(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

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
        Parse options included in field definitions

        Field definitions consist of 1) field name, 2) datatype class, and 3) options string
        Ostring contains a comma separated list of values.  Return a dict of options, including:
        String   Dict key   Dict val  Option
        ------   --------   -------  ------------
        '?'      'optional' Boolean  Field is optional, equivalent to [0:1]
        '#'      'choice'   Boolean  Field is a Choice type
        '{key}'  'atfield'  String   Field name of type of an Attribute field
        '[n:m]'  'range'    Tuple    Min and max lengths for arrays and strings
        """
        opts = {'optional':False, 'choice': False}
        for o in ostring.split(','):    # TODO: better validation of parse options
            if o == '?':
                opts['optional'] = True
            elif o[:1] == '#':
                opts['choice'] = True
            else:
                m = re.match('{(\w+)}$', o)
                if m:
                    opts['atfield'] = m.group(1)
        return opts

    def printattrs(self, level=0):
        print(type(self))

    def fmap(self, v):
        fv = v if self.case_match else v.lower()
        return fv if ':' in fv else self._ns + ':' + fv

    def normalize_fields(self, vtree):
        """
        Normalize field names to lower case and explicit namespace
        """
        nfields = {}
        if isinstance(vtree, dict):
            nfields = {self.fmap(k):k for k in vtree}
        elif isinstance(vtree, str):
            nfields = {self.fmap(vtree):vtree}
        return nfields

    def check_fields(self, nfields):
        '''
        Check decoded normalized field names against class fields
        '''
        if isinstance(nfields, dict):
            nf = set(nfields)
            cf = set(self._fields)
            if nf - cf:
                print("ValidationError: %s: Unrecognized var %s, should be in %s" % (type(self).__name__, nf - cf, cf))

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

class VString(Codec):
    def decode(self, val, opts):
        if not isinstance(val, str):
            print("ValidationError: %r is not a string" % val)
        return val

    def encode(self):
        pass

class Enumerated(Codec):
    def decode(self, val, opts):
        assert isinstance(val, str), "%r is not a string" % val
        ns = self.__module__
        v = val if ':' in val else self._ns + ':' + val
        v = v if self.case_match else v.lower()
        assert v in self._fields, "%s: %s not in %s" % (type(self).__name__, v, self._fields)
        return val

    def encode(self):
        pass

class Map(Codec):           # TODO: exactly 1 match (choice), undefined values
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict):
            print("Map: Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+'...'))
            return

        nfields = self.normalize_fields(vtree)
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

class Record(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("%r is not a %s" % (str(vtree)[:20]+'...', 'dict' if self.verbose_record else 'list'))
        nfields = self.normalize_fields(vtree)
        rec = {}
        for n, f in enumerate(self.vals):
            fopts = self.parse_field_opts(f[2])
            if self.verbose_record:
                x = self._fields[n]
                exists = x in nfields or fopts['choice']
            else:
                x = n
                exists = n < len(vtree) and vtree[n] is not None
            if exists:
                field = f[1]()
                if 'atfield' in fopts:
                    fopts['atype'] = rec[fopts['atfield']]
                if fopts['choice']:
                    rec = field.decode(vtree, fopts)
                else:
                    x = x if isinstance(x, int) else nfields[x]
                    rec[f[0]] = field.decode(vtree[x], fopts)
            else:
                if not fopts['optional'] and not fopts['choice']:       # TODO: fix field name check for choice (*)
                    print("ValidationError: %s: missing Record element '%s' %r" % (type(self).__name__, f[0], opts))
        self.check_fields(nfields)
        return rec

    def encode(self):
        pass

class Choice(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("ValidationError: %r is not a %s" % (str(vtree)[:20] + '...', 'dict' if self.verbose_record else 'list'))
        if isinstance(vtree, dict):
            nfields = self.normalize_fields(vtree)
            nf = set(self._fields) & set(nfields)
            if len(nf) != 1:
                print("ValidationError: %s Choice should match one element: $s" % (type(self).__name__, nf))
            nf = next(iter(nf))
            val = vtree[nfields[nf]]
        elif isinstance(vtree, list) and len(vtree) == 2:
            nf = next(iter(self.normalize_fields(vtree[0])))
            val = vtree[1]
        else:
            print("ValidationError: %s: bad choice %s: %s" % (type(self).__name__, type(vtree), vtree))
            return
        self.dlog("Choice:", nf + "[" + str(self._fx[nf]+1) + "]", val)
        return {nf: self.vals[self._fx[nf]][1]().decode(val, '')}

    def encode(self):
        pass

class Attribute(Codec):
    """
    Attribute value with external type selector
    """
    def decode(self, vtree, opts):
        self.dlog('Attribute#', type(self).__name__, vtree, opts)
        atype = next(iter(self.normalize_fields(opts['atype'])))
        if atype in self._fields:
            field, cls, copts = self.vals[self._fx[atype]]
            self.field = cls()
            self.dlog('Attribute:', self, cls, vtree, copts, opts['atype'])
            return self.field.decode(vtree, copts)
        else:
            print("ValidationError: %s: attribute '%s' not in %s" % (type(self).__name__, atype, self._fields))

    def encode(self):
        pass
