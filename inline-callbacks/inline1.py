from twisted.internet.defer import Deferred

def callback1(arg):
    print 'first callback'
    return 1

def callback2(arg):
    print 'second callback got', arg
    d = Deferred()
    reactor.callLater(5, d.callback, 2)
    return d

def callback3(arg):
    print 'third callback got', arg
    d = Deferred()
    reactor.callLater(5, d.errback, Exception(3))
    return d

def errback4(err):
    print 'fourth callback got', repr(err)
    reactor.stop()

from twisted.internet import reactor
d = Deferred()
d.addCallback(callback1)
d.addCallback(callback2)
d.addCallback(callback3)
d.addErrback(errback4)

reactor.callWhenRunning(d.callback, None)
reactor.run()


