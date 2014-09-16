import sys, glob
sys.path.append('gen-py')

from simulator import simComm
from simulator.ttypes import *

from thrift.transport import TSocket, TTransport

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

