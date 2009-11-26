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
        n_items += 1
    print 'parsed %d items' % n_items
    return units

def saveDict(units, outfile):
    ndict = {}
    for unitId, unitData in units.items():
        if unitId == 'Version':
            continue
        ndict[unitId] = unitDict = {}
        for unitKey, unitValue in unitData.items():
            if unitValue:
                if unitKey=='ProperNames':
                    unitValue = unitValue.split(',')
                unitDict[unitKey] = unitValue

    json.dump(ndict, outfile, indent=2)



infile = file('DotA Allstars v6.60.xml')
outfile = file('units-6.60.json', 'w')

units = makeDict(infile)
saveDict(units, outfile)
