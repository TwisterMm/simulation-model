
from simpy import *
import random

class Person(object):
    def __init__(self, env: Environment):
        self.env = env        
        self.toilet_break = False
        self.break_count = 0
        self.break_min = 0
        
        self.working = self.env.process(self.working())
        self.env.process(self.go_to_toilet())

    def working(self):
        while True:
            try:
                yield self.env.timeout(1000)
                print("work")
            except Interrupt:
                self.toilet_break = True
                urinate = random.choice([True, False])
                if(urinate):
                    yield self.env.timeout(3)
                    self.break_min +=3
                    print("Back from urinate %d min" % self.env.now)
                else:
                    yield self.env.timeout(5)
                    self.break_min +=5
                    print("Back from defeacate %d min" % self.env.now)
                self.toilet_break = False

    def go_to_toilet(self):
        while True:            
            yield self.env.timeout(random.expovariate(1/20))
            if not self.toilet_break:
                self.working.interrupt("toilet break at %d" % self.env.now)
                self.break_count += 1

   
if __name__ == "__main__":
    
    env = Environment()
    event = Event(env)

    

    
    amy = Person(env) 
      
    env.run(until=1000)
    print("total toilet breaks: %d" % amy.break_count)
    print("total breaks minutes: %d" % amy.break_min)

   