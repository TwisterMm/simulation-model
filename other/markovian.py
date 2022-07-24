import simpy
import random
import statistics


arrivals_time = []
service_time = []
waiting_time = []

mean_service = 1.0
mean_arrival = 2.0
num_servers = 1

class Markovian(object):
    def __init__(self, env, servers):
        self.env = env
        #self.action = env.process(self.run())

    #def server(self,packet ):
        #timeout after random service time
     #   t = random.expovariate(1.0/mean_service)
        #service_time.append(t)
      #  yield self.env.timeout(t)
    
    def getting_service(env, packet, servers):
        # new packet arrives in the system

        begin_wait = env.now
        req = servers.request()
        yield req
        
        begin_service = env.now
        waiting_time.append(begin_service - begin_wait)

        print('%.1f Begin Service of packet %d' % (begin_service, packet))
        
        yield env.timeout(random.expovariate(1.0/mean_service))
        
        service_time.append(env.now - begin_service)

        yield servers.release(req)
        print('%.1f End Service of packet %d' % (env.now, packet))

    
    def run_markovian(env,servers):
        markovian = Markovian(env,servers)
        packet = 0
        #generate new packets
        while True:
            t = random.expovariate(1.0/mean_arrival)
            yield env.timeout(t)
            arrivals_time.append(t)
            packet +=1
            print('%.1f Arrival of packet %d' % (env.now, packet))

            env.process(Markovian.getting_service(env,packet,servers))


    def get_average_service_time(service_time):
        average_service_time = statistics.mean(service_time)
        return average_service_time
    
def main():
    random.seed(42)

    env= simpy.Environment()
    servers  = simpy.Resource(env, num_servers)

    env.process(Markovian.run_markovian(env,servers))
    env.run(until = 50)
    
    print(Markovian.get_average_service_time(service_time))
    print ("Time between consecutive arrivals \n", arrivals_time)
    print("Size: ", len(arrivals_time))
    print ("Service Times \n", service_time)
    print("Size: ", len(service_time))
    print ("Waiting Times \n", service_time)
    print (waiting_time)
    print("Size: ",len(waiting_time))


    
if __name__ == "__main__":
    main()