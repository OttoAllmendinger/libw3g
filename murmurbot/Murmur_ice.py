# **********************************************************************
#
# Copyright (c) 2003-2005 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

# Ice version 3.1.1
# Generated from file `Murmur.ice'

import Ice, IcePy, __builtin__

# Start of module Murmur
_M_Murmur = Ice.openModule('Murmur')
__name__ = 'Murmur'

if not _M_Murmur.__dict__.has_key('_t_NetAddress'):
    _M_Murmur._t_NetAddress = IcePy.defineSequence('::Murmur::NetAddress', IcePy._t_byte)

if not _M_Murmur.__dict__.has_key('User'):
    _M_Murmur.User = Ice.createTempClass()
    class User(object):
        def __init__(self, session=0, userid=0, mute=False, deaf=False, suppress=False, selfMute=False, selfDeaf=False, channel=0, name='', onlinesecs=0, bytespersec=0, version=0, release='', os='', osversion='', identity='', context='', comment='', address=None, tcponly=False, idlesecs=0):
            self.session = session
            self.userid = userid
            self.mute = mute
            self.deaf = deaf
            self.suppress = suppress
            self.selfMute = selfMute
            self.selfDeaf = selfDeaf
            self.channel = channel
            self.name = name
            self.onlinesecs = onlinesecs
            self.bytespersec = bytespersec
            self.version = version
            self.release = release
            self.os = os
            self.osversion = osversion
            self.identity = identity
            self.context = context
            self.comment = comment
            self.address = address
            self.tcponly = tcponly
            self.idlesecs = idlesecs

        def __hash__(self):
            _h = 0
            _h = 5 * _h + __builtin__.hash(self.session)
            _h = 5 * _h + __builtin__.hash(self.userid)
            _h = 5 * _h + __builtin__.hash(self.mute)
            _h = 5 * _h + __builtin__.hash(self.deaf)
            _h = 5 * _h + __builtin__.hash(self.suppress)
            _h = 5 * _h + __builtin__.hash(self.selfMute)
            _h = 5 * _h + __builtin__.hash(self.selfDeaf)
            _h = 5 * _h + __builtin__.hash(self.channel)
            _h = 5 * _h + __builtin__.hash(self.name)
            _h = 5 * _h + __builtin__.hash(self.onlinesecs)
            _h = 5 * _h + __builtin__.hash(self.bytespersec)
            _h = 5 * _h + __builtin__.hash(self.version)
            _h = 5 * _h + __builtin__.hash(self.release)
            _h = 5 * _h + __builtin__.hash(self.os)
            _h = 5 * _h + __builtin__.hash(self.osversion)
            _h = 5 * _h + __builtin__.hash(self.identity)
            _h = 5 * _h + __builtin__.hash(self.context)
            _h = 5 * _h + __builtin__.hash(self.comment)
            if self.address:
                for _i0 in self.address:
                    _h = 5 * _h + __builtin__.hash(_i0)
            _h = 5 * _h + __builtin__.hash(self.tcponly)
            _h = 5 * _h + __builtin__.hash(self.idlesecs)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.session == other.session:
                return False
            if not self.userid == other.userid:
                return False
            if not self.mute == other.mute:
                return False
            if not self.deaf == other.deaf:
                return False
            if not self.suppress == other.suppress:
                return False
            if not self.selfMute == other.selfMute:
                return False
            if not self.selfDeaf == other.selfDeaf:
                return False
            if not self.channel == other.channel:
                return False
            if not self.name == other.name:
                return False
            if not self.onlinesecs == other.onlinesecs:
                return False
            if not self.bytespersec == other.bytespersec:
                return False
            if not self.version == other.version:
                return False
            if not self.release == other.release:
                return False
            if not self.os == other.os:
                return False
            if not self.osversion == other.osversion:
                return False
            if not self.identity == other.identity:
                return False
            if not self.context == other.context:
                return False
            if not self.comment == other.comment:
                return False
            if not self.address == other.address:
                return False
            if not self.tcponly == other.tcponly:
                return False
            if not self.idlesecs == other.idlesecs:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_User)

        __repr__ = __str__

    _M_Murmur._t_User = IcePy.defineStruct('::Murmur::User', User, (
        ("session", IcePy._t_int),
        ("userid", IcePy._t_int),
        ("mute", IcePy._t_bool),
        ("deaf", IcePy._t_bool),
        ("suppress", IcePy._t_bool),
        ("selfMute", IcePy._t_bool),
        ("selfDeaf", IcePy._t_bool),
        ("channel", IcePy._t_int),
        ("name", IcePy._t_string),
        ("onlinesecs", IcePy._t_int),
        ("bytespersec", IcePy._t_int),
        ("version", IcePy._t_int),
        ("release", IcePy._t_string),
        ("os", IcePy._t_string),
        ("osversion", IcePy._t_string),
        ("identity", IcePy._t_string),
        ("context", IcePy._t_string),
        ("comment", IcePy._t_string),
        ("address", _M_Murmur._t_NetAddress),
        ("tcponly", IcePy._t_bool),
        ("idlesecs", IcePy._t_int)
    ))

    _M_Murmur.User = User
    del User

if not _M_Murmur.__dict__.has_key('_t_IntList'):
    _M_Murmur._t_IntList = IcePy.defineSequence('::Murmur::IntList', IcePy._t_int)

if not _M_Murmur.__dict__.has_key('Channel'):
    _M_Murmur.Channel = Ice.createTempClass()
    class Channel(object):
        def __init__(self, id=0, name='', parent=0, links=None, description='', temporary=False, position=0):
            self.id = id
            self.name = name
            self.parent = parent
            self.links = links
            self.description = description
            self.temporary = temporary
            self.position = position

        def __hash__(self):
            _h = 0
            _h = 5 * _h + __builtin__.hash(self.id)
            _h = 5 * _h + __builtin__.hash(self.name)
            _h = 5 * _h + __builtin__.hash(self.parent)
            if self.links:
                for _i0 in self.links:
                    _h = 5 * _h + __builtin__.hash(_i0)
            _h = 5 * _h + __builtin__.hash(self.description)
            _h = 5 * _h + __builtin__.hash(self.temporary)
            _h = 5 * _h + __builtin__.hash(self.position)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.id == other.id:
                return False
            if not self.name == other.name:
                return False
            if not self.parent == other.parent:
                return False
            if not self.links == other.links:
                return False
            if not self.description == other.description:
                return False
            if not self.temporary == other.temporary:
                return False
            if not self.position == other.position:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Channel)

        __repr__ = __str__

    _M_Murmur._t_Channel = IcePy.defineStruct('::Murmur::Channel', Channel, (
        ("id", IcePy._t_int),
        ("name", IcePy._t_string),
        ("parent", IcePy._t_int),
        ("links", _M_Murmur._t_IntList),
        ("description", IcePy._t_string),
        ("temporary", IcePy._t_bool),
        ("position", IcePy._t_int)
    ))

    _M_Murmur.Channel = Channel
    del Channel

if not _M_Murmur.__dict__.has_key('Group'):
    _M_Murmur.Group = Ice.createTempClass()
    class Group(object):
        def __init__(self, name='', inherited=False, inherit=False, inheritable=False, add=None, remove=None, members=None):
            self.name = name
            self.inherited = inherited
            self.inherit = inherit
            self.inheritable = inheritable
            self.add = add
            self.remove = remove
            self.members = members

        def __hash__(self):
            _h = 0
            _h = 5 * _h + __builtin__.hash(self.name)
            _h = 5 * _h + __builtin__.hash(self.inherited)
            _h = 5 * _h + __builtin__.hash(self.inherit)
            _h = 5 * _h + __builtin__.hash(self.inheritable)
            if self.add:
                for _i0 in self.add:
                    _h = 5 * _h + __builtin__.hash(_i0)
            if self.remove:
                for _i1 in self.remove:
                    _h = 5 * _h + __builtin__.hash(_i1)
            if self.members:
                for _i2 in self.members:
                    _h = 5 * _h + __builtin__.hash(_i2)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.name == other.name:
                return False
            if not self.inherited == other.inherited:
                return False
            if not self.inherit == other.inherit:
                return False
            if not self.inheritable == other.inheritable:
                return False
            if not self.add == other.add:
                return False
            if not self.remove == other.remove:
                return False
            if not self.members == other.members:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Group)

        __repr__ = __str__

    _M_Murmur._t_Group = IcePy.defineStruct('::Murmur::Group', Group, (
        ("name", IcePy._t_string),
        ("inherited", IcePy._t_bool),
        ("inherit", IcePy._t_bool),
        ("inheritable", IcePy._t_bool),
        ("add", _M_Murmur._t_IntList),
        ("remove", _M_Murmur._t_IntList),
        ("members", _M_Murmur._t_IntList)
    ))

    _M_Murmur.Group = Group
    del Group

