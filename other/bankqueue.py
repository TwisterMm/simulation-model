import random
from simpy import *
import pandas as pd
import matplotlib.pyplot as plt

number = 300  # Max number of jobs if infinite is false
noJobCap = True  # For infinite
maxTime = 100000.0  # Runtime limit
timeInBank = 20.0  # Mean time in bank
arrivalMean = 2.0  # Mean of arrival process
seed = 204204  # Seed for RNG
parallelism = 10  # Number of queues
d = 2  # Number of queues to parse
doPrint = False  # True => print every arrival and wait time

if noJobCap == True:
    number = 0

Queues = []


def job(env, name, counters):
    arrive = env.now
    Qlength = {i: NoInSystem(counters[i]) for i in QueueSelector(d, counters)}
    if doPrint:
        print("%7.4f %s: Arrival " % (arrive, name))
    Queues.append({i: len(counters[i].put_queue) for i in range(len(counters))})
    choice = [k for k, v in sorted(Qlength.items(), key=lambda a: a[1])][0]
    with counters[choice].request() as req:
        # Wait in queue
        yield req
        wait = env.now - arrive
        # We got to the server
        if doPrint:
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tib = random.expovariate(1.0 / timeInBank)
        yield env.timeout(tib)
        Queues.append({i: len(counters[i].put_queue) for i in range(len(counters))})
        if doPrint:
            print('%7.4f %s: Finished' % (env.now, name))


def NoInSystem(R):
    """Total number of jobs in the resource R"""
    return len(R.put_queue) + len(R.users)


def QueueSelector(d, counters):
    return random.sample(range(len(counters)), d)


def Source(env, number, interval, counters):
    if noJobCap == False:
        for i in range(number):
            c = job(env, 'job%02d' % i, counters)
            env.process(c)
            t = random.expovariate(1.0 / interval)
            yield env.timeout(t)
    else:
        while True:  # Needed for infinite case as True refers to "until".
            i = number
            number += 1
            c = job(env, 'job%02d' % i, counters)
            env.process(c)
            t = random.expovariate(1.0 / interval)
            yield env.timeout(t)
