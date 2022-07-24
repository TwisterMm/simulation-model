
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

right_lane = []
straight_lane = []
traffic_lane = [right_lane, straight_lane]
traffic_count = 0
light_state = 'green'
wait_time = []

t_red = 100
t_green = 30
t_interarrival_mean = 10

def arrival():
    global right_lane, straight_lane, traffic_count
    while True:
        arrival_time = random.expovariate(1/t_interarrival_mean)
        yield env.timeout(arrival_time)
        print("Vehicle arrived at %.3f min" % (env.now /60))
        traffic_count += 1

def set_lane():
    global traffic_lane
    return random.choices(traffic_lane, weights=[0.6, 0.4])

def departure():
    global right_lane, light_state, wait_time, straight_lane
    while True:
        if(light_state == 'green'):
            if (len(right_lane) > 0):
                #right lane
                totalWaitTime = env.now - right_lane[0]
                wait_time.append(totalWaitTime)                
                right_lane.pop(0)

                #left lane
                totalWaitTime = env.now - straight_lane[0]
                wait_time.append(totalWaitTime)                
                straight_lane.pop(0)
                print("Vehicle departed at %.3f min" % (env.now /60))
                delay_time = vehicle_delay()
                yield env.timeout(delay = delay_time)
            
        
def traffic_cycle(redLightTime, greenLightTime):
    global light_state, right_lane, straight_lane
    while True:
        print("\nThe light turned red at time %.3f min" % (env.now /60))
        light_state = 'red'
        print("Number of cars queueing at right lane %d" % len(right_lane))
        print("Number of cars queueing at straight lane %d" % len(straight_lane))
        yield env.timeout(redLightTime)
        print("\nThe light turned green at time %.3f min" % (env.now /60))
        print("Number of cars queueing at right lane %d" % len(right_lane))
        print("Number of cars queueing at straight lane %d" % len(straight_lane))
        light_state = 'green'
        env.process(departure())
        yield env.timeout(greenLightTime)

def vehicle_delay():
    return random.triangular(low= 1, high=5, mode = 2)

if __name__ == "__main__":
    env = Environment()    
    # traffic_light(env)
    env.process(arrival())
    env.process(traffic_cycle(redLightTime=t_red, greenLightTime=t_green)) 
    env.run(until=1000)
    print("finished simulation")
    print("Traffic count %d" % traffic_count)
    print("Traffic remains in queue %d" % len(right_lane))
    


    wait_time = np.array(wait_time)
    print("Average waiting time %.2f" % np.mean(wait_time))
    