_M_Murmur.PermissionWrite = 1

_M_Murmur.PermissionTraverse = 2

_M_Murmur.PermissionEnter = 4

_M_Murmur.PermissionSpeak = 8

_M_Murmur.PermissionWhisper = 256

_M_Murmur.PermissionMuteDeafen = 16

_M_Murmur.PermissionMove = 32

_M_Murmur.PermissionMakeChannel = 64

_M_Murmur.PermissionMakeTempChannel = 1024

_M_Murmur.PermissionLinkChannel = 128

_M_Murmur.PermissionTextMessage = 512

_M_Murmur.PermissionKick = 65536

_M_Murmur.PermissionBan = 131072

_M_Murmur.PermissionRegister = 262144

_M_Murmur.PermissionRegisterSelf = 524288

if not _M_Murmur.__dict__.has_key('ACL'):
    _M_Murmur.ACL = Ice.createTempClass()
    class ACL(object):
        def __init__(self, applyHere=False, applySubs=False, inherited=False, userid=0, group='', allow=0, deny=0):
            self.applyHere = applyHere
            self.applySubs = applySubs
            self.inherited = inherited
            self.userid = userid
            self.group = group
            self.allow = allow
            self.deny = deny

        def __hash__(self):
            _h = 0
            _h = 5 * _h + __builtin__.hash(self.applyHere)
            _h = 5 * _h + __builtin__.hash(self.applySubs)
            _h = 5 * _h + __builtin__.hash(self.inherited)
            _h = 5 * _h + __builtin__.hash(self.userid)
            _h = 5 * _h + __builtin__.hash(self.group)
            _h = 5 * _h + __builtin__.hash(self.allow)
            _h = 5 * _h + __builtin__.hash(self.deny)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.applyHere == other.applyHere:
                return False
            if not self.applySubs == other.applySubs:
                return False
            if not self.inherited == other.inherited:
                return False
            if not self.userid == other.userid:
                return False
            if not self.group == other.group:
                return False
            if not self.allow == other.allow:
                return False
            if not self.deny == other.deny:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_ACL)

        __repr__ = __str__

    _M_Murmur._t_ACL = IcePy.defineStruct('::Murmur::ACL', ACL, (
        ("applyHere", IcePy._t_bool),
        ("applySubs", IcePy._t_bool),
        ("inherited", IcePy._t_bool),
        ("userid", IcePy._t_int),
        ("group", IcePy._t_string),
        ("allow", IcePy._t_int),
        ("deny", IcePy._t_int)
    ))

    _M_Murmur.ACL = ACL
    del ACL

if not _M_Murmur.__dict__.has_key('Ban'):
    _M_Murmur.Ban = Ice.createTempClass()
    class Ban(object):
        def __init__(self, address=None, bits=0, name='', hash='', reason='', start=0, duration=0):
            self.address = address
            self.bits = bits
            self.name = name
            self.hash = hash
            self.reason = reason
            self.start = start
            self.duration = duration

        def __hash__(self):
            _h = 0
            if self.address:
                for _i0 in self.address:
                    _h = 5 * _h + __builtin__.hash(_i0)
            _h = 5 * _h + __builtin__.hash(self.bits)
            _h = 5 * _h + __builtin__.hash(self.name)
            _h = 5 * _h + __builtin__.hash(self.hash)
            _h = 5 * _h + __builtin__.hash(self.reason)
            _h = 5 * _h + __builtin__.hash(self.start)
            _h = 5 * _h + __builtin__.hash(self.duration)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.address == other.address:
                return False
            if not self.bits == other.bits:
                return False
            if not self.name == other.name:
                return False
            if not self.hash == other.hash:
                return False
            if not self.reason == other.reason:
                return False
            if not self.start == other.start:
                return False
            if not self.duration == other.duration:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Ban)

        __repr__ = __str__

    _M_Murmur._t_Ban = IcePy.defineStruct('::Murmur::Ban', Ban, (
        ("address", _M_Murmur._t_NetAddress),
        ("bits", IcePy._t_int),
        ("name", IcePy._t_string),
        ("hash", IcePy._t_string),
        ("reason", IcePy._t_string),
        ("start", IcePy._t_long),
        ("duration", IcePy._t_int)
    ))

    _M_Murmur.Ban = Ban
    del Ban

if not _M_Murmur.__dict__.has_key('LogEntry'):
    _M_Murmur.LogEntry = Ice.createTempClass()
    class LogEntry(object):
        def __init__(self, timestamp=0, txt=''):
            self.timestamp = timestamp
            self.txt = txt

        def __hash__(self):
            _h = 0
            _h = 5 * _h + __builtin__.hash(self.timestamp)
            _h = 5 * _h + __builtin__.hash(self.txt)
            return _h % 0x7fffffff

        def __eq__(self, other):
            if not self.timestamp == other.timestamp:
                return False
            if not self.txt == other.txt:
                return False
            return True

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_LogEntry)

        __repr__ = __str__

    _M_Murmur._t_LogEntry = IcePy.defineStruct('::Murmur::LogEntry', LogEntry, (
        ("timestamp", IcePy._t_int),
        ("txt", IcePy._t_string)
    ))

    _M_Murmur.LogEntry = LogEntry
    del LogEntry

if not _M_Murmur.__dict__.has_key('Tree'):
    _M_Murmur._t_Tree = IcePy.declareClass('::Murmur::Tree')
    _M_Murmur._t_TreePrx = IcePy.declareProxy('::Murmur::Tree')

if not _M_Murmur.__dict__.has_key('_t_TreeList'):
    _M_Murmur._t_TreeList = IcePy.defineSequence('::Murmur::TreeList', _M_Murmur._t_Tree)

if not _M_Murmur.__dict__.has_key('ChannelInfo'):
    _M_Murmur.ChannelInfo = Ice.createTempClass()
    class ChannelInfo(object):

        def __init__(self, val):
            assert(val >= 0 and val < 2)
            self.value = val

        def __str__(self):
            if self.value == 0:
                return 'ChannelDescription'
            elif self.value == 1:
                return 'ChannelPosition'
            return None

        __repr__ = __str__

        def __hash__(self):
            return self.value

        def __cmp__(self, other):
            return cmp(self.value, other.value)

    ChannelInfo.ChannelDescription = ChannelInfo(0)
    ChannelInfo.ChannelPosition = ChannelInfo(1)

    _M_Murmur._t_ChannelInfo = IcePy.defineEnum('::Murmur::ChannelInfo', ChannelInfo, (ChannelInfo.ChannelDescription, ChannelInfo.ChannelPosition))

    _M_Murmur.ChannelInfo = ChannelInfo
    del ChannelInfo

