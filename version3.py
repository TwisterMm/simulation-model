from simpy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


T_INTERARRIVAL_MEAN = 3
T_GREEN = 24
T_RED = 100
T_YELLOW = 5
T_SIMULATION = 100
SEED = 32
SIZE = 1000
# use data frame, numpy array to replace deque


class vehicle(object):
    def __init__(self, name, time): 
        self.name = name
        self.time = time   


class traffic_intersection(object):
    def __init__(self, env: Environment):
        self.env = env    
        self.green_light = True
        self.right_queue = Store(env)            
        self.straight_queue = Store(env)
        self.interarrival_times = np.array([])        
        self.arrival_times = np.array([]) 
        self.departure_times = np.array([])        
        self.wait_time = np.array([])
        
        
        # # self.env.process(self.arrival()) 
        # self.depart = self.env.process(self.departure())            
        # self.env.process(self.traffic_light()) 

    def traffic_light(self, vehicle):
        yield self.env.timeout(T_RED)
        self.right_queue.put(vehicle)
        # while True:                   
        #     if not self.green_light:
        #         # truns red light after green light
        #         self.depart.interrupt()
        #     else: #green light
        #         yield self.env.timeout(T_GREEN)
        #         self.green_light = False 

    def queue_right(self, vehicle):
        self.env.process(self.traffic_light(vehicle))

    def get(self):
        return self.right_queue.get()

    def view_queue(self):
        return self.right_queue.get_queue()


def arrival(env: Environment, traffic_light: traffic_intersection):
    arrival_count = 0
    while True:        
        interarrival_time = np.random.exponential(T_INTERARRIVAL_MEAN)
        # self.interarrival_times = np.append(self.interarrival_times, interarrival_time)
        yield env.timeout(interarrival_time)
        print("vehicle no %d arrival %.3f" % (arrival_count, env.now))
        traffic_light.queue_right(vehicle(arrival_count, env.now))
        arrival_count += 1
        # self.arrival_times = np.append(self.arrival_times, self.env.now)
            

       
def departure(env: Environment, traffic_light: traffic_intersection):
    while True:
        # try:
        vehicle =  yield traffic_light.get()
        print(vehicle)     
        print("depart time : %.3f" % env.now)     
        # except Interrupt:
        #     #turn red light and wait for green light
        #     print("turn red light")
        #     yield env.timeout(T_RED)                
        #     # self.green_light = True      

def vehicle_delay():
    return np.random.triangular(3, 5, 10)

def convert_second(seconds):
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
    rng = np.random.default_rng(SEED)   
    tr = traffic_intersection(env) 
    env.process(arrival(env, tr))
    env.process(departure(env, tr))
    env.run(until=T_SIMULATION)     
    
     
    print("finished simulation")
    
   
    
    