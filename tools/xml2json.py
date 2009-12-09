import xml.etree.ElementTree as ET
import json

def makeDict(xmlfile):
    tree = ET.ElementTree()
    tree.parse(xmlfile)
    n_items = 0
    units = {}
    for nItem in tree.getiterator('Item'):
        buf = {}
        for node in nItem.getiterator():
            buf[node.tag] = (node.text or '').strip()
        units[buf['Id']] = buf
        del buf['Id']
        n_items += 1
    print 'parsed %d items' % n_items
    return units

def saveDict(units, outfile, compact=False):
    ndict = {}
    for unitId, unitData in units.items():
        if unitId == 'Version':
            continue
        ndict[unitId] = unitDict = {}
        for unitKey, unitValue in unitData.items():
            if unitValue:
                if unitKey=='ProperNames':
                    unitValue = unitValue.split(',')
                elif unitKey=='RelatedTo':
                    unitValue = unitValue.split(',')
                elif unitKey=='Art':
                    unitKey='Image'
                    unitValue = unitValue.replace("images/", "")
                    #unitValue = unitValue[:-3] + 'png'
                unitDict[unitKey] = unitValue

    indent = None if compact else 2

    json.dump(ndict, outfile, indent=indent)



infile = file('DotA Allstars v6.60.xml')
outfile = file('units-6.60.json', 'w')
outfile_compact = file('units-6.60.compact.json', 'w')

units = makeDict(infile)
saveDict(units, outfile)
saveDict(units, outfile_compact, compact=True)
