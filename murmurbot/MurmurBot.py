import time

import Murmur
VERSION = '0.1'


class MetaCallbackI(Murmur.MetaCallback):
    def __init__(self, meta, adapter):
        for server in meta.getBootedServers():
            serverR = Murmur.ServerCallbackPrx.uncheckedCast(
                    adapter.addWithUUID(ServerCallbackI(server, adapter)))
            server.addCallback(serverR)

    def started(self):
        self.bot.say("started")

class ServerCallbackI(Murmur.ServerCallback):
    def __init__(self, server, adapter):
        self.server = server
        self.server.sendMessageChannel(0, True,
                "ServerCallback for server %s created" % server)
        self.contextR = Murmur.ServerContextCallbackPrx.uncheckedCast(
                adapter.addWithUUID(ServerContextCallbackI(server, adapter)))

    def userConnected(self, p, current=None):
        self.server.addContextCallback(
                p.session, "something", "someothertthing", self.contextR,
                Murmur.ContextServer |
                Murmur.ContextChannel |
                Murmur.ContextUser)
        print 'user connected: %r' % p
        print 'added context callback'

class ServerContextCallbackI(Murmur.ServerContextCallback):
    def __init__(self, server, adapter):
        self.server = server

    def contextAction(self, action, p, session, chanid, current=None):
        print 'contextAction: %r' % locals()
        self.server.sendMessageChannel(0, True, repr(locals()))


class MurmurBot:
    def __init__(self, ic):
        self.ic = ic

    def run(self):
        self.say("MurmurBot %s starting..." % VERSION)

        self.meta = meta = Murmur.MetaPrx.checkedCast(
                self.ic.stringToProxy("Meta:tcp -h 127.0.0.1 -p 6502"))
        self.adapter = adapter = self.ic.createObjectAdapterWithEndpoints(
                "Callback.Client", "tcp -h 127.0.0.1")
        adapter.activate()
        metaR = Murmur.MetaCallbackPrx.uncheckedCast(
            adapter.addWithUUID(MetaCallbackI(meta, adapter)))
        meta.addCallback(metaR)

        """
        metaR = Murmur.MetaCallbackPrx.uncheckedCast(adapter.addWithUUID(
            MetaCallbackI(self))

        serverR = Murmur.ServerCallbackPrx.uncheckedCast(
                adapter.addWithUUID(ServerCallbackI(self)))
        self.say('adapter=%r' % adapter)
        self.server.addCallback(serverR)
        """

        try:
            self.ic.waitForShutdown()
        except:
            print 'removing meta callback'
            meta.removeCallback(metaR)
            raise

    def say(self, text):
        print 'say(%s)' % text
        #self.server.sendMessageChannel(0, True, text)
