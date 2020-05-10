import lgsvl
import os
import time
from lgsvl.geometry import Vector, Transform

# Simulation Configuration
SIMULATOR_HOST = "127.0.0.1"
BRIDGE_HOST = "127.0.0.1"
SIM_INITIALIZE_TIME = 2
SIM_TIME_LIMIT = 10

# Connect to simulator
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

# Set the map scene
if sim.current_scene == "BorregasAve":
    sim.reset()
else:
    sim.load("BorregasAve")

# Set initial time of the day for the simulation
sim.set_time_of_day(12)

#
initial_transform = sim.map_point_on_lane(sim.get_spawn()[0].position)
initial_transform.position.x += 1.5

# spawn EGO
npc_initial_state = lgsvl.AgentState()
print(sim.get_spawn()[0])
print(initial_transform)
npc_initial_state.transform = initial_transform
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, ego_initial_state)

# Run Simulation
t0 = time.time()
sim.run(SIM_INITIALIZE_TIME)
while True:
    sim.run(1)
    time.sleep(0.1)
    if (time.time() - t0) > SIM_TIME_LIMIT:
        break