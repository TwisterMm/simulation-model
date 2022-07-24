
import simpy
import numpy as np
import random 
from simpy import start_delayed

TRAFFIC_RED_TIME = 120
TRAFFIC_YELLOW_TIME = 3
TRAFFIC_GREEN_TIME = 25

class TrafficLight(object):

    def __init__(self, env):
        self.traffic_light_state = ''
        self.rightQueue = 0
        self.straigtQueue = 0
        self.trafficlight = simpy.Resource(env)
    
    def vehicle_arrival(self, env):
        print(f'Car {name} arriving at {env.now}')
        # interarrival = random.expovariate(env)  # generate interarrival 
        # time += interarrival
        # yield time  # produce the next arrival time
        t = random.expovariate(1.0 / 5)
        yield env.timeout(t)
        print(t)
        

    def generate_interarrival():
        random.exponential()

    def set_lane():
        """
        set vehicles into different queue
        """
        random_num = random.expovariate()
        if()      

    def traffic_light(self, env):
        while True:
            # print("Light turned green at t= %.2f min" % (env.now/60))
            # traffic_light_state = 'G'
            # yield env.timeout(TRAFFIC_GREEN_TIME)
            # print("Light turned yellow at t= %.2f min" % (env.now/60))
            # traffic_light_state = 'Y'
            # yield env.timeout(TRAFFIC_YELLOW_TIME)
            # print("Light turned red at t= %.2f min" % (env.now/60))
            # traffic_light_state = 'R'
            # yield env.timeout(TRAFFIC_RED_TIME)
            # Section 4.2.1: Change the light to green.

            traffic_light_state = 'G'
            print("\nThe light turned green at time %.3f." % env.now)

            # If there are cars in the queue, schedule a departure event:
            if len(self.rightQueue):

                # Generate departure delay as a random draw from triangular
                # distribution:
                delay= random.triangular(left=t_depart_left, mode=t_depart_mode,
                right=t_depart_right)

                start_delayed(env, departure(), delay=delay)

            # Schedule event that will turn the light red:
            yield env.timeout(t_green)


            # Section 4.2.2: Change the light to red.
            light= 'red'
            print("\nThe light turned red at time %.3f."   % env.now)

            # Schedule event that will turn the light green:
            yield env.timeout(t_red)

    def departure(env):
        pass
        

 
def main():        
    env = simpy.Environment()
    sim = TrafficLight()
    env.process(sim.arrival(env))
    env.process(sim.traffic_light(env))
    env.run(until=3600)
    print("Simulation complete")

if __name__ == '__main__':
    main()