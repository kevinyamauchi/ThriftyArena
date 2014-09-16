/**

simcomm

Simulator is a service for handling communication between the controller (client) and the Arena simulator (server).


Methods:



*/

// Reserve namespace in the all the languages
namespace cpp simcomm
namespace d simcomm
namespace java simcomm

// Struct to hold the state information
struct stateVars {

  1: i32 x1,
  2: i32 x2,
  3: i32 x3,
  4: i32 x4;

}

/**


    Service (simComm) definition


*/


service simComm {

  void ping();

  // Method to start the problem
  list<i32> initSim();

  // Method to perform the next iteration
  list<i32> step(1: i32 force);

  // Method to end the challene
  bool endSim();

}
