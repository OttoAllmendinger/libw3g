import logging
import shelve
import json
from os.path import *

from libw3g.Tools import pprint

PATH_JSONFILE = join(dirname(__file__), 'units-%s.json')

def _getUnitInfo(version):
    return json.load(file(PATH_JSONFILE % version, 'r'))

class Unit:
    mapper = _getUnitInfo('6.60')

    def __init__(self, unitId):
        self.unitId = unitId
        self.unitData = self.mapper[unitId]
        self.name = self.getName()

    def getName(self):
        return self.unitData['Name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, str(self))

class Hero(Unit):
    def getName(self):
        name = self.unitData['Name']
        properName = self.unitData.get('ProperNames', ['Name'])[-1]
        return '%s (%s)' % (name, properName)

class Item(Unit):
    pass

class UnknownUnit(Unit):
    def __init__(self, unitId):
        self.unitId = unitId
        self.unitData = {'Image': 'UnknownUnit.png'}
        self.name = self.getName()

    def getName(self):
        return 'Unknown (id=%s)' % self.unitId

def getUnit(unitId):
    if unitId=='\0'*4:
        return None

    unit = Unit.mapper.get(unitId)

    if unit==None:
        logging.warn("unknown unit %s" % unitId)
        return UnknownUnit(unitId)

    utype = unit.get('Type')

    if utype=='HERO':
        return Hero(unitId)
    elif utype=='ITEM':
        return Item(unitId)
    else:
        return Unit(unitId)

def dump():
    for k,v in Unit.mapper.items():
        print k, v

if __name__=="__main__":
    dump()
