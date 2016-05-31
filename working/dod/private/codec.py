import inspect, json

class Codec:
    ttab = {
        'record': [decode_record, encode_record],
        'map':    [decode_map,    encode_map],
        'string': [decode_string, encode_string],
        'time':   [decode_time,   encode_time],
        'timeinterval': [decode_timeinterval, encode_timeinterval],
    }

    def __init__(self):
        self.vtree = None
        self.json_v = False

    def decode_record(self):
        for n, f in enumerate(self.vals):
            x = f[0] if self.json_v else n
            print('  ', f[0] + ':', self.vtree[x])
            setattr(self, f[0], f[2](self.vtree[x]))
        pass

    def encode_record(self):
        pass

    def decode_map(self):
        pass

    def encode_map(self):
        pass

    def decode_string(self):
        assert(isinstance(val, str))
        return val

    def encode_string(self):
        pass

    def decode_time(self):
        assert(isinstance(val, str))
        return val

    def encode_time(self):
        pass

    def decode_vtimeinterval(self):
        assert(isinstance(val, str))
        return val

    def encode_timeinterval(self):
        pass

    def from_json(self, valstr):
        self.vtree = json.loads(valstr)
        self.json_v = isinstance(self.vtree, dict)
        self.decode()

    def decode(self):
        print('Decode: vtree =', self.vtree)
        print(type(self).__name__ + ':', self.type + '[' + ','.join([f[0] for f in self.vals]) + ']')
        ttab(self.type)[0]()       # run selected decoder
