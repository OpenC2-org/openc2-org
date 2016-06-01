import json

class Codec:

    def __init__(self):
        self.vtree = None
        self.json_v = False
        self.inst = []

    def from_json(self, valstr):
        vtree = json.loads(valstr)
        self.json_v = isinstance(vtree, dict)
        self.decode(vtree)

    def _decode_base(self, vtree):
        self.vtree = vtree
        print('Decode: vtree =', self.vtree)
        print(type(self).__name__ + ': [' + ','.join([f[0] for f in self.vals]) + ']')


class VString(Codec):
    def decode(self, vval):
        assert (isinstance(vval, str))
        return vval

    def encode(self):
        pass

class VTime(Codec):
    def decode(self, val):
        assert (isinstance(val, str))
        return val

    def encode(self):
        pass

class VTimeInterval(Codec):
    def decode(self, val):
        assert (isinstance(val, str))
        return val

    def encode(self):
        pass

class Map(Codec):
    def decode(self):
        pass

    def encode(self):
        pass

class OrderedMap(Codec):
    def decode(self):
        pass

    def encode(self):
        pass

class Record(Codec):
    def decode(self, vtree):
        self._decode_base(vtree)
        assert(isinstance(self.vtree, dict if self.json_v else list))
        for n, f in enumerate(self.vals):
            x = f[0] if self.json_v else n
            print('  ', f[0] + ':', self.vtree[x], '#', f[2])
            i = f[2]()
            self.inst.append(i)
            val = i.decode(self.vtree[x])
            if val:
                setattr(self, f[0], val)

    def encode(self):
        pass
