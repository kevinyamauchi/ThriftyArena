import sys, glob
sys.path.append('gen-py')

from simulator import simComm
from simulator.ttypes import *

from thrift.transport import TSocket, TTransport

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class simCommHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print 'ping()'

    def initSim(self):
        print 'initSim()'

        return [1,2,3,4]

    def step(self, u):
        print 'step()'

        return [u, 2, 3, 4]

    def endSim(self):

        return FALSE

handler = simCommHandler()
processor = simComm.Processor(handler)
transport = TSocket.TServerSocket(port = 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# Serve 'em up
print 'Starting the server...'
server.serve()

print 'done'


