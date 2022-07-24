from collections import deque
import simpy
import itertools


class queue:     
    def __init__(self, env):
        self.queue = deque()      
        self.trafficGreenTime= simpy.Container(env, init = 0, capacity=30)
        self.mon_proc = env.process(self.monitor_tank(env))

    def initialise(self):
        for i in range(10):
            self.queue.append((1, i))
    
    def car_generator(env, gas_station, fuel_pump):        
        for i in itertools.count():
            yield env.timeout(random.randint(*T_INTER))
            env.process(car('Car %d' % i, env, gas_station, fuel_pump))

    def departure(self):
        yield self.trafficGreenTime.get(1)