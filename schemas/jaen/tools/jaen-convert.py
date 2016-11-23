"""
Translate JSON Abstract Encoding Notation (JAEN) files
"""

from jaen import jaen_load, jaen_dump, jaen_check
from tr_jas import jas_load, jas_dump
from tr_tables import table_dump

if __name__ == "__main__":
    for fname in ("openc2", "cybox"):

        # Convert JAEN Abstract Syntax (JAS) to JAEN

        source = fname + ".jas"
        dest = fname + "_gena"
        jaen = jas_load(source)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)

        # Convert JAEN to JAS, prettyprinted JAEN, and property tables

        source = fname + ".jaen"
        dest = fname + "_genj"
        jaen = jaen_load(source)
        jas_dump(jaen, dest + ".jas", source)
        jaen_dump(jaen, dest + ".jaen", source)
        table_dump(jaen, dest + ".xlsx", source)
