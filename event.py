from collections import deque
import simpy
import numpy as np


class traffic_light:
    def __init__(self, env: simpy.Environment, intertimes, queue):
        self.env = env
        
        self.intertimes = intertimes
        self.queue = queue
        self.red_light = env.process(self.red_light())
        # self.stop_departure = env.event()
    
    def departure(self):
        while True:
            time = self.env.now % 130            
            if(time >= 100):
                exit_time = queue.popleft()
                print("vehicle depart at %d" % self.env.now)
                yield self.env.timeout(exit_time)
            else:
                return
            

    def red_light(self):
        while True:
            print("Red light %d" % self.env.now)            
            yield self.env.timeout(100)
            print("Green light %d" %self.env.now)
            green_light = env.process(self.departure())
            yield green_light
            # self.stop_departure = env.event()

if __name__ == "__main__":
    rng = np.random.default_rng(23)
    interarrival_times = rng.exponential(scale= 3.0, size= 400)    
    
    env = simpy.Environment()
    queue = deque()
    for time in np.nditer(interarrival_times, order='C'):
        queue.append(time)
    tr = traffic_light(env, interarrival_times, queue)
    env.run(until=1000)
    print(interarrival_times)