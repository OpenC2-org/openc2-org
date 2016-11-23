"""
Translate JAEN to property tables (xlsx format)
"""

import xlsxwriter
from codec_utils import opts_s2d
from datetime import datetime


def _set_col_widths(sheet, col, widths):
    for n, w in enumerate(widths):
        sheet.set_column(col+n, col+n, w)

def _write_type(sheet, row, col, ncols, tname, tval, fmt):
    sheet.write(row, col, tname, fmt[0])
    sheet.merge_range(row, col + 1, row, col + ncols, tval, fmt[1])
    return 1

def _write_row(sheet, row, col, values, format):
    for n, v in enumerate(values):
        sheet.write(row, col + n, v, format)

def _write_field(sheet, row, col, f, fmt, tname = "", btype = ""):
    req = ""
    if tname in ["Record", "Map"]:
        opts = opts_s2d(f[3])
        req = " (optional)" if opts["optional"] else " (required)"
    btype = " (" + btype + ")" if btype else ""
    sheet.write(row, col, f[0], fmt)
    sheet.write(row, col + 1, f[1] + req, fmt)
    sheet.write(row, col + 2, f[2] + btype, fmt)
    if len(f) > 4:
        sheet.write(row, col + 3, f[4], fmt)
    return 1

def table_dump(jaen, fname, source=""):
    wkbook = xlsxwriter.Workbook(fname)
    sheet_meta = wkbook.add_worksheet("Meta")
    sheet_types = wkbook.add_worksheet("Types")
    sheet_vocab = wkbook.add_worksheet("Vocab")

    fgen = wkbook.add_format({"font_name": "consolas", "font_size": 10})
    mkey = wkbook.add_format({"valign": "vcenter", "bold": True, "bg_color": "#ffeedd", "border": 1})
    mval = wkbook.add_format({"valign": "vcenter", "text_wrap": True, "bg_color": "#ffeedd", "border": 1})
    thead = wkbook.add_format({"align": "center", "bold": True, "bg_color": "#303090", "font_color": "white", "border": 1})
    tdname = wkbook.add_format({"bold": True})
    tdval1 = wkbook.add_format({"bg_color": "#d0d8ff"})
    tdval = wkbook.add_format({})
    tdfield = wkbook.add_format({"text_wrap": True, "valign": "top", "border": 1})

    # Generate configuration information page from meta fields

    if source:
        sheet_meta.write(1, 1, "Generated from " + source + ", " + datetime.ctime(datetime.now()), fgen)
    row, col = 3, 1
    sheet_meta.set_column(1, 1, 15)
    sheet_meta.set_column(2, 2, 60)
    hdrs = jaen["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import"]
    for n, h in enumerate(hdr_list + list(set(hdrs) - set(hdr_list))):
        if h in hdrs:
            sheet_meta.write(row + n, col, h, mkey)
            if h == "import":
                val = "\n".join(["{0:d}:{1:s} - {2:s}".format(*k) for k in hdrs[h]])
            elif isinstance(hdrs[h], (int, str, bool)):
                val = hdrs[h]
            else:
                val = "???"
            sheet_meta.write(row + n, col + 1, val, mval)

    # Generate property tables from type definitions

    trow, tcol = 1, 1
    vrow, vcol = 1, 1
    _set_col_widths(sheet_types, 0, [12, 4, 20, 20, 50])
    _set_col_widths(sheet_vocab, 0, [12, 4, 20, 70])
    fmt = [tdname, tdval]
    fmt1 = [tdname, tdval1]
    symtab = {t[0]:t[1] for t in jaen["types"]}
    for n, t in enumerate(jaen["types"]):   # 0: type name, 1: base type, 2:opts, 3: desc, 4:fields
        if t[1] == "Enumerated":
            vrow += _write_type(sheet_vocab, vrow, 0, 3, "Vocabulary:", t[0], fmt1)
            if t[2]:
                vrow += _write_type(sheet_vocab, vrow, 0, 3, "Options:", t[2], fmt)
            if t[3]:
                vrow += _write_type(sheet_vocab, vrow, 0, 3, "Description:", t[3], fmt)
            _write_row(sheet_vocab, vrow + 1, vcol, ["Id", "Value", "Description"], thead)
            vrow += 2
            for nf, f in enumerate(t[4]):
                vrow += _write_field(sheet_vocab, vrow, vcol, f, tdfield)
            vrow += 1
        else:
            trow += _write_type(sheet_types, trow, 0, 4, "Type Name:", t[0], fmt1)
            trow += _write_type(sheet_types, trow, 0, 4, "Type:", t[1], fmt)
            if t[2]:
                opts = opts_s2d(t[2])
                del(opts["optional"])
                optsd = ", ".join([k + ': "' + v + '"' for k,v in opts.items()])
                trow += _write_type(sheet_types, trow, 0, 4, "Options:", optsd, fmt)
            if t[3]:
                trow += _write_type(sheet_types, trow, 0, 4, "Description:", t[3], fmt)
            if t[1] in ["Attribute", "Choice", "Map", "Record"]:
                _write_row(sheet_types, trow + 1, tcol, ["Id", "Name", "Type", "Description"], thead)
                trow += 2
            if len(t) > 4:      # field table without header indicates something wrong
                for nf, f in enumerate(t[4]):
                    btype = symtab[f[2]] if f[2] in symtab else ""
                    btype = "vocab" if btype == "Enumerated" else btype
                    trow += _write_field(sheet_types, trow, tcol, f, tdfield, t[1], btype)
            trow += 2

    wkbook.close()
