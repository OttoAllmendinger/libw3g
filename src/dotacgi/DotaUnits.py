import logging
import shelve
import json
from os.path import *

from libw3g.Tools import pprint

PATH_SHELVEFILE = 'units-%s.db'
PATH_JSONFILE = 'units-%s.json'

def _getShelve(dotaversion):
    sh = shelve.open(PATH_SHELVEFILE % dotaversion)
    if len(sh.keys())==0:
        _fillShelve(sh, dotaversion)
    return sh

def _fillShelve(sh, dotaversion):
    jsonFile = file(PATH_JSONFILE % dotaversion)
    sh.update(dict(
        (k.encode('ASCII'), v) for k,v in json.load(jsonFile).items()))


class Unit:
    mapper = _getShelve('6.60')

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

    def getName(self):
        return 'Unknown (id=%s)' % self.unitId

def getUnit(unitId):
    if unitId=='\0'*4:
        return None

    unit = Unit.mapper.get(unitId)

    if unit==None:
        return UnknownUnit(unitId)

    utype = unit.get('Type')

    if utype=='HERO':
        return Hero(unitId)
    elif utype=='ITEM':
        return Item(unitId)
    else:
        return Unit(unitId)
