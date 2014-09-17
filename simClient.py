import sys, glob

# Add the thrift-generated python files to the path
sys.path.append('gen-py')

from simulator import simComm
from simulator.ttypes import *

from thrift import Thrift # requires python bindings
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from numpy import zeros

import matplotlib.pyplot as plt

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

    # Start the simulation and get the initial condition
    x = client.initSim()

    print x

    # Initialize the state history
    state_history = ()
    state_history += (x, )

    print state_history

    # Set the forcing function to zero
    us = zeros(1000)

    # Step 1000 times
    for u in us:

        x = client.step(u)
        state_history += (x,)



    transport.close()

except Thrift.TException, tx:
    print '%s' % (tx.message)

# Get the state variable time history
x1s = [x for x, _, _, _ in state_history]
x2s = [x for _, x, _, _ in state_history]

u1s = [u for _, _, u, _ in state_history]
u2s = [u for _, _, _, u in state_history]

# Plot the state variable time history
plt.plot(x1s)
plt.plot(x2s)

plt.figure()
plt.plot(u1s)
plt.plot(u2s)

plt.show()
