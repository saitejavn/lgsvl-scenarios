import lgsvl
import os
import json

# Simulation Configuration
SIMULATOR_HOST = "localhost"
BRIDGE_HOST = "localhost"
MAP = "BorregasAve"
SPEED = 6
AGENT1_INTERSECTION_POSITION = lgsvl.Vector(-31.46246, -2.040497, 2.334152)
AGENT1_INTERSECTION_ROTATION = lgsvl.Vector(0.301, 105.532, -1.382)
AGENT2_INTERSECTION_POSITION = lgsvl.Vector(-30.3782, -1.951178, 5.902245)
AGENT2_INTERSECTION_ROTATION = lgsvl.Vector(0.301, 105.532, -1.382)

def waypoint_collector(pos, rot, buffer_time):
    #spawn the npc vehicle on intersection
    state = lgsvl.AgentState()
    state.transform.position = pos
    state.transform.rotation = rot
    npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

    #creating a list of waypoint for the npc vehicle
    waypoints = []
    npc.follow_closest_lane(True, SPEED)
    sim.run(0.5)

    #waypoint collector
    for i in range(20):
        tf = npc.transform
        wp = lgsvl.DriveWaypoint(tf.position, speed=SPEED,
                                 angle=tf.rotation, idle=0)
        waypoints.append(wp)
        sim.run(buffer_time)
    sim.remove_agent(npc)
    return waypoints


def waypoint_follow_test(waypoints, pos, rot):
    state = lgsvl.AgentState()
    state.transform.position = pos
    state.transform.rotation = rot
    npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)
    npc.follow(waypoints)
    sim.run(10)


# Connect to simulator
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

# Set the map scene
if sim.current_scene == MAP:
    sim.reset()
else:
    sim.load(MAP)

waypoints_dic = {}

waypoints_dic["agent_1"] =[{
        "position": wp.position.to_json(),
        "speed": wp.speed,
        "angle": wp.angle.to_json(),
        "idle": wp.idle,
        "deactivate": wp.deactivate,
        "trigger_distance": wp.trigger_distance,
        "timestamp": wp.timestamp
      } for wp in waypoint_collector(AGENT1_INTERSECTION_POSITION, AGENT1_INTERSECTION_ROTATION, 0.1)]

waypoints_dic["agent_2"] = [{
        "position": wp.position.to_json(),
        "speed": wp.speed,
        "angle": wp.angle.to_json(),
        "idle": wp.idle,
        "deactivate": wp.deactivate,
        "trigger_distance": wp.trigger_distance,
        "timestamp": wp.timestamp
      } for wp in waypoint_collector(AGENT2_INTERSECTION_POSITION, AGENT2_INTERSECTION_ROTATION, 0.3)]

with open('scenario_1_waypoints.json', 'w') as fp:
    json.dump(waypoints_dic, fp, indent=4)