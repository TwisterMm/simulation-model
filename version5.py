#objectives 
#simulation of traffic junction queue with traffic light using simpy 
from collections import deque
from simpy import *
import numpy as np
import pandas as pd
# model by Tee Wen Shi
# List of dependencies
# cycler==0.11.0
# fonttools==4.31.2
# kiwisolver==1.4.2
# matplotlib==3.5.1
# numpy==1.22.3
# packaging==21.3
# pandas==1.4.1
# Pillow==9.0.1
# pyparsing==3.0.7
# python-dateutil==2.8.2
# pytz==2022.1
# scipy==1.8.0
# seaborn==0.11.2
# simpy==4.0.1
# six==1.16.0


# T_INTERARRIVAL_MEAN = 3
# T_GREEN = 30
# T_RED = 100
# T_YELLOW = 0
# YELLOW_START = T_RED + T_GREEN
# T_SIMULATION = 1000
# T_CYCLE = T_RED + T_GREEN + T_YELLOW
# SEED = 188
DEPARTURE_CONSTANT = 3

class Vehicle(object):
    def __init__(self, name, arrivaltime): 
        self.name = name
        self.arrival_time = arrivaltime          

    def __str__(self):
        return "vehicle: %d arrival time: %s " % (self.name, convert_second(self.arrival_time))


class Traffic_intersection(object):
    def __init__(self, env: Environment, green, red):
        self.env = env       
        self.right_lane = deque()
        self.straight_lane = deque()
        self.departure_times = []
        self.green_time = green
        self.red_time = red 
        self.traffic_cycle_time = green + red           
        self.red_light_event = self.env.process(self.traffic_light()) 
        self.right_queue_count = [[],[]]    
        self.straight_queue_count = [[],[]]   
              
    def departure(self, lane: deque[Vehicle]):
        # queue not empty
        # first car departure
        if(lane):            
            yield self.env.timeout(vehicle_delay())
            #append to the departure times
            self.departure_times.append(self.env.now)
            vehicle = lane.popleft()
            print("vehicle no %s depart at %-20s" % (vehicle.name, convert_second(self.env.now)) ) 
        while True:
            time = self.env.now % self.traffic_cycle_time            
            if(time >= self.red_time and lane):
                vehicle = lane.popleft()
                yield self.env.timeout(DEPARTURE_CONSTANT)
                self.departure_times.append(self.env.now)
                print("vehicle no %s depart at %-20s" % (vehicle.name, convert_second(self.env.now)) )               
            else:
                #adjust back the green light time
                adjust = abs(time - self.traffic_cycle_time)
                yield self.env.timeout(adjust)                
                return             
        
    def traffic_light(self):       
        while True:            
            print("\n\nRed light: %s" % convert_second(self.env.now))
            #red light              
            yield self.env.timeout(self.red_time)
            self.record_queue()
                                      
            #green light  
            print("\n\nGreen light: %s" % convert_second(self.env.now))
            
            # start departure           
            yield self.env.process(self.departure(self.right_lane)) & self.env.process(self.departure(self.straight_lane))
            self.check_queue()
            
    def set_lane(self):
        right_lane = np.random.choice([True, False], p=[0.6, 0.4])
        if(right_lane):
            return self.right_lane, "right"
        else:
            return self.straight_lane, "straight"

    def check_queue(self):
        print("%d vehicles still in right lane" % len(self.right_lane))
        print("%d vehicles still in straight lane" % len(self.straight_lane))

    def record_queue(self):
        self.right_queue_count[0].append(len(self.right_lane))
        self.right_queue_count[1].append(self.env.now)
        self.straight_queue_count[0].append(len(self.straight_lane))
        self.straight_queue_count[1].append(self.env.now)

    def queue_data_frame(self):
        squeue_df = pd.DataFrame({
            "No of vehicles in queue": self.straight_queue_count[0],
                "Time recorded /s": self.straight_queue_count[1],
        })

        rqueue_df = pd.DataFrame({
            "No of vehicles in queue": self.right_queue_count[0],
                "Time recorded /s": self.right_queue_count[1],
        })
        return squeue_df, rqueue_df

def arrival(env: Environment, traffic_light: Traffic_intersection, array, lane, mean):
    arrival_count = 0 
      
    while True:       
        interarrival_time = np.random.exponential(mean)
        arrival_count += 1
        array.append(interarrival_time)
        lane_queue, name_of_lane = traffic_light.set_lane() 
        lane.append(name_of_lane)       
        yield env.timeout(interarrival_time)
        print("vehicle no %d arrival %-20s" % (arrival_count, convert_second(env.now)))        
        lane_queue.append(Vehicle(arrival_count, env.now))        
        

        
def vehicle_delay():
    
    return np.random.triangular(3, 5, 10)

def convert_second(seconds):
    if(seconds <= 60):
        return "%5.3f s" % seconds
    elif(seconds >= 3600):
        min, sec = divmod(seconds, 60)
        hr, min = divmod(min, 60)
        return "%d h %d min %5.3f s" % (hr, min, sec)
    else:
        min, sec = divmod(seconds, 60)
        return "%d min %5.3f s" % (min, sec)

def main(seed_value, mean=3, green_light_time= 30, red_light_time= 100, run_length=1000):        
    env = Environment()      
    tr = Traffic_intersection(env, green_light_time, red_light_time)    
    np.random.seed(seed_value)  
    interarrival_times = []
    lane = []
    env.process(arrival(env, tr, interarrival_times, lane, mean))   
    env.run(until=run_length)  
    tr.check_queue()

      
    
    #data processing
    
    arrival_times = np.cumsum(interarrival_times)
    departure_times = np.array(tr.departure_times)
    new_dep = np.resize(departure_times, arrival_times.shape[0]) 
    new_dep[departure_times.size:] = np.nan
    wait_times = np.subtract(new_dep,arrival_times)
    lane = np.array(lane)

    #pandas data frame
    vehicles_df = pd.DataFrame({
            "interarrival_time": interarrival_times,
            "arrive_time": arrival_times,
            "departure_time": new_dep,            
            "wait_time": wait_times,  
            "lane_entered": lane          
        })

    print(vehicles_df)
    
    straight_queue, right_queue =tr.queue_data_frame()
    

    print("finished simulation")
    return vehicles_df, straight_queue, right_queue

if __name__ == "__main__":
    # seed is use to replicate the same conditions in generator
    sim1, straight1, right1 = main(188, 3, 40, 100, 1000)
    print(straight1)
    print(right1)
    # sim2 = main(188, 3, 30, 100, 1000)
    # sim3 = main(188, 3, 40, 60, 1000)