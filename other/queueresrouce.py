from simpy import *



def arrival(queue:Resource):
    queue.put_queue()

def depart(queue:Resource):
    with queue.request() as req:
        yield env.timeout(3)
        yield req
    

env = Environment()
queue = Resource(env, capacity=1)
env.process(arrival(queue))
env.process(depart(queue))
env.run(until=20)