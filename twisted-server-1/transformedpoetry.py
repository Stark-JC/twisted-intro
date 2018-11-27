# -*-coding:utf-8 -*-
# This is the Twisted Poetry Transform Server, version 1.0

import optparse

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import NetstringReceiver


def parse_args():
    usage = """usage: %prog [options]

This is the Poetry Transform Server.
Run it like this:

  python transformedpoetry.py

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/transformedpoetry.py --port 11000

to provide poetry transformation on port 11000.
"""

    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port', type='int', help=help)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()

    if len(args) != 0:
        parser.error('Bad arguments.')

    return options


class TransformService(object):
    '''
    格式转换服务与具体协议实现分离，这样做可以通过多种协议实现同一种服务，以增加了代码的重用性。
    '''

    def cummingsify(self, poem):
        return poem.lower()


class TransformProtocol(NetstringReceiver):
    '''
    继承后底层实现了编解码功能，我们只需实现stringRecevied方法，基类同样管理着缓冲区，即当一首诗歌完整接收完再进行解码。
    '''
    def stringReceived(self, request):
        if '.' not in request: # bad request
            print("Got a bad request, disconnect with client-----")
            self.transport.loseConnection()
            return

        print("Got a proper request, start to transform----")
        xform_name, poem = request.split('.', 1)

        self.xformRequestReceived(xform_name, poem)

    def xformRequestReceived(self, xform_name, poem):
        new_poem = self.factory.transform(xform_name, poem)

        if new_poem is not None:
            print("Sending back the transformed request----")
            self.sendString(new_poem)

        self.transport.loseConnection()


class TransformFactory(ServerFactory):

    protocol = TransformProtocol

    def __init__(self, service):
        self.service = service

    def transform(self, xform_name, poem):
        thunk = getattr(self, 'xform_%s' % (xform_name,), None)

        if thunk is None: # no such transform
            return None

        try:
            return thunk(poem)
        except:
            return None # transform failed

    def xform_cummingsify(self, poem):
        return self.service.cummingsify(poem)


def main():
    options = parse_args()

    service = TransformService()

    factory = TransformFactory(service)

    from twisted.internet import reactor

    port = reactor.listenTCP(options.port or 0, factory,
                             interface=options.iface)

    print 'Serving transforms on %s.' % (port.getHost(),)

    reactor.run()


if __name__ == '__main__':
    main()
