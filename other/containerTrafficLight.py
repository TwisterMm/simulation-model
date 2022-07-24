from collections import deque
from simpy import *
import numpy.random as random
# import numpy as np
# from simpy.events import AnyOf, AllOf, Event

T_INTERARRIVAL_MEAN = 3
T_GREEN = 24
T_RED = 100
T_YELLOW = 5
T_SIMULATION = 10000

class Struct(object):
   """
   This simple class allows one to create an object whose attributes are
   initialized via keyword argument/value pairs.  One can update the attributes
   as needed later.
   """
   def __init__(self, **kwargs):
      self.__dict__.update(kwargs)

class traffic_intersection(object):
    def __init__(self, env: Environment):
        self.env = env        
        
        self.arrival_count = 0
        self.departure_count = 0        
        self.light = 'green'
        self.lightActivity = self.env.event()
        self.isMovingR = False
        self.isMovingS = False
        self.greenLightTime = Container(env, T_GREEN, init= 0)
        self.Q_stats= Struct(count=0, cars_waiting_at_RL=0, cars_waiting_at_SL=0)
        self.W_stats= Struct(count=0, waiting_time=0.0) 
        self.departing = env.event()   
        self.env.process(self.arrival())        
        self.env.process(self.traffic_cycle()) 
            
        # self.right_lane_depart = self.env.process(self.departure(self.right_lane, self.isMovingR))
        # self.straight_lane_depart = self.env.process(self.departure(self.straight_lane, self.isMovingS))
        # self.env.process(self.monitor()) 
    
        


    def initialise(self):
        init_arrival = int(random.expovariate(2))
        self.arrival_count += init_arrival
        for i in range(init_arrival):
            lane, lanename = self.set_lane()             
            lane.append((self.arrival_count, self.env.now))
            print("%s : vehicle %d arrived at %s" % (lanename, i, secondsConversion(self.env.now)))
        
    def arrival(self):
       
        while True:
            arrival_time = random.expovariate(1/T_INTERARRIVAL_MEAN)
            yield self.env.timeout(arrival_time)   #next arrival time

    def vehicle(self):     
            yield self.greenLightTime.get(vehicle_delay())


    def set_lane(self):
        lane = random.choices(["right lane", "straight lane"], weights=[0.6, 0.4])
        lane = lane[0]
        if(lane == 'right lane'):
            return self.right_lane, lane
        else:
            return self.straight_lane, lane

    def get_lanename(self, lane: deque):
        if(lane == self.right_lane):
            return 'right lane'
        else:
            return 'straight lane'

    def departure(self, lane: deque, isMoving: bool):
        while True:
            pass
                    
                      
                          

    def traffic_cycle(self):        
        while True:                     
            self.light = 'green'
            print("\nThe light turned green at time %s" % secondsConversion(self.env.now))
             
            self.env.process(self.departure(self.right_lane, self.isMovingR))               
            self.env.process(self.departure(self.straight_lane, self.isMovingS))            
            self.lightActivity = self.env.timeout(T_GREEN)  
            yield self.lightActivity          
            # self.light = 'yellow'    
            # print("\nThe light turned yellow at time %s" % secondsConversion(self.env.now))                  
            # self.lightActivity = self.env.timeout(T_YELLOW)            
            self.light = 'red'
            self.isMovingR = False 
            self.isMovingS = False
            print("\nThe light turned red at time %s" % secondsConversion(self.env.now)) 
            self.lightActivity = self.env.timeout(T_RED)              
            yield self.lightActivity            
    
    def monitor(self):
        while True:
            self.Q_stats.count += 1
            self.Q_stats.cars_waiting_at_RL += len(self.right_lane)
            self.Q_stats.cars_waiting_at_SL += len(self.straight_lane)
            yield env.timeout(1.0)

    def summary(self):
        print("Total Arrival: %d" %self.arrival_count)
        print("Total Departure: %d" %self.departure_count)        
  
def vehicle_delay(self):
    if(self.isMoving):
        return 2.0
    else:
        return random.triangular(low = 3, high = 10, mode = 5)

def secondsConversion(seconds):
    if(seconds >= 60):
        min, sec = divmod(seconds, 60)
        return "%d min %.3f s" % (min, sec)
    elif(seconds >= 3600):
        min, sec = divmod(seconds, 60)
        hr, min = divmod(min, 60)
        return "%d h %d min %.3f s" % (hr, min, sec)
    else:
        return "%.3f s" % seconds


if __name__ == "__main__":
    env = Environment() 
    tr = traffic_intersection(env)
    
    env.run(until=T_SIMULATION)    
    print("finished simulation")
    
    
    
    