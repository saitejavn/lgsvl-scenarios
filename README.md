# lgsvl-scenarios

* This repository contains code for running scenarios for adversarial testing of Autonomous Vehicles using the open source photorealistic simulator [LGSVL](https://www.lgsvlsimulator.com/).
* The Perception, Prediction, Planning and Control is done by the AD stack Apollo which communicates with the simulator using the Cyber RT bridge.
* The example scenario is taken from the follwing research work:

[1] *Simulation-based Adversarial Test Generation for Autonomous Vehicles with Machine Learning Components*  
C.E. Tuncali, G. Fainekos, H. Ito, J. Kapinski,  
IEEE Intelligent Vehicles Symposium, 2018  
[@arxiv](https://arxiv.org/abs/1804.06760)
[@staliro-references](https://sites.google.com/a/asu.edu/s-taliro/references)

[2] *Sim-ATAV: Simulation-Based Adversarial Testing Framework for Autonomous Vehicles*  
C.E. Tuncali, G. Fainekos, H. Ito, J. Kapinski,  
Proceedings of the 21st International Conference on Hybrid Systems: Computation and Control (part of CPS Week), 2018  
[@staliro-references](https://sites.google.com/a/asu.edu/s-taliro/references)

Quoting the scenario as mentioned in [Sim-ATAV](https://github.com/tuncali/sim-atav):

## Example Scenario

![](scenario1.png)

In this example scenario, the Ego vehicle is making a left turn at an intersection.
An agent vehicle (Agent 2) is also making a left turn from the other side of the intersection.
Another agent vehicle (Agent 1) is running a red light and creating a collision risk with the Ego vehicle.
Ego vehicle should be able to detect the Agent 1 and avoid a collision. 

The paper's goal is to search for a set of parameter values that cause the perception system on the Ego vehicle to fail and result in a collision.
The parameters used in the test generation are:  

- Ego initial speed,  
- Ego initial distance to the intersection,  
- Agent 1 initial distance to the intersection,  
- Agent 1 initial speed,  
- Agent 1 speed when approaching the intersection,  
- Agent 1 speed inside the intersection,  
- Agent 1 initial lateral position,  
- Agent 1 target lateral position when approaching the intersection,  
- Agent 1 target lateral position inside the intersection,  
- Agent 2 initial lateral position,  
- Agent 2 speed,  
- Agent 2 initial distance to the intersection.

## Interface with MATLAB test generation framework and Simulator Python API
* These parameters can directly be passed from the Matlab test generation framework used in sim-atav or by generating a JSON file through any other test generation framework.
* The scenarios are generated by using the [LGSVL Python API](https://github.com/lgsvl/PythonAPI) which needs to be installed and added to the import paths.
