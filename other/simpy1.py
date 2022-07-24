from simpy import *
import random
import numpy as np



# Begin when vehicle arrive at the junction
# -   making decision to enter the correct lane
#             o   if lane full queue up behind
# -   wait for turn to pass through the junction
#             o   if green light & previous vehicle move
#             o   vehicle move out of the junction and exit to the direction
#             o   else queue up behind
# -   vehicle exit the junction
right_lane = 0
straight_lane = 0
traffic_lane = [right_lane, straight_lane]
traffic_count = 0
light_state = 'green'

t_red = 100
t_green = 30
t_interarrival_mean = 3

def arrival():
    global right_lane, traffic_count
    while True:
        arrival_time = random.expovariate(1/t_interarrival_mean)
        yield env.timeout(arrival_time)
        print("Vehicle arrived at %.3f s" % env.now)
        right_lane += 1
        traffic_count += 1


def departure():
    global right_lane, light_state
    while True:
        if(light_state == 'green'):
            if (right_lane > 0):
                right_lane -= 1
                print("Vehicle departed at %.3f s" % env.now)
                yield env.timeout(delay=vehicle_delay())
                if(light_state == 'red'):
                    break
        
def traffic_cycle(redLightTime, greenLightTime):
    global light_state, right_lane
    while True:
        print("\nThe light turned red at time %.3f." % env.now)
        light_state = 'red'
        print("Number of cars queueing %d" % right_lane)
        yield env.timeout(redLightTime)
        print("\nThe light turned green at time %.3f." % env.now)
        print("Number of cars queueing %d" % right_lane)
        light_state = 'green'
        env.process(departure())
        yield env.timeout(greenLightTime)

def vehicle_delay():
    return random.triangular(low= 1, high=10, mode = 2)






if __name__ == "__main__":
    env = Environment()    
    # traffic_light(env)
    env.process(arrival())
    env.process(traffic_cycle(redLightTime=t_red, greenLightTime=t_green)) 
    env.run(until=1000.0)
    print("finished simulation")
    print("Traffic count %d" % traffic_count)
    print("Traffic remains in queue %d" % (traffic_count - right_lane))
