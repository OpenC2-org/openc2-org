"""
Support functions for JAEN codec
  Convert dict between nested and flat
  Convert typedef options between dict and strings
"""

from functools import reduce

# Dict conversion utilities

def _dmerge(x, y):
    k, v = next(iter(y.items()))
    if k in x:
        _dmerge(x[k], v)
    else:
        x[k] = v
    return x


def hdict(keys, value, sep="."):
    """
    Convert a hierarchical-key value pair to a nested dict
    """
    return reduce(lambda v, k: {k: v}, reversed(keys.split(sep)), value)


def fluff(src, sep="."):
    """
    Convert a flat dict with hierarchical keys to a nested dict

    :param src: flat dict - e.g., {"a.b.c": 1, "a.b.d": 2}
    :param sep: separator character for keys
    :return: nested dict - e.g., {"a": {"b": {"c": 1, "d": 2}}}
    """
    return reduce(lambda x, y: _dmerge(x, y), [hdict(k, v, sep) for k, v in src.items()], {})


def flatten(cmd, path="", fc={}, sep="."):
    """
    Convert a nested dict to a flat dict with hierarchical keys
    """
    fcmd = fc.copy()
    if isinstance(cmd, dict):
        for k, v in cmd.items():
            k = k.split(":")[1] if ":" in k else k
            fcmd = flatten(v, sep.join((path, k)) if path else k, fcmd)
    else:
        fcmd[path] = ('"' + cmd + '"' if isinstance(cmd, str) else str(cmd))
    return (fcmd)


# Option conversions

def opts_s2d(ostr):
    """
    Convert list of type definition option strings to options dictionary

    String   Dict key   Dict val  Option
    ------   --------   -------  ------------
    "?"      "optional" Boolean  Field is optional
    "{key"   "atfield"  String   Field name of Attribute type
    "[n:m"   "range"    Tuple    Min and max lengths for arrays and strings
    ">*"     "pattern"  String   Regular expression to match against String value
    """

    assert isinstance(ostr, (list, tuple)), "%r is not a list" % olist
    opts = {"optional": False}
    for o in ostr:
        if o[0] == "?":
            opts["optional"] = True
        elif o[0] == "{":
            opts["atfield"] = o[1:]
        elif o[0] == "[":
            opts["range"] = (0,0)       # TODO: do it
        elif o[0] == ">":
            opts["pattern"] = o[1:]
        else:
            print("Unknown option '", o, "'")
    return opts


def opts_d2s(opts):
    """
    Convert options dictionary to list of option strings
    """
    ostr = []
    for k, v in opts.items():
        if k == "optional" and v:
            ostr.append("?")
        elif k == "atfield":
            ostr.append("{" + v)
        elif k == "range":
            ostr.append("[" + str(v[0]) + ":" + str(v[1]))
        elif k == "pattern":
            ostr.append(">" + v)
        else:
            print("Unknown option '", o, "'")
    return ostr
