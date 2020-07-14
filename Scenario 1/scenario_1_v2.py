import lgsvl
import time
import json
import lgsvl.scenario.utils as su
from lgsvl.geometry import Vector, Transform
import os


def simulate_from_matlab(ego_and_agents_config=[], sim_duration=15000,
                         for_matlab=False, agent_waypoint=[], ego_waypoint=[]):
    # Simulation Configuration
    simulator_config = su.SimulatorConfig()
    simulator_config.simulation_duration = sim_duration

    # Bridge Configuration
    bridge_config = su.BridgeConfig()

    # Parse ego and agents initial conditions
    vehicles_config = {}
    ego_and_agents_config = ego_and_agents_config.tolist()

    ego_position_y = -4  # EGO POSITION Y
    vehicles_config['ego'] = {
        'position': Vector(ego_and_agents_config[0], ego_position_y, ego_and_agents_config[1]),
        'initial_speed': ego_and_agents_config[3]
    }
    agent_1_position_y = -4  # AGENT 1 POSITION Y
    vehicles_config['agent_1'] = {
        'position': Vector(ego_and_agents_config[4], agent_1_position_y, agent_waypoint[0][2]),
        'initial_speed': ego_and_agents_config[6]
    }
    agent_2_position_y = -4  # AGENT 2 POSITION Y
    vehicles_config['agent_2'] = {
        'position': Vector(ego_and_agents_config[7], agent_2_position_y, agent_waypoint[0][4]),
        'initial_speed': ego_and_agents_config[9]
    }

    # Parse ego and agent waypoints
    waypoints_config = {}

    simulate(simulator_config, bridge_config, vehicles_config, waypoints_config)


def simulate_from_file(simulation_config, vehicles_config, waypoints_config):
    # simulation configuration
    with open('simulation_config.json') as json_file:
        simulation_config = json.load(json_file)
    simulator_config = simulation_config['simulator']
    bridge_config = simulation_config['bridge']

    # vehicles configuration
    with open('vehicles_config.json') as json_file:
        vehicles_config = json.load(json_file)

    # Parse ego and agent waypoints
    waypoints_config = {}

    simulate(simulator_config, bridge_config, vehicles_config, waypoints_config)


def simulate(simulator_config, bridge_config, vehicles_config, waypoints_config):
    # Initialize simulator
    sim = simulator_config.initialize()

    # Spawn vehicles
    # spawn EGO
    ego_initial_state = lgsvl.AgentState()
    ego_initial_state.transform = \
        sim.map_point_on_lane(vehicles_config['ego'].position)
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, ego_initial_state)
    ego.connect_bridge(bridge_config.host, bridge_config.port)

    # Spawn Agents
    # Agent 1
    agent_1_initial_state = lgsvl.AgentState()
    agent_1_initial_state.transform = \
        sim.map_point_on_lane(vehicles_config['agent_1'].position)
    agent_1 = sim.add_agent("Sedan", lgsvl.AgentType.EGO, ego_initial_state)

    # Agent 2
    agent_2_initial_state = lgsvl.AgentState()
    agent_2_initial_state.transform = \
        sim.map_point_on_lane(vehicles_config['agent_2'].position)
    agent_2 = sim.add_agent("Sedan", lgsvl.AgentType.EGO, ego_initial_state)

    # Run Simulation
    t0 = time.time()
    sim.run(simulator_config.initialization_time)
    # agent_1.follow(agent_1_waypoints)
    # agent_2.follow(agent_2_waypoints)
    while True:
        sim.run(1)
        time.sleep(0.1)
        if (time.time() - t0) > simulator_config.duration:
            break
