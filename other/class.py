from simpy import *
import random
import numpy as np
from simpy.events import AnyOf, AllOf, Event

T_INTERARRIVAL_MEAN = 5
T_GREEN = 30
T_RED = 100
T_SIMULATION = 1000


class traffic_intersection(object):
    def __init__(self, env: Environment):
        self.env = env
        self.light_state = 'green'
        self.right_lane = []
        self.straight_lane = []
        self.traffic_count = 0
        self.wait_time = []        
        env.process(self.arrival())        
        env.process(self.traffic_cycle())
        self.deprat = env.process(self.departure(self.right_lane))  
        
    
    
    def arrival(self):
        while True:
            arrival_time = random.expovariate(1/T_INTERARRIVAL_MEAN)
            yield self.env.timeout(arrival_time)            
            lane, lanename = self.set_lane()
            lane.append(self.env.now)
            print("%s : vehicle arrived at %s" % (lanename, secondsConversion(self.env.now)))
            self.traffic_count += 1

    def set_lane(self):
        lane = random.choices(["right lane", "straight lane"], weights=[0.6, 0.4])
        lane = lane[0]
        if(lane == 'right lane'):
            return self.right_lane, lane
        else:
            return self.straight_lane, lane

    def departure(self, lane: list):
        while True:
            if(self.light_state == 'green'):
                if(len(lane) > 0):
                    totalWaitTime = self.env.now - lane[0]
                    self.wait_time.append(totalWaitTime)             
                    lane.pop()
                    print("vehicle departed at %s" % secondsConversion(self.env.now))
                    yield self.env.timeout(delay=vehicle_delay())
                        

    def traffic_cycle(self):
        while True:
            print("\nThe light turned green at time %s" % secondsConversion(self.env.now))
            self.light_state = 'green'
            yield self.env.timeout(T_GREEN)
            print("\nThe light turned red at time %s" % secondsConversion(self.env.now))
            # interrupt depart
            
            print("Number of cars queueing at right lane %d" % len(self.right_lane))
            print("Number of cars queueing at straight lane %d" % len(self.straight_lane))
            self.light_state = 'red'
            yield self.env.timeout(T_RED)

    def summary(self):
        print("Traffic count %d" % self.traffic_count)
        print("Traffic remains in right queue %d" % len(self.right_lane))
        print("Traffic remains in straight queue %d" % len(self.straight_lane))
        wait_time = np.array(self.wait_time)
        print("Average waiting time %s" % secondsConversion(np.mean(wait_time)))

def vehicle_delay():
    return random.triangular(low= 1, high=5, mode = 2)

def secondsConversion(seconds):
    min, sec = divmod(seconds, 60)
    return "%d min %.3f s" % (min, sec)


# def set_lane():
#         right_lane = [1,2,3]
#         straight_lane = [8,8,3]
#         lane = random.choices(["right lane", "straight lane"], weights=[0.6, 0.4])
#         lane = lane[0]
#         if(lane == 'right lane'):
#             return right_lane, lane
#         else:
#             return straight_lane, lane

if __name__ == "__main__":
    env = Environment() 
    tr = traffic_intersection(env)
    env.run(until=T_SIMULATION)
    tr.summary()
    print("finished simulation")
    
    