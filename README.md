ThriftyArena
============

Reimplementation of Arena using [Thrift](http://http://thrift.apache.org/) to facilitate communication between the controller and the simulator.

The communication protocol has several methods:

initSim() begins the simulation by creating a pendulum simulator object and returning the intiial condition

step(force) takes the forcing function value for that time point as the input argument and returns the system's state and the end of the step.

## To Do
* Change the thrift protocol to pass the state variables as as struct instead of a list

* Create a logging system on the server side and a method to retreive the log
