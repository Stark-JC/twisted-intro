from twisted.internet.defer import Deferred

def status(*ds):
    return [(getattr(d,'result',"N/A"), len(d.callbacks)) for d in ds]

def b_callback(arg):
    print "b_callback called with arg =", arg
    return b

def on_done(arg):
    print "on_done called with arg =", arg
    return arg

a = Deferred()
b = Deferred()
a.addCallback(b_callback).addCallback(on_done)