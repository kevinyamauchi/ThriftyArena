import sys, glob

# Add the thrift-generated python files to the path
sys.path.append('gen-py')

from simulator import simComm
from simulator.ttypes import *

from thrift import Thrift # requires python bindings
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:

    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is required because the socket is slow
    trnasport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = simComm.Client(protocol)

    # Connect
    transport.open()

    client.ping()

    initialConditions = client.initSim()

    print initialConditions

    nextStep = client.step(5)

    print nextStep

    transport.close()

except Thrift.TException, tx:
    print '%s' % (tx.message)

