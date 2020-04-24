import lgsvl
import time
import json
from lgsvl.geometry import Vector, Transform
import os

# Simulation Configuration
SIMULATOR_HOST = "127.0.0.1"
BRIDGE_HOST = "127.0.0.1"
SIM_INITIALIZE_TIME = 2
SIM_TIME_LIMIT = 30

# scenario configuration
with open('config.json') as json_file:
    scenario_config = json.load(json_file)

with open('parameters.json') as json_file:
    scenario_parameters = json.load(json_file)

# Intersections
ego_intersection_transform = Transform.from_json(scenario_config["ego_intersection"]['transform'])
agent_1_intersection_transform = Transform.from_json(scenario_config["agent_1_intersection"]['transform'])
agent_2_intersection_transform = Transform.from_json(scenario_config["agent_2_intersection"]['transform'])

# Waypoints
with open('waypoints.json') as json_file:
    scenario_waypoints = json.load(json_file)

# Agent 1 Way Points
agent_1_waypoints = []
for waypoint in scenario_waypoints['agent_1']:
    agent_1_waypoints.append(lgsvl.agent.DriveWaypoint(Vector.from_json(waypoint['position']),
                                                       waypoint['speed'],
                                                       Vector.from_json(waypoint['angle']),
                                                       waypoint['idle'],
                                                       waypoint['deactivate'],
                                                       waypoint['trigger_distance'],
                                                       waypoint['timestamp']))

# Agent 2 Way Points
agent_2_waypoints = []
for waypoint in scenario_waypoints['agent_2']:
    agent_2_waypoints.append(lgsvl.agent.DriveWaypoint(Vector.from_json(waypoint['position']),
                                                       waypoint['speed'],
                                                       Vector.from_json(waypoint['angle']),
                                                       waypoint['idle'],
                                                       waypoint['deactivate'],
                                                       waypoint['trigger_distance'],
                                                       waypoint['timestamp']))

# Connect to simulator
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

# Set the map scene
if sim.current_scene == scenario_config['map']:
    sim.reset()
else:
    sim.load(scenario_config['map'])

# Set initial time of the day for the simulation
sim.set_time_of_day(12)

# spawn EGO
ego_initial_state = lgsvl.AgentState()
ego_initial_state.transform = \
    sim.map_point_on_lane(ego_intersection_transform.position
                          - (scenario_parameters['ego']["distance_to_intersection"]
                             * lgsvl.utils.transform_to_forward(ego_intersection_transform)))
ego = sim.add_agent(scenario_config['ego_vehicle'], lgsvl.AgentType.EGO, ego_initial_state)
ego.connect_bridge(BRIDGE_HOST, 9090)

# Spawn Agents
# Agent 1
agent_1_initial_state = lgsvl.AgentState()
agent_1_initial_state.transform = \
    sim.map_point_on_lane(agent_1_intersection_transform.position
                          - (scenario_parameters['agent_1']["distance_to_intersection"]
                             * lgsvl.utils.transform_to_forward(agent_1_intersection_transform)))
agent_1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, agent_1_initial_state)


# Agent 2
agent_2_initial_state = lgsvl.AgentState()
agent_2_initial_state.transform = \
    sim.map_point_on_lane(agent_2_intersection_transform.position
                          - (scenario_parameters['agent_2']["distance_to_intersection"]
                             * lgsvl.utils.transform_to_forward(agent_2_intersection_transform)))
agent_2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, agent_2_initial_state)


# Run Simulation
t0 = time.time()
sim.run(SIM_INITIALIZE_TIME)
agent_1.follow(agent_1_waypoints)
agent_2.follow(agent_2_waypoints)
while True:
    sim.run(1)
    time.sleep(0.1)
    if (time.time() - t0) > SIM_TIME_LIMIT:
        break
