from twisted.internet import reactor, defer

class Getter:
    def gotResults(self, x):
        """
        The Deferred mechanism provides a mechanism to signal error
        conditions.  In this case, odd numbers are bad.

        This function demonstrates a more complex way of starting
        the callback chain by checking for expected results and
        choosing whether to fire the callback or errback chain
        """
        if self.d is None:
            print("Nowhere to put results")
            return

        d = self.d
        self.d = None
        if x % 2 == 0:
            d.callback(x*3)
        else:
            d.errback(ValueError("You used an odd number!"))

    def _toHTML(self, r):
        """
        This function converts r to HTML.

        It is added to the callback chain by getDummyData in
        order to demonstrate how a callback passes its own result
        to the next callback
        """
        return "Result: %s" % r

    def pass_through(self, arg, name):
        print(name + " pass through")
        return arg

    def getDummyData(self, x):
        """
        The Deferred mechanism allows for chained callbacks.
        In this example, the output of gotResults is first
        passed through _toHTML on its way to printData.

        Again this function is a dummy, simulating a delayed result
        using callLater, rather than using a real asynchronous
        setup.
        """
        self.d = defer.Deferred()
        # simulate a delayed result by asking the reactor to schedule
        # gotResults in 2 seconds time
        reactor.callLater(2, self.gotResults, x)
        self.d.addCallbacks(self._toHTML, self.pass_through, errbackArgs=['to_html'])
        return self.d

def double(arg):
    return arg*2

def block(arg):
    d = defer.Deferred()
    d.addCallback(double)
    reactor.callLater(2, d.callback, 233)
    return d

def cbPrintData(result):
    print(result)

def ebPrintError(failure):
    import sys
    sys.stderr.write(str(failure))

# this series of callbacks and errbacks will print an error message
g = Getter()
d = g.getDummyData(3)
d.addCallbacks(cbPrintData,g.pass_through, errbackArgs=['cbPrintData'])
d.addCallbacks(g.pass_through, ebPrintError, callbackArgs=['cbPrintError'])
d.addBoth(block)
d.addCallbacks(cbPrintData,g.pass_through, errbackArgs=['cbPrintData'])

# this series of callbacks and errbacks will print "Result: 12"
# g = Getter()
# d = g.getDummyData(4)
# d.addCallbacks(cbPrintData,g.pass_through, errbackArgs=['cbPrintData'])
# d.addCallbacks(g.pass_through, ebPrintError, callbackArgs=['cbPrintError'])

reactor.run()