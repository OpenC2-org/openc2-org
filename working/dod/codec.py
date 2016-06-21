import json, re

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
        if hasattr(self, 'vals'):
            assert(isinstance(self.vals, list) and isinstance(self.vals[0], (tuple, str)))
            if isinstance(self.vals[0], tuple):
                self._fields = [self._ns + ':' + f[0] if hasattr(self, '_ns') else f[0] for f in self.vals]
            else:
                self._fields = [self._ns + ':' + f if hasattr(self, '_ns') else f for f in self.vals]
            if not Codec.case_match:
                self._fields = [f.lower() for f in self._fields]
            self._fx = {v:n for n, v in enumerate(self._fields)}
        print("init: %s %d %s" % (type(self).__name__, len(self.vals), self._fx))

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
        Parse options included in field definitions of compound datatypes

        Field definitions consist of 1) field name, 2) datatype class, and 3) options string
        Options is a string containing a comma separated list of values.  Return a dict of
        options, including:
        String   Dict key   Dict val  Option
        ------   --------   -------  ------------
        '?'      'optional' Boolean  Field is optional, equivalent to [0:1]
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

    def to_match(self, d):
        return d if self.case_match else {k.lower():v for k,v in d.items()}

    def check_unknown_fields(self, vtree):
        ft = set(self.to_match(vtree))
        if hasattr(self, '_ns'):
            ft = {f if ':' in f else self._ns + ':' + f for f in ft}
        fv = set(self._fields)
        if ft - fv:
            print("ValidationError: %s: unrecognized key %s, should be in %s" % (type(self).__name__, ft - fv, fv))
        return ft

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
        v = val if ':' in val else self._ns + ':' + val
        v = v if self.case_match else v.lower()
        assert v in self._fields, "%s: %s not in %s" % (type(self).__name__, v, self._fields)
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

class Map(Codec):           # TODO: exactly 1 match (choice), undefined values
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict):
            print("Map: Expected dict, got %s (%r)" % (type(self.vtree), str(self.vtree)[:20]+'...'))
            return

        self.check_unknown_fields(vtree)
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
            self.check_unknown_fields(vtree)
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
                x = self._fields[n]
                vt = self.to_match(vtree)
                if hasattr(self, '_ns'):
                    vt = {(k if ':' in k else self._ns + ':' + k):v for k,v in vt.items()}
                exists = x in vt
#                print("Record:", exists, n, f[0], x, vt)
            else:
                x = n - choicen
                vt = vtree
                exists = x < len(vt) and vt[x] is not None
            if exists:
                if 'choice' in fopts:
                    choice = fopts['choice']
                field = f[1]()
                if 'atfield' in fopts:
                    fopts['atype'] = rec[fopts['atfield']]
                self.dlog('  Rec Field#', x, type(field).__name__, vt[x], opts)
                rec[f[0]] = f[1]().decode(vt[x], fopts)
            else:
                if not fopts['optional']:
                    print("ValidationError: %s: missing Record element '%s' %r" % (type(self).__name__, f[0], opts))
        return rec

    def encode(self):
        pass

class Choice(Codec):
    def decode(self, vtree, opts):
        if not isinstance(vtree, dict if self.verbose_record else list):
            print("ValidationError: %r is not a %s" % (str(vtree)[:20] + '...', 'dict' if self.verbose_record else 'list'))
        if isinstance(vtree, dict) and len(vtree) == 1:
            field = next(iter(self.check_unknown_fields(vtree)))
        elif len(vtree) == 2:
            field = vtree[0]
        else:
            print("ValidationError: %s: bad choice %s" % (type(self).__name__, field))
        print("Choice:", field, self._fx)
        return {field: self.vals[self._fx[field]][1]().decode(vtree[next(iter(vtree))], '')}

    def encode(self):
        pass

class Attribute(Codec):
    """
    Attribute value with external type selector
    """
    def decode(self, vtree, opts):
        self.dlog('Attribute#', type(self).__name__, vtree, opts)
        atype = opts['atype']       # TODO: ns/case,
        if atype in self._fields:
            field, cls, copts = self.vals[self._fx[atype]]
            self.field = cls()
            self.dlog('Attribute:', self, cls, vtree, copts, opts['atype'])
            return self.field.decode(vtree, copts)
        else:
            print("ValidationError: %s: attribute '%s' not in %s" % (type(self).__name__, atype, self._fields))

    def encode(self):
        pass
