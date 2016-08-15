import os
from lxml import etree

xs = '{http://www.w3.org/2001/XMLSchema}'

def xstprint(e, level=0, sp='. ', drop='as', ofile=None):
    ''' Print an indented tree of elements from XSD '''
    tag = str(e.tag)
    if 's' in drop:
        tag = tag.replace(xs, 'xs:')
    if 'a' in drop and 'annotation' in tag:
        return
    text = e.text.strip() if e.text else ''
    if hasattr(e.tag, '__call__'):
        t = str(e.tag())
        print(tag, e.tag.__name__, t)
        tag = e.tag.__name__ + ': ' + (t[:60] + '..' if len(t) > 62 else t)
    out = level*sp + tag + ': ' + str([a[0]+'='+a[1] for a in e.items()]) + ' "' + text + '"'
    if ofile is None:
        print(out)
    else:
        ofile.write(out+'\n')
    for child in e:
        xstprint(child, level+1, sp, drop, ofile)

schemadir = 'data'

for top, dirs, files in os.walk(schemadir):
    for file in files:
        ifile = os.path.join(top, file)
        base, ext = os.path.splitext(ifile)
        if ext == '.xsd':
            ofile = base + '_sum.txt'
            with open(ifile) as f:
                tree = etree.parse(f)
            print(ifile+': root_name =', tree.docinfo.root_name)
            with open(ofile, 'w') as fw:
                xstprint(tree.getroot(), ofile=fw)
