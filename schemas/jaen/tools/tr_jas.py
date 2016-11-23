"""
Translate JAEN to and from JAS (JAEN Abstract Syntax)
"""

import re
import jas_parse
from copy import deepcopy
from datetime import datetime
from codec_utils import opts_s2d, opts_d2s
from textwrap import fill, shorten


class Jastype:

    def __init__(self):
        types = [
            ("Attribute", "ATTRIBUTE"),
            ("Array", "ARRAY"),
            ("Choice", "CHOICE"),
            ("Enumerated", "ENUMERATED"),
            ("Map", "MAP"),
            ("Record", "RECORD"),
            ("Boolean", "BOOLEAN"),
            ("Integer", "INTEGER"),
            ("Number", "REAL"),
            ("String", "UTF8String")
        ]
        self._ptype = {t[0].lower(): t[1] for t in types}
        self._jtype = {t[1].lower(): t[0] for t in types}

    def ptype(self, jt):
        t = jt.lower()
        return self._ptype[t] if t in self._ptype else jt

    def jtype(self, pt):
        t = pt.lower()
        return self._jtype[t] if t in self._jtype else pt


def _parse_import(import_str):
    tag, ns, uid = re.match("(\d+),\s*(\w+),\s*(.+)$", import_str).groups()
    return [int(tag), ns, uid]


def _nstr(v):       # Return empty string if None
    return v if v else ""


def _fopts(v):      # TODO: process min/max/range option
    opts = {}
    for o in v if v else []:
        if isinstance(o, str) and o.lower() == "optional":
            opts.update({"optional": True})
        elif isinstance(o, list) and o[0] == ".&":
            opts.update({"atfield": o[1]})
        elif isinstance(o, list) and o[0].lower() == "pattern":
            opts.update({"pattern": "".join(o[1])})
        else:
            print("Unknown field option", o, v)
    return opts_d2s(opts)


def jas_loads(jas_str):
    """
    Load abstract syntax from JAS file
    """

    parser = jas_parse.jasParser(parseinfo=True, )

    ast = parser.parse(jas_str, 'jas', trace=False)
    meta = {}
    for m in ast["metas"]:
        k = m["key"]
        if k.lower() == "import":
            meta[k] = [[int(x), y.strip(), z.strip()] for x, y, z in (s.split(",") for s in m["val"])]
        else:
            meta[k] = " ".join(m["val"])

    pt = Jastype()
    types = []
    for t in ast["types"]:
        fields = []
        tdesc = t["td1"]
        if t["f"]:
            tdesc = t["f"]["td2"] if t["f"]["td2"] else tdesc
            tf = t["f"]["fields"]
            for n in range(len(tf)-1):          # shift field descriptions up to corresponding fields
                tf[n]["fd2"] = tf[n+1]["fd1"]
            for n, f in enumerate(t["f"]["fields"]):
                fdesc = f["fd2"]
                if t["type"].lower() == "record":
                    tag = n + 1
                elif isinstance(f["tag"], str):
                    tag = int(f["tag"])
                else:
                    print("Error: missing tag", t["name"], f["name"])
                if tag:
                    if t["type"].lower() == "enumerated":
                        fields.append([tag, f["name"], _nstr(fdesc)])
                    else:
                        fields.append([tag, f["name"], pt.jtype(f["type"]), _fopts(f["fopts"]), _nstr(fdesc)])
        tdef = [t["name"], pt.jtype(t["type"]), _fopts(t["topts"]), _nstr(tdesc)]
        types.append(tdef + [fields] if tdef[1] not in ["String", "Integer", "Number", "Boolean"] else tdef)
    jaen = {"meta": meta, "types": types}
    return jaen


def jas_load(fname):
    with open(fname) as f:
        return jas_loads(f.read())


def jas_dumps(jaen):
    """
    Produce JAS module from JAEN structure

    JAS represents features available in both jaen and ASN.1 using ASN.1 syntax, but creates
    extended datatypes (Record, Map, Attribute) for JAEN types not directly representable in ASN.1.
    With appropriate encoding rules (which do not yet exist), SEQUENCE could replace Record.  Map and
    Attribute could be implemented using ASN.1 table constraints, but for the purpose of representing
    JSON objects, the Map and Attribute first-class types in JAS are easier to use.
    """

    jas = "/*\n"
    hdrs = jaen["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import"]
    for h in hdr_list + list(set(hdrs) - set(hdr_list)):
        if h in hdrs:
            if h == "description":
                jas += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h+":"), subsequent_indent=15*" ") + "\n"
            elif h == "import":
                hh = "{:14} ".format(h+":")
                for imp in hdrs[h]:
                    jas += hh + "{0:d}, {1}, {2}\n".format(*imp)
                    hh = 15*" "
            else:
                jas += "{0:14} {1:}\n".format(h+":", hdrs[h])
    jas += "*/\n"

    pt = Jastype()
    for td in jaen["types"]:                    # 0:name, 1:type, 2:topts, 3:tdesc, 4:fields
        tname, ttype = td[0:2]
        topts = opts_s2d(td[2])
        tostr = '(PATTERN "' + topts["pattern"] + '")' if "pattern" in topts else ""
        tdesc = "    -- " + td[3] if td[3] else ""
        jas += "\n" + tname + " ::= " + pt.ptype(ttype) + tostr
        if len(td) > 4:
            titems = deepcopy(td[4])
            for n, i in enumerate(titems):      # 0:id, 1:name, 2:fdesc  (enumerated), or
                if len(i) > 3:                  # 0:id, 1:name, 2:type, 3: fopts, 4:fdesc
                    desc = i[4]
                    i[2] = pt.ptype(i[2])
                else:
                    desc = i[2]
                desc = "    -- " + desc if desc else ""
                i.append("," + desc if n < len(titems) - 1 else (" " + desc if desc else ""))
            flen = min(32, max(12, max([len(i[1]) for i in titems]) + 1 if titems else 0))
            jas += " {" + tdesc + "\n"
            if ttype.lower() == "enumerated":
                fmt = "    {1:" + str(flen) + "} ({0:d}){3}"
                jas += "\n".join([fmt.format(*i) for i in titems])
            else:
                fmt = "    {1:" + str(flen) + "} [{0:d}] {2}{3}{4}"
                if ttype.lower() == 'record':
                    fmt = "    {1:" + str(flen) + "} {2}{3}{4}"
                items = []
                for n, i in enumerate(titems):
                    ostr = ""
                    opts = opts_s2d(i[3])
                    if "atfield" in opts:
                        ostr += ".&" + opts["atfield"]
                        del opts["atfield"]
                    if opts["optional"]:
                        ostr += " OPTIONAL"
                    del opts["optional"]
                    items += [fmt.format(i[0], i[1], i[2], ostr, i[5]) + (" ***" + str(opts) if opts else "")]
                jas += "\n".join(items)
            jas += "\n}\n" if titems else "}\n"
        else:
            jas += tdesc + "\n"
    return jas


def jas_dump(jaen, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(jas_dumps(jaen))
