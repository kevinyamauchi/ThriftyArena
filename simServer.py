import sys, glob
sys.path.append('gen-py')

from simulator import simComm
from simulator.ttypes import *

from thrift.transport import TSocket, TTransport

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from numpy import pi, ones, hstack

# Import the pendulum simulator
from secord import pendulumFactory

############################################################################
#
#   Handler for the simulator communication
#
#
############################################################################

class simCommHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print 'ping()'

    # This method starts the simulation and returns this intial conditions
    def initSim(self):
        print 'initSim()'

        # Create the pendulum simulator object
        self._myPend = pendulumFactory()

        return hstack((0, 3 * pi / 4, 1e-3 * ones(2) ))

    # Method to step the simulation. Takes the forcing function, returns
    # the new state
    def step(self, u):
        print 'step()'

        return self._myPend(u)

    def endSim(self):

        return FALSE

###########################################################################
#
#   Server set up script
#
#
############################################################################

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
