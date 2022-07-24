import simpy
#from simpy.util import start_delayed
# import numpy.random
from collections import deque, namedtuple
from numpy import random



#model components
NUM_INT = 3
ARRIVAL_TIME_MEAN = 1.1
TRIP_LENGTH = 4
GREEN_TIME = 3.0
RED_TIME = 3.0




class Simulation(object):
    def __init__(self,env):
        self.env = env
        self.intersections = [Intersection(env,i) for i in range(NUM_INT)]
        for (i,intersection) in enumerate(self.intersections):
            intersection.set_next_intersection(self.intersections[(i+1)%NUM_INT])
        self.env.process(self.light())
        self.env.process(self.arrivals())

    def arrivals(self):
        while True:
            yield self.env.timeout(random.exponential(ARRIVAL_TIME_MEAN))
            intersection = random.choice(self.intersections)
            intersection.receive(TRIP_LENGTH)

    def light(self):
        while True:
            for intersection in self.intersections:
                intersection.start_departing()
            yield self.env.timeout(GREEN_TIME)
            for intersection in self.intersections:
                intersection.turn_red()
            yield env.timeout(RED_TIME)


class Intersection(object):
    def __init__(self,env,index):
        self.index = index
        self.queue = deque()
        self.env = env
        self.start_departing()

    def set_next_intersection(self,intersection):
        self.next_intersection = intersection

    def start_departing(self):
        self.is_departing = True
        self.action = env.process(self.departure())

    def turn_red(self):
        if self.is_departing:
            self.is_departing = False
            self.action.interrupt('red light')

    def receive(self,car):
        self.queue.append(car)
        if not self.is_departing:
            self.start_departing()

    def departure(self):
        while True:
            try:
                if len(self.queue)==0:
                    self.is_departing = False
                    self.env.exit('no more cars in %d'%self.index)
                else:
                    yield self.env.timeout(1.0)
                    if len(self.queue)>0:
                        if len(self.queue)==1:
                            car=self.queue[0]
                            self.queue.clear()
                        else:
                            car = self.queue.popleft()
                        car = car - 1
                        if car > 0:
                            self.next_intersection.receive(car)
            except simpy.Interrupt as i:
                print('interrupted by',i.cause)




#model/ experiment
env = simpy.Environment()
sim = Simulation(env)
env.run(until=10)