if not _M_Murmur.__dict__.has_key('UserInfo'):
    _M_Murmur.UserInfo = Ice.createTempClass()
    class UserInfo(object):

        def __init__(self, val):
            assert(val >= 0 and val < 5)
            self.value = val

        def __str__(self):
            if self.value == 0:
                return 'UserName'
            elif self.value == 1:
                return 'UserEmail'
            elif self.value == 2:
                return 'UserComment'
            elif self.value == 3:
                return 'UserHash'
            elif self.value == 4:
                return 'UserPassword'
            return None

        __repr__ = __str__

        def __hash__(self):
            return self.value

        def __cmp__(self, other):
            return cmp(self.value, other.value)

    UserInfo.UserName = UserInfo(0)
    UserInfo.UserEmail = UserInfo(1)
    UserInfo.UserComment = UserInfo(2)
    UserInfo.UserHash = UserInfo(3)
    UserInfo.UserPassword = UserInfo(4)

    _M_Murmur._t_UserInfo = IcePy.defineEnum('::Murmur::UserInfo', UserInfo, (UserInfo.UserName, UserInfo.UserEmail, UserInfo.UserComment, UserInfo.UserHash, UserInfo.UserPassword))

    _M_Murmur.UserInfo = UserInfo
    del UserInfo

if not _M_Murmur.__dict__.has_key('_t_UserMap'):
    _M_Murmur._t_UserMap = IcePy.defineDictionary('::Murmur::UserMap', IcePy._t_int, _M_Murmur._t_User)

if not _M_Murmur.__dict__.has_key('_t_ChannelMap'):
    _M_Murmur._t_ChannelMap = IcePy.defineDictionary('::Murmur::ChannelMap', IcePy._t_int, _M_Murmur._t_Channel)

if not _M_Murmur.__dict__.has_key('_t_ChannelList'):
    _M_Murmur._t_ChannelList = IcePy.defineSequence('::Murmur::ChannelList', _M_Murmur._t_Channel)

if not _M_Murmur.__dict__.has_key('_t_UserList'):
    _M_Murmur._t_UserList = IcePy.defineSequence('::Murmur::UserList', _M_Murmur._t_User)

if not _M_Murmur.__dict__.has_key('_t_GroupList'):
    _M_Murmur._t_GroupList = IcePy.defineSequence('::Murmur::GroupList', _M_Murmur._t_Group)

if not _M_Murmur.__dict__.has_key('_t_ACLList'):
    _M_Murmur._t_ACLList = IcePy.defineSequence('::Murmur::ACLList', _M_Murmur._t_ACL)

if not _M_Murmur.__dict__.has_key('_t_LogList'):
    _M_Murmur._t_LogList = IcePy.defineSequence('::Murmur::LogList', _M_Murmur._t_LogEntry)

if not _M_Murmur.__dict__.has_key('_t_BanList'):
    _M_Murmur._t_BanList = IcePy.defineSequence('::Murmur::BanList', _M_Murmur._t_Ban)

if not _M_Murmur.__dict__.has_key('_t_IdList'):
    _M_Murmur._t_IdList = IcePy.defineSequence('::Murmur::IdList', IcePy._t_int)

if not _M_Murmur.__dict__.has_key('_t_NameList'):
    _M_Murmur._t_NameList = IcePy.defineSequence('::Murmur::NameList', IcePy._t_string)

if not _M_Murmur.__dict__.has_key('_t_NameMap'):
    _M_Murmur._t_NameMap = IcePy.defineDictionary('::Murmur::NameMap', IcePy._t_int, IcePy._t_string)

if not _M_Murmur.__dict__.has_key('_t_IdMap'):
    _M_Murmur._t_IdMap = IcePy.defineDictionary('::Murmur::IdMap', IcePy._t_string, IcePy._t_int)

if not _M_Murmur.__dict__.has_key('_t_Texture'):
    _M_Murmur._t_Texture = IcePy.defineSequence('::Murmur::Texture', IcePy._t_byte)

if not _M_Murmur.__dict__.has_key('_t_ConfigMap'):
    _M_Murmur._t_ConfigMap = IcePy.defineDictionary('::Murmur::ConfigMap', IcePy._t_string, IcePy._t_string)

if not _M_Murmur.__dict__.has_key('_t_GroupNameList'):
    _M_Murmur._t_GroupNameList = IcePy.defineSequence('::Murmur::GroupNameList', IcePy._t_string)

if not _M_Murmur.__dict__.has_key('_t_CertificateDer'):
    _M_Murmur._t_CertificateDer = IcePy.defineSequence('::Murmur::CertificateDer', IcePy._t_byte)

if not _M_Murmur.__dict__.has_key('_t_CertificateList'):
    _M_Murmur._t_CertificateList = IcePy.defineSequence('::Murmur::CertificateList', _M_Murmur._t_CertificateDer)

if not _M_Murmur.__dict__.has_key('_t_UserInfoMap'):
    _M_Murmur._t_UserInfoMap = IcePy.defineDictionary('::Murmur::UserInfoMap', _M_Murmur._t_UserInfo, IcePy._t_string)

if not _M_Murmur.__dict__.has_key('Tree'):
    _M_Murmur.Tree = Ice.createTempClass()
    class Tree(Ice.Object):
        def __init__(self, c=_M_Murmur.Channel(), children=None, users=None):
            self.c = c
            self.children = children
            self.users = users

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::Tree')

        def ice_id(self, current=None):
            return '::Murmur::Tree'

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Tree)

        __repr__ = __str__

    _M_Murmur.TreePrx = Ice.createTempClass()
    class TreePrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.TreePrx.ice_checkedCast(proxy, '::Murmur::Tree', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.TreePrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_TreePrx = IcePy.defineProxy('::Murmur::Tree', TreePrx)

    _M_Murmur._t_Tree = IcePy.defineClass('::Murmur::Tree', Tree, False, None, (), (
        ('c', _M_Murmur._t_Channel),
        ('children', _M_Murmur._t_TreeList),
        ('users', _M_Murmur._t_UserList)
    ))
    Tree.ice_type = _M_Murmur._t_Tree

    _M_Murmur.Tree = Tree
    del Tree

    _M_Murmur.TreePrx = TreePrx
    del TreePrx

if not _M_Murmur.__dict__.has_key('MurmurException'):
    _M_Murmur.MurmurException = Ice.createTempClass()
    class MurmurException(Ice.UserException):
        def __init__(self):
            pass

        def ice_name(self):
            return 'Murmur::MurmurException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_MurmurException = IcePy.defineException('::Murmur::MurmurException', MurmurException, None, ())
    MurmurException.ice_type = _M_Murmur._t_MurmurException

    _M_Murmur.MurmurException = MurmurException
    del MurmurException

if not _M_Murmur.__dict__.has_key('InvalidSessionException'):
    _M_Murmur.InvalidSessionException = Ice.createTempClass()
    class InvalidSessionException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidSessionException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidSessionException = IcePy.defineException('::Murmur::InvalidSessionException', InvalidSessionException, _M_Murmur._t_MurmurException, ())
    InvalidSessionException.ice_type = _M_Murmur._t_InvalidSessionException

    _M_Murmur.InvalidSessionException = InvalidSessionException
    del InvalidSessionException

if not _M_Murmur.__dict__.has_key('InvalidChannelException'):
    _M_Murmur.InvalidChannelException = Ice.createTempClass()
    class InvalidChannelException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidChannelException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidChannelException = IcePy.defineException('::Murmur::InvalidChannelException', InvalidChannelException, _M_Murmur._t_MurmurException, ())
    InvalidChannelException.ice_type = _M_Murmur._t_InvalidChannelException

    _M_Murmur.InvalidChannelException = InvalidChannelException
    del InvalidChannelException

if not _M_Murmur.__dict__.has_key('InvalidServerException'):
    _M_Murmur.InvalidServerException = Ice.createTempClass()
    class InvalidServerException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidServerException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidServerException = IcePy.defineException('::Murmur::InvalidServerException', InvalidServerException, _M_Murmur._t_MurmurException, ())
    InvalidServerException.ice_type = _M_Murmur._t_InvalidServerException

    _M_Murmur.InvalidServerException = InvalidServerException
    del InvalidServerException

if not _M_Murmur.__dict__.has_key('ServerBootedException'):
    _M_Murmur.ServerBootedException = Ice.createTempClass()
    class ServerBootedException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::ServerBootedException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_ServerBootedException = IcePy.defineException('::Murmur::ServerBootedException', ServerBootedException, _M_Murmur._t_MurmurException, ())
    ServerBootedException.ice_type = _M_Murmur._t_ServerBootedException

    _M_Murmur.ServerBootedException = ServerBootedException
    del ServerBootedException

if not _M_Murmur.__dict__.has_key('ServerFailureException'):
    _M_Murmur.ServerFailureException = Ice.createTempClass()
    class ServerFailureException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::ServerFailureException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_ServerFailureException = IcePy.defineException('::Murmur::ServerFailureException', ServerFailureException, _M_Murmur._t_MurmurException, ())
    ServerFailureException.ice_type = _M_Murmur._t_ServerFailureException

    _M_Murmur.ServerFailureException = ServerFailureException
    del ServerFailureException

if not _M_Murmur.__dict__.has_key('InvalidUserException'):
    _M_Murmur.InvalidUserException = Ice.createTempClass()
    class InvalidUserException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidUserException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidUserException = IcePy.defineException('::Murmur::InvalidUserException', InvalidUserException, _M_Murmur._t_MurmurException, ())
    InvalidUserException.ice_type = _M_Murmur._t_InvalidUserException

    _M_Murmur.InvalidUserException = InvalidUserException
    del InvalidUserException

if not _M_Murmur.__dict__.has_key('InvalidTextureException'):
    _M_Murmur.InvalidTextureException = Ice.createTempClass()
    class InvalidTextureException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidTextureException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidTextureException = IcePy.defineException('::Murmur::InvalidTextureException', InvalidTextureException, _M_Murmur._t_MurmurException, ())
    InvalidTextureException.ice_type = _M_Murmur._t_InvalidTextureException

    _M_Murmur.InvalidTextureException = InvalidTextureException
    del InvalidTextureException

if not _M_Murmur.__dict__.has_key('InvalidCallbackException'):
    _M_Murmur.InvalidCallbackException = Ice.createTempClass()
    class InvalidCallbackException(_M_Murmur.MurmurException):
        def __init__(self):
            _M_Murmur.MurmurException.__init__(self)

        def ice_name(self):
            return 'Murmur::InvalidCallbackException'

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

    _M_Murmur._t_InvalidCallbackException = IcePy.defineException('::Murmur::InvalidCallbackException', InvalidCallbackException, _M_Murmur._t_MurmurException, ())
    InvalidCallbackException.ice_type = _M_Murmur._t_InvalidCallbackException

    _M_Murmur.InvalidCallbackException = InvalidCallbackException
    del InvalidCallbackException

if not _M_Murmur.__dict__.has_key('ServerCallback'):
    _M_Murmur.ServerCallback = Ice.createTempClass()
    class ServerCallback(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.ServerCallback:
                raise RuntimeError('Murmur.ServerCallback is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::ServerCallback')

        def ice_id(self, current=None):
            return '::Murmur::ServerCallback'

        #
        # Operation signatures.
        #
        # def userConnected(self, state, current=None):
        # def userDisconnected(self, state, current=None):
        # def userStateChanged(self, state, current=None):
        # def channelCreated(self, state, current=None):
        # def channelRemoved(self, state, current=None):
        # def channelStateChanged(self, state, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_ServerCallback)

        __repr__ = __str__

    _M_Murmur.ServerCallbackPrx = Ice.createTempClass()
    class ServerCallbackPrx(Ice.ObjectPrx):

        def userConnected(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_userConnected.invoke(self, (state, ), _ctx)

        def userDisconnected(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_userDisconnected.invoke(self, (state, ), _ctx)

        def userStateChanged(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_userStateChanged.invoke(self, (state, ), _ctx)

        def channelCreated(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_channelCreated.invoke(self, (state, ), _ctx)

        def channelRemoved(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_channelRemoved.invoke(self, (state, ), _ctx)

        def channelStateChanged(self, state, _ctx=None):
            return _M_Murmur.ServerCallback._op_channelStateChanged.invoke(self, (state, ), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.ServerCallbackPrx.ice_checkedCast(proxy, '::Murmur::ServerCallback', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.ServerCallbackPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_ServerCallbackPrx = IcePy.defineProxy('::Murmur::ServerCallback', ServerCallbackPrx)

    _M_Murmur._t_ServerCallback = IcePy.defineClass('::Murmur::ServerCallback', ServerCallback, True, None, (), ())
    ServerCallback.ice_type = _M_Murmur._t_ServerCallback

    ServerCallback._op_userConnected = IcePy.Operation('userConnected', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_User,), (), None, ())
    ServerCallback._op_userDisconnected = IcePy.Operation('userDisconnected', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_User,), (), None, ())
    ServerCallback._op_userStateChanged = IcePy.Operation('userStateChanged', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_User,), (), None, ())
    ServerCallback._op_channelCreated = IcePy.Operation('channelCreated', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_Channel,), (), None, ())
    ServerCallback._op_channelRemoved = IcePy.Operation('channelRemoved', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_Channel,), (), None, ())
    ServerCallback._op_channelStateChanged = IcePy.Operation('channelStateChanged', Ice.OperationMode.Idempotent, False, (_M_Murmur._t_Channel,), (), None, ())

    _M_Murmur.ServerCallback = ServerCallback
    del ServerCallback

    _M_Murmur.ServerCallbackPrx = ServerCallbackPrx
    del ServerCallbackPrx

_M_Murmur.ContextServer = 1

_M_Murmur.ContextChannel = 2

_M_Murmur.ContextUser = 4

if not _M_Murmur.__dict__.has_key('ServerContextCallback'):
    _M_Murmur.ServerContextCallback = Ice.createTempClass()
    class ServerContextCallback(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.ServerContextCallback:
                raise RuntimeError('Murmur.ServerContextCallback is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::ServerContextCallback')

        def ice_id(self, current=None):
            return '::Murmur::ServerContextCallback'

        #
        # Operation signatures.
        #
        # def contextAction(self, action, usr, session, channelid, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_ServerContextCallback)

        __repr__ = __str__

    _M_Murmur.ServerContextCallbackPrx = Ice.createTempClass()
    class ServerContextCallbackPrx(Ice.ObjectPrx):

        def contextAction(self, action, usr, session, channelid, _ctx=None):
            return _M_Murmur.ServerContextCallback._op_contextAction.invoke(self, (action, usr, session, channelid), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.ServerContextCallbackPrx.ice_checkedCast(proxy, '::Murmur::ServerContextCallback', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.ServerContextCallbackPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_ServerContextCallbackPrx = IcePy.defineProxy('::Murmur::ServerContextCallback', ServerContextCallbackPrx)

    _M_Murmur._t_ServerContextCallback = IcePy.defineClass('::Murmur::ServerContextCallback', ServerContextCallback, True, None, (), ())
    ServerContextCallback.ice_type = _M_Murmur._t_ServerContextCallback

    ServerContextCallback._op_contextAction = IcePy.Operation('contextAction', Ice.OperationMode.Idempotent, False, (IcePy._t_string, _M_Murmur._t_User, IcePy._t_int, IcePy._t_int), (), None, ())

    _M_Murmur.ServerContextCallback = ServerContextCallback
    del ServerContextCallback

    _M_Murmur.ServerContextCallbackPrx = ServerContextCallbackPrx
    del ServerContextCallbackPrx

if not _M_Murmur.__dict__.has_key('ServerAuthenticator'):
    _M_Murmur.ServerAuthenticator = Ice.createTempClass()
    class ServerAuthenticator(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.ServerAuthenticator:
                raise RuntimeError('Murmur.ServerAuthenticator is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::ServerAuthenticator')

        def ice_id(self, current=None):
            return '::Murmur::ServerAuthenticator'

        #
        # Operation signatures.
        #
        # def authenticate(self, name, pw, certificates, certhash, certstrong, current=None):
        # def getInfo(self, id, current=None):
        # def nameToId(self, name, current=None):
        # def idToName(self, id, current=None):
        # def idToTexture(self, id, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_ServerAuthenticator)

        __repr__ = __str__

    _M_Murmur.ServerAuthenticatorPrx = Ice.createTempClass()
    class ServerAuthenticatorPrx(Ice.ObjectPrx):

        def authenticate(self, name, pw, certificates, certhash, certstrong, _ctx=None):
            return _M_Murmur.ServerAuthenticator._op_authenticate.invoke(self, (name, pw, certificates, certhash, certstrong), _ctx)

        def getInfo(self, id, _ctx=None):
            return _M_Murmur.ServerAuthenticator._op_getInfo.invoke(self, (id, ), _ctx)

        def nameToId(self, name, _ctx=None):
            return _M_Murmur.ServerAuthenticator._op_nameToId.invoke(self, (name, ), _ctx)

        def idToName(self, id, _ctx=None):
            return _M_Murmur.ServerAuthenticator._op_idToName.invoke(self, (id, ), _ctx)

        def idToTexture(self, id, _ctx=None):
            return _M_Murmur.ServerAuthenticator._op_idToTexture.invoke(self, (id, ), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.ServerAuthenticatorPrx.ice_checkedCast(proxy, '::Murmur::ServerAuthenticator', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.ServerAuthenticatorPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_ServerAuthenticatorPrx = IcePy.defineProxy('::Murmur::ServerAuthenticator', ServerAuthenticatorPrx)

    _M_Murmur._t_ServerAuthenticator = IcePy.defineClass('::Murmur::ServerAuthenticator', ServerAuthenticator, True, None, (), ())
    ServerAuthenticator.ice_type = _M_Murmur._t_ServerAuthenticator

    ServerAuthenticator._op_authenticate = IcePy.Operation('authenticate', Ice.OperationMode.Idempotent, False, (IcePy._t_string, IcePy._t_string, _M_Murmur._t_CertificateList, IcePy._t_string, IcePy._t_bool), (IcePy._t_string, _M_Murmur._t_GroupNameList), IcePy._t_int, ())
    ServerAuthenticator._op_getInfo = IcePy.Operation('getInfo', Ice.OperationMode.Idempotent, False, (IcePy._t_int,), (_M_Murmur._t_UserInfoMap,), IcePy._t_bool, ())
    ServerAuthenticator._op_nameToId = IcePy.Operation('nameToId', Ice.OperationMode.Idempotent, False, (IcePy._t_string,), (), IcePy._t_int, ())
    ServerAuthenticator._op_idToName = IcePy.Operation('idToName', Ice.OperationMode.Idempotent, False, (IcePy._t_int,), (), IcePy._t_string, ())
    ServerAuthenticator._op_idToTexture = IcePy.Operation('idToTexture', Ice.OperationMode.Idempotent, False, (IcePy._t_int,), (), _M_Murmur._t_Texture, ())

    _M_Murmur.ServerAuthenticator = ServerAuthenticator
    del ServerAuthenticator

    _M_Murmur.ServerAuthenticatorPrx = ServerAuthenticatorPrx
    del ServerAuthenticatorPrx

if not _M_Murmur.__dict__.has_key('ServerUpdatingAuthenticator'):
    _M_Murmur.ServerUpdatingAuthenticator = Ice.createTempClass()
    class ServerUpdatingAuthenticator(_M_Murmur.ServerAuthenticator):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.ServerUpdatingAuthenticator:
                raise RuntimeError('Murmur.ServerUpdatingAuthenticator is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::ServerAuthenticator', '::Murmur::ServerUpdatingAuthenticator')

        def ice_id(self, current=None):
            return '::Murmur::ServerUpdatingAuthenticator'

        #
        # Operation signatures.
        #
        # def registerUser(self, info, current=None):
        # def unregisterUser(self, id, current=None):
        # def getRegisteredUsers(self, filter, current=None):
        # def setInfo(self, id, info, current=None):
        # def setTexture(self, id, tex, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_ServerUpdatingAuthenticator)

        __repr__ = __str__

    _M_Murmur.ServerUpdatingAuthenticatorPrx = Ice.createTempClass()
    class ServerUpdatingAuthenticatorPrx(_M_Murmur.ServerAuthenticatorPrx):

        def registerUser(self, info, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticator._op_registerUser.invoke(self, (info, ), _ctx)

        def unregisterUser(self, id, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticator._op_unregisterUser.invoke(self, (id, ), _ctx)

        def getRegisteredUsers(self, filter, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticator._op_getRegisteredUsers.invoke(self, (filter, ), _ctx)

        def setInfo(self, id, info, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticator._op_setInfo.invoke(self, (id, info), _ctx)

        def setTexture(self, id, tex, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticator._op_setTexture.invoke(self, (id, tex), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.ServerUpdatingAuthenticatorPrx.ice_checkedCast(proxy, '::Murmur::ServerUpdatingAuthenticator', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.ServerUpdatingAuthenticatorPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_ServerUpdatingAuthenticatorPrx = IcePy.defineProxy('::Murmur::ServerUpdatingAuthenticator', ServerUpdatingAuthenticatorPrx)

    _M_Murmur._t_ServerUpdatingAuthenticator = IcePy.defineClass('::Murmur::ServerUpdatingAuthenticator', ServerUpdatingAuthenticator, True, None, (_M_Murmur._t_ServerAuthenticator,), ())
    ServerUpdatingAuthenticator.ice_type = _M_Murmur._t_ServerUpdatingAuthenticator

    ServerUpdatingAuthenticator._op_registerUser = IcePy.Operation('registerUser', Ice.OperationMode.Normal, False, (_M_Murmur._t_UserInfoMap,), (), IcePy._t_int, ())
    ServerUpdatingAuthenticator._op_unregisterUser = IcePy.Operation('unregisterUser', Ice.OperationMode.Normal, False, (IcePy._t_int,), (), IcePy._t_int, ())
    ServerUpdatingAuthenticator._op_getRegisteredUsers = IcePy.Operation('getRegisteredUsers', Ice.OperationMode.Idempotent, False, (IcePy._t_string,), (), _M_Murmur._t_NameMap, ())
    ServerUpdatingAuthenticator._op_setInfo = IcePy.Operation('setInfo', Ice.OperationMode.Idempotent, False, (IcePy._t_int, _M_Murmur._t_UserInfoMap), (), IcePy._t_int, ())
    ServerUpdatingAuthenticator._op_setTexture = IcePy.Operation('setTexture', Ice.OperationMode.Idempotent, False, (IcePy._t_int, _M_Murmur._t_Texture), (), IcePy._t_int, ())

    _M_Murmur.ServerUpdatingAuthenticator = ServerUpdatingAuthenticator
    del ServerUpdatingAuthenticator

    _M_Murmur.ServerUpdatingAuthenticatorPrx = ServerUpdatingAuthenticatorPrx
    del ServerUpdatingAuthenticatorPrx

if not _M_Murmur.__dict__.has_key('Server'):
    _M_Murmur.Server = Ice.createTempClass()
    class Server(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.Server:
                raise RuntimeError('Murmur.Server is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::Server')

        def ice_id(self, current=None):
            return '::Murmur::Server'

        #
        # Operation signatures.
        #
        # def isRunning_async(self, _cb, current=None):
        # def start_async(self, _cb, current=None):
        # def stop_async(self, _cb, current=None):
        # def delete_async(self, _cb, current=None):
        # def id_async(self, _cb, current=None):
        # def addCallback_async(self, _cb, cb, current=None):
        # def removeCallback_async(self, _cb, cb, current=None):
        # def setAuthenticator_async(self, _cb, auth, current=None):
        # def getConf_async(self, _cb, key, current=None):
        # def getAllConf_async(self, _cb, current=None):
        # def setConf_async(self, _cb, key, value, current=None):
        # def setSuperuserPassword_async(self, _cb, pw, current=None):
        # def getLog_async(self, _cb, first, last, current=None):
        # def getUsers_async(self, _cb, current=None):
        # def getChannels_async(self, _cb, current=None):
        # def getTree_async(self, _cb, current=None):
        # def getBans_async(self, _cb, current=None):
        # def setBans_async(self, _cb, bans, current=None):
        # def kickUser_async(self, _cb, session, reason, current=None):
        # def getState_async(self, _cb, session, current=None):
        # def setState_async(self, _cb, state, current=None):
        # def sendMessage_async(self, _cb, session, text, current=None):
        # def hasPermission_async(self, _cb, session, channelid, perm, current=None):
        # def addContextCallback_async(self, _cb, session, action, text, cb, ctx, current=None):
        # def removeContextCallback_async(self, _cb, cb, current=None):
        # def getChannelState_async(self, _cb, channelid, current=None):
        # def setChannelState_async(self, _cb, state, current=None):
        # def removeChannel_async(self, _cb, channelid, current=None):
        # def addChannel_async(self, _cb, name, parent, current=None):
        # def sendMessageChannel_async(self, _cb, channelid, tree, text, current=None):
        # def getACL_async(self, _cb, channelid, current=None):
        # def setACL_async(self, _cb, channelid, acls, groups, inherit, current=None):
        # def addUserToGroup_async(self, _cb, channelid, session, group, current=None):
        # def removeUserFromGroup_async(self, _cb, channelid, session, group, current=None):
        # def redirectWhisperGroup_async(self, _cb, session, source, target, current=None):
        # def getUserNames_async(self, _cb, ids, current=None):
        # def getUserIds_async(self, _cb, names, current=None):
        # def registerUser_async(self, _cb, info, current=None):
        # def unregisterUser_async(self, _cb, userid, current=None):
        # def updateRegistration_async(self, _cb, userid, info, current=None):
        # def getRegistration_async(self, _cb, userid, current=None):
        # def getRegisteredUsers_async(self, _cb, filter, current=None):
        # def verifyPassword_async(self, _cb, name, pw, current=None):
        # def getTexture_async(self, _cb, userid, current=None):
        # def setTexture_async(self, _cb, userid, tex, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Server)

        __repr__ = __str__

    _M_Murmur.ServerPrx = Ice.createTempClass()
    class ServerPrx(Ice.ObjectPrx):

        def isRunning(self, _ctx=None):
            return _M_Murmur.Server._op_isRunning.invoke(self, (), _ctx)

        def start(self, _ctx=None):
            return _M_Murmur.Server._op_start.invoke(self, (), _ctx)

        def stop(self, _ctx=None):
            return _M_Murmur.Server._op_stop.invoke(self, (), _ctx)

        def delete(self, _ctx=None):
            return _M_Murmur.Server._op_delete.invoke(self, (), _ctx)

        def id(self, _ctx=None):
            return _M_Murmur.Server._op_id.invoke(self, (), _ctx)

        def addCallback(self, cb, _ctx=None):
            return _M_Murmur.Server._op_addCallback.invoke(self, (cb, ), _ctx)

        def removeCallback(self, cb, _ctx=None):
            return _M_Murmur.Server._op_removeCallback.invoke(self, (cb, ), _ctx)

        def setAuthenticator(self, auth, _ctx=None):
            return _M_Murmur.Server._op_setAuthenticator.invoke(self, (auth, ), _ctx)

        def getConf(self, key, _ctx=None):
            return _M_Murmur.Server._op_getConf.invoke(self, (key, ), _ctx)

        def getAllConf(self, _ctx=None):
            return _M_Murmur.Server._op_getAllConf.invoke(self, (), _ctx)

        def setConf(self, key, value, _ctx=None):
            return _M_Murmur.Server._op_setConf.invoke(self, (key, value), _ctx)

        def setSuperuserPassword(self, pw, _ctx=None):
            return _M_Murmur.Server._op_setSuperuserPassword.invoke(self, (pw, ), _ctx)

        def getLog(self, first, last, _ctx=None):
            return _M_Murmur.Server._op_getLog.invoke(self, (first, last), _ctx)

        def getUsers(self, _ctx=None):
            return _M_Murmur.Server._op_getUsers.invoke(self, (), _ctx)

        def getChannels(self, _ctx=None):
            return _M_Murmur.Server._op_getChannels.invoke(self, (), _ctx)

        def getTree(self, _ctx=None):
            return _M_Murmur.Server._op_getTree.invoke(self, (), _ctx)

        def getBans(self, _ctx=None):
            return _M_Murmur.Server._op_getBans.invoke(self, (), _ctx)

        def setBans(self, bans, _ctx=None):
            return _M_Murmur.Server._op_setBans.invoke(self, (bans, ), _ctx)

        def kickUser(self, session, reason, _ctx=None):
            return _M_Murmur.Server._op_kickUser.invoke(self, (session, reason), _ctx)

        def getState(self, session, _ctx=None):
            return _M_Murmur.Server._op_getState.invoke(self, (session, ), _ctx)

        def setState(self, state, _ctx=None):
            return _M_Murmur.Server._op_setState.invoke(self, (state, ), _ctx)

        def sendMessage(self, session, text, _ctx=None):
            return _M_Murmur.Server._op_sendMessage.invoke(self, (session, text), _ctx)

        def hasPermission(self, session, channelid, perm, _ctx=None):
            return _M_Murmur.Server._op_hasPermission.invoke(self, (session, channelid, perm), _ctx)

        def addContextCallback(self, session, action, text, cb, ctx, _ctx=None):
            return _M_Murmur.Server._op_addContextCallback.invoke(self, (session, action, text, cb, ctx), _ctx)

        def removeContextCallback(self, cb, _ctx=None):
            return _M_Murmur.Server._op_removeContextCallback.invoke(self, (cb, ), _ctx)

        def getChannelState(self, channelid, _ctx=None):
            return _M_Murmur.Server._op_getChannelState.invoke(self, (channelid, ), _ctx)

        def setChannelState(self, state, _ctx=None):
            return _M_Murmur.Server._op_setChannelState.invoke(self, (state, ), _ctx)

        def removeChannel(self, channelid, _ctx=None):
            return _M_Murmur.Server._op_removeChannel.invoke(self, (channelid, ), _ctx)

        def addChannel(self, name, parent, _ctx=None):
            return _M_Murmur.Server._op_addChannel.invoke(self, (name, parent), _ctx)

        def sendMessageChannel(self, channelid, tree, text, _ctx=None):
            return _M_Murmur.Server._op_sendMessageChannel.invoke(self, (channelid, tree, text), _ctx)

        def getACL(self, channelid, _ctx=None):
            return _M_Murmur.Server._op_getACL.invoke(self, (channelid, ), _ctx)

        def setACL(self, channelid, acls, groups, inherit, _ctx=None):
            return _M_Murmur.Server._op_setACL.invoke(self, (channelid, acls, groups, inherit), _ctx)

        def addUserToGroup(self, channelid, session, group, _ctx=None):
            return _M_Murmur.Server._op_addUserToGroup.invoke(self, (channelid, session, group), _ctx)

        def removeUserFromGroup(self, channelid, session, group, _ctx=None):
            return _M_Murmur.Server._op_removeUserFromGroup.invoke(self, (channelid, session, group), _ctx)

        def redirectWhisperGroup(self, session, source, target, _ctx=None):
            return _M_Murmur.Server._op_redirectWhisperGroup.invoke(self, (session, source, target), _ctx)

        def getUserNames(self, ids, _ctx=None):
            return _M_Murmur.Server._op_getUserNames.invoke(self, (ids, ), _ctx)

        def getUserIds(self, names, _ctx=None):
            return _M_Murmur.Server._op_getUserIds.invoke(self, (names, ), _ctx)

        def registerUser(self, info, _ctx=None):
            return _M_Murmur.Server._op_registerUser.invoke(self, (info, ), _ctx)

        def unregisterUser(self, userid, _ctx=None):
            return _M_Murmur.Server._op_unregisterUser.invoke(self, (userid, ), _ctx)

        def updateRegistration(self, userid, info, _ctx=None):
            return _M_Murmur.Server._op_updateRegistration.invoke(self, (userid, info), _ctx)

        def getRegistration(self, userid, _ctx=None):
            return _M_Murmur.Server._op_getRegistration.invoke(self, (userid, ), _ctx)

        def getRegisteredUsers(self, filter, _ctx=None):
            return _M_Murmur.Server._op_getRegisteredUsers.invoke(self, (filter, ), _ctx)

        def verifyPassword(self, name, pw, _ctx=None):
            return _M_Murmur.Server._op_verifyPassword.invoke(self, (name, pw), _ctx)

        def getTexture(self, userid, _ctx=None):
            return _M_Murmur.Server._op_getTexture.invoke(self, (userid, ), _ctx)

        def setTexture(self, userid, tex, _ctx=None):
            return _M_Murmur.Server._op_setTexture.invoke(self, (userid, tex), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.ServerPrx.ice_checkedCast(proxy, '::Murmur::Server', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.ServerPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_ServerPrx = IcePy.defineProxy('::Murmur::Server', ServerPrx)

    _M_Murmur._t_Server = IcePy.defineClass('::Murmur::Server', Server, True, None, (), ())
    Server.ice_type = _M_Murmur._t_Server

    Server._op_isRunning = IcePy.Operation('isRunning', Ice.OperationMode.Idempotent, True, (), (), IcePy._t_bool, ())
    Server._op_start = IcePy.Operation('start', Ice.OperationMode.Normal, True, (), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_ServerFailureException))
    Server._op_stop = IcePy.Operation('stop', Ice.OperationMode.Normal, True, (), (), None, (_M_Murmur._t_ServerBootedException,))
    Server._op_delete = IcePy.Operation('delete', Ice.OperationMode.Normal, True, (), (), None, (_M_Murmur._t_ServerBootedException,))
    Server._op_id = IcePy.Operation('id', Ice.OperationMode.Idempotent, True, (), (), IcePy._t_int, ())
    Server._op_addCallback = IcePy.Operation('addCallback', Ice.OperationMode.Normal, True, (_M_Murmur._t_ServerCallbackPrx,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidCallbackException))
    Server._op_removeCallback = IcePy.Operation('removeCallback', Ice.OperationMode.Normal, True, (_M_Murmur._t_ServerCallbackPrx,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidCallbackException))
    Server._op_setAuthenticator = IcePy.Operation('setAuthenticator', Ice.OperationMode.Normal, True, (_M_Murmur._t_ServerAuthenticatorPrx,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidCallbackException))
    Server._op_getConf = IcePy.Operation('getConf', Ice.OperationMode.Idempotent, True, (IcePy._t_string,), (), IcePy._t_string, ())
    Server._op_getAllConf = IcePy.Operation('getAllConf', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_ConfigMap, ())
    Server._op_setConf = IcePy.Operation('setConf', Ice.OperationMode.Idempotent, True, (IcePy._t_string, IcePy._t_string), (), None, ())
    Server._op_setSuperuserPassword = IcePy.Operation('setSuperuserPassword', Ice.OperationMode.Idempotent, True, (IcePy._t_string,), (), None, ())
    Server._op_getLog = IcePy.Operation('getLog', Ice.OperationMode.Idempotent, True, (IcePy._t_int, IcePy._t_int), (), _M_Murmur._t_LogList, ())
    Server._op_getUsers = IcePy.Operation('getUsers', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_UserMap, (_M_Murmur._t_ServerBootedException,))
    Server._op_getChannels = IcePy.Operation('getChannels', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_ChannelMap, (_M_Murmur._t_ServerBootedException,))
    Server._op_getTree = IcePy.Operation('getTree', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_Tree, (_M_Murmur._t_ServerBootedException,))
    Server._op_getBans = IcePy.Operation('getBans', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_BanList, (_M_Murmur._t_ServerBootedException,))
    Server._op_setBans = IcePy.Operation('setBans', Ice.OperationMode.Idempotent, True, (_M_Murmur._t_BanList,), (), None, (_M_Murmur._t_ServerBootedException,))
    Server._op_kickUser = IcePy.Operation('kickUser', Ice.OperationMode.Normal, True, (IcePy._t_int, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException))
    Server._op_getState = IcePy.Operation('getState', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (), _M_Murmur._t_User, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException))
    Server._op_setState = IcePy.Operation('setState', Ice.OperationMode.Idempotent, True, (_M_Murmur._t_User,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException, _M_Murmur._t_InvalidChannelException))
    Server._op_sendMessage = IcePy.Operation('sendMessage', Ice.OperationMode.Normal, True, (IcePy._t_int, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException))
    Server._op_hasPermission = IcePy.Operation('hasPermission', Ice.OperationMode.Normal, True, (IcePy._t_int, IcePy._t_int, IcePy._t_int), (), IcePy._t_bool, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException, _M_Murmur._t_InvalidChannelException))
    Server._op_addContextCallback = IcePy.Operation('addContextCallback', Ice.OperationMode.Normal, True, (IcePy._t_int, IcePy._t_string, IcePy._t_string, _M_Murmur._t_ServerContextCallbackPrx, IcePy._t_int), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidCallbackException))
    Server._op_removeContextCallback = IcePy.Operation('removeContextCallback', Ice.OperationMode.Normal, True, (_M_Murmur._t_ServerContextCallbackPrx,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidCallbackException))
    Server._op_getChannelState = IcePy.Operation('getChannelState', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (), _M_Murmur._t_Channel, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_setChannelState = IcePy.Operation('setChannelState', Ice.OperationMode.Idempotent, True, (_M_Murmur._t_Channel,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_removeChannel = IcePy.Operation('removeChannel', Ice.OperationMode.Normal, True, (IcePy._t_int,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_addChannel = IcePy.Operation('addChannel', Ice.OperationMode.Normal, True, (IcePy._t_string, IcePy._t_int), (), IcePy._t_int, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_sendMessageChannel = IcePy.Operation('sendMessageChannel', Ice.OperationMode.Normal, True, (IcePy._t_int, IcePy._t_bool, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_getACL = IcePy.Operation('getACL', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (_M_Murmur._t_ACLList, _M_Murmur._t_GroupList, IcePy._t_bool), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_setACL = IcePy.Operation('setACL', Ice.OperationMode.Idempotent, True, (IcePy._t_int, _M_Murmur._t_ACLList, _M_Murmur._t_GroupList, IcePy._t_bool), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException))
    Server._op_addUserToGroup = IcePy.Operation('addUserToGroup', Ice.OperationMode.Idempotent, True, (IcePy._t_int, IcePy._t_int, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException, _M_Murmur._t_InvalidSessionException))
    Server._op_removeUserFromGroup = IcePy.Operation('removeUserFromGroup', Ice.OperationMode.Idempotent, True, (IcePy._t_int, IcePy._t_int, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidChannelException, _M_Murmur._t_InvalidSessionException))
    Server._op_redirectWhisperGroup = IcePy.Operation('redirectWhisperGroup', Ice.OperationMode.Idempotent, True, (IcePy._t_int, IcePy._t_string, IcePy._t_string), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidSessionException))
    Server._op_getUserNames = IcePy.Operation('getUserNames', Ice.OperationMode.Idempotent, True, (_M_Murmur._t_IdList,), (), _M_Murmur._t_NameMap, (_M_Murmur._t_ServerBootedException,))
    Server._op_getUserIds = IcePy.Operation('getUserIds', Ice.OperationMode.Idempotent, True, (_M_Murmur._t_NameList,), (), _M_Murmur._t_IdMap, (_M_Murmur._t_ServerBootedException,))
    Server._op_registerUser = IcePy.Operation('registerUser', Ice.OperationMode.Normal, True, (_M_Murmur._t_UserInfoMap,), (), IcePy._t_int, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException))
    Server._op_unregisterUser = IcePy.Operation('unregisterUser', Ice.OperationMode.Normal, True, (IcePy._t_int,), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException))
    Server._op_updateRegistration = IcePy.Operation('updateRegistration', Ice.OperationMode.Idempotent, True, (IcePy._t_int, _M_Murmur._t_UserInfoMap), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException))
    Server._op_getRegistration = IcePy.Operation('getRegistration', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (), _M_Murmur._t_UserInfoMap, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException))
    Server._op_getRegisteredUsers = IcePy.Operation('getRegisteredUsers', Ice.OperationMode.Idempotent, True, (IcePy._t_string,), (), _M_Murmur._t_NameMap, (_M_Murmur._t_ServerBootedException,))
    Server._op_verifyPassword = IcePy.Operation('verifyPassword', Ice.OperationMode.Idempotent, True, (IcePy._t_string, IcePy._t_string), (), IcePy._t_int, (_M_Murmur._t_ServerBootedException,))
    Server._op_getTexture = IcePy.Operation('getTexture', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (), _M_Murmur._t_Texture, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException))
    Server._op_setTexture = IcePy.Operation('setTexture', Ice.OperationMode.Idempotent, True, (IcePy._t_int, _M_Murmur._t_Texture), (), None, (_M_Murmur._t_ServerBootedException, _M_Murmur._t_InvalidUserException, _M_Murmur._t_InvalidTextureException))

    _M_Murmur.Server = Server
    del Server

    _M_Murmur.ServerPrx = ServerPrx
    del ServerPrx

if not _M_Murmur.__dict__.has_key('MetaCallback'):
    _M_Murmur.MetaCallback = Ice.createTempClass()
    class MetaCallback(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.MetaCallback:
                raise RuntimeError('Murmur.MetaCallback is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::MetaCallback')

        def ice_id(self, current=None):
            return '::Murmur::MetaCallback'

        #
        # Operation signatures.
        #
        # def started(self, srv, current=None):
        # def stopped(self, srv, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_MetaCallback)

        __repr__ = __str__

    _M_Murmur.MetaCallbackPrx = Ice.createTempClass()
    class MetaCallbackPrx(Ice.ObjectPrx):

        def started(self, srv, _ctx=None):
            return _M_Murmur.MetaCallback._op_started.invoke(self, (srv, ), _ctx)

        def stopped(self, srv, _ctx=None):
            return _M_Murmur.MetaCallback._op_stopped.invoke(self, (srv, ), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.MetaCallbackPrx.ice_checkedCast(proxy, '::Murmur::MetaCallback', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.MetaCallbackPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_MetaCallbackPrx = IcePy.defineProxy('::Murmur::MetaCallback', MetaCallbackPrx)

    _M_Murmur._t_MetaCallback = IcePy.defineClass('::Murmur::MetaCallback', MetaCallback, True, None, (), ())
    MetaCallback.ice_type = _M_Murmur._t_MetaCallback

    MetaCallback._op_started = IcePy.Operation('started', Ice.OperationMode.Normal, False, (_M_Murmur._t_ServerPrx,), (), None, ())
    MetaCallback._op_stopped = IcePy.Operation('stopped', Ice.OperationMode.Normal, False, (_M_Murmur._t_ServerPrx,), (), None, ())

    _M_Murmur.MetaCallback = MetaCallback
    del MetaCallback

    _M_Murmur.MetaCallbackPrx = MetaCallbackPrx
    del MetaCallbackPrx

if not _M_Murmur.__dict__.has_key('_t_ServerList'):
    _M_Murmur._t_ServerList = IcePy.defineSequence('::Murmur::ServerList', _M_Murmur._t_ServerPrx)

if not _M_Murmur.__dict__.has_key('Meta'):
    _M_Murmur.Meta = Ice.createTempClass()
    class Meta(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_Murmur.Meta:
                raise RuntimeError('Murmur.Meta is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::Murmur::Meta')

        def ice_id(self, current=None):
            return '::Murmur::Meta'

        #
        # Operation signatures.
        #
        # def getServer_async(self, _cb, id, current=None):
        # def newServer_async(self, _cb, current=None):
        # def getBootedServers_async(self, _cb, current=None):
        # def getAllServers_async(self, _cb, current=None):
        # def getDefaultConf_async(self, _cb, current=None):
        # def getVersion_async(self, _cb, current=None):
        # def addCallback_async(self, _cb, cb, current=None):
        # def removeCallback_async(self, _cb, cb, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_Murmur._t_Meta)

        __repr__ = __str__

    _M_Murmur.MetaPrx = Ice.createTempClass()
    class MetaPrx(Ice.ObjectPrx):

        def getServer(self, id, _ctx=None):
            return _M_Murmur.Meta._op_getServer.invoke(self, (id, ), _ctx)

        def newServer(self, _ctx=None):
            return _M_Murmur.Meta._op_newServer.invoke(self, (), _ctx)

        def getBootedServers(self, _ctx=None):
            return _M_Murmur.Meta._op_getBootedServers.invoke(self, (), _ctx)

        def getAllServers(self, _ctx=None):
            return _M_Murmur.Meta._op_getAllServers.invoke(self, (), _ctx)

        def getDefaultConf(self, _ctx=None):
            return _M_Murmur.Meta._op_getDefaultConf.invoke(self, (), _ctx)

        def getVersion(self, _ctx=None):
            return _M_Murmur.Meta._op_getVersion.invoke(self, (), _ctx)

        def addCallback(self, cb, _ctx=None):
            return _M_Murmur.Meta._op_addCallback.invoke(self, (cb, ), _ctx)

        def removeCallback(self, cb, _ctx=None):
            return _M_Murmur.Meta._op_removeCallback.invoke(self, (cb, ), _ctx)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Murmur.MetaPrx.ice_checkedCast(proxy, '::Murmur::Meta', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=''):
            return _M_Murmur.MetaPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_Murmur._t_MetaPrx = IcePy.defineProxy('::Murmur::Meta', MetaPrx)

    _M_Murmur._t_Meta = IcePy.defineClass('::Murmur::Meta', Meta, True, None, (), ())
    Meta.ice_type = _M_Murmur._t_Meta

    Meta._op_getServer = IcePy.Operation('getServer', Ice.OperationMode.Idempotent, True, (IcePy._t_int,), (), _M_Murmur._t_ServerPrx, ())
    Meta._op_newServer = IcePy.Operation('newServer', Ice.OperationMode.Normal, True, (), (), _M_Murmur._t_ServerPrx, ())
    Meta._op_getBootedServers = IcePy.Operation('getBootedServers', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_ServerList, ())
    Meta._op_getAllServers = IcePy.Operation('getAllServers', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_ServerList, ())
    Meta._op_getDefaultConf = IcePy.Operation('getDefaultConf', Ice.OperationMode.Idempotent, True, (), (), _M_Murmur._t_ConfigMap, ())
    Meta._op_getVersion = IcePy.Operation('getVersion', Ice.OperationMode.Idempotent, True, (), (IcePy._t_int, IcePy._t_int, IcePy._t_int, IcePy._t_string), None, ())
    Meta._op_addCallback = IcePy.Operation('addCallback', Ice.OperationMode.Normal, True, (_M_Murmur._t_MetaCallbackPrx,), (), None, (_M_Murmur._t_InvalidCallbackException,))
    Meta._op_removeCallback = IcePy.Operation('removeCallback', Ice.OperationMode.Normal, True, (_M_Murmur._t_MetaCallbackPrx,), (), None, (_M_Murmur._t_InvalidCallbackException,))

    _M_Murmur.Meta = Meta
    del Meta

    _M_Murmur.MetaPrx = MetaPrx
    del MetaPrx

# End of module Murmur
