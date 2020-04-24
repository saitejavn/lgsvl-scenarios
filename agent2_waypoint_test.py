import lgsvl
import os

# Simulation Configuration
SIMULATOR_HOST = "localhost"
BRIDGE_HOST = "localhost"
MAP = "BorregasAve"


AGENT2_INTERSECTION_POSITION = lgsvl.Vector(-6.700272, -1.926125, 1.748038)
AGENT2_INTERSECTION_ROTATION = lgsvl.Vector(0.563, -73.79601, -0.274)
AGENT2_DESTINATION_POSITION = lgsvl.Vector(-28.12951, -2.466399, -18.73548)
AGENT2_DESTINATION_ROTATION = lgsvl.Vector(1.227, -163.168, -0.668)
AGENT2_SPEED_DESTINATION = 10

# Connect to simulator
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

# Set the map scene
if sim.current_scene == MAP:
    sim.reset()
else:
    sim.load(MAP)


spawns = sim.get_spawn()

# testing for destination waypoint behaviour
state = lgsvl.AgentState()


#spawn the npc vehicle on intersection
state.transform.position = AGENT2_INTERSECTION_POSITION
state.transform.rotation = AGENT2_INTERSECTION_ROTATION

npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

#creating a list of waypoint for the ego vehicle
waypoints = []

#adding a destination waypoint as the only wp for testing
dest_wp = lgsvl.DriveWaypoint(AGENT2_DESTINATION_POSITION, speed=AGENT2_SPEED_DESTINATION, angle=AGENT2_DESTINATION_ROTATION, idle=5)
waypoints.append(dest_wp)

npc.follow(waypoints)

sim.run(5)