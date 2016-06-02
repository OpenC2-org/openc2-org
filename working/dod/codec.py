import json

class Codec:

    def __init__(self, json_v=None):
        self.vtree = None
        self.json_v = json_v

    def from_json(self, valstr):
        vtree = json.loads(valstr)
        self.json_v = isinstance(vtree, dict)
        self.decode(vtree)

    def _decode_base(self, vtree):
        self.vtree = vtree

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
        assert(isinstance(self.vtree, dict if self.json_v else list))
        for n, f in enumerate(self.vals):
            x = f[0] if self.json_v else n
#            print('  ', f[0] + ':', self.vtree[x], '#', f[2])
            inst = f[2](json_v=self.json_v)
            val = inst.decode(self.vtree[x])
            setattr(self, f[0], val)
        return self

    def encode(self):
        pass
