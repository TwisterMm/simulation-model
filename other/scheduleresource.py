import simpy

def scheduleResources(Resources, env):

    # start the resource process and return a list of hte processes
    process_list = []
    for resource in Resources:
        process_list.append(resource.start())

    return(process_list)

class Resource:
    def __init__(self, env, id, otherResources, timeToProcess):
        self.id = id
        self.resource_process = None
        self.otherResources = otherResources
        self.env = env
        self.timeToProcess = timeToProcess

    def appendOtherResource(self, otherResource):
        self.otherResources.append(otherResource)

    def start(self):
        #yield (self.env.timeout(0))
        self.resource_process = self.env.process(self.run())
        return self.resource_process

    def run(self):
        try:
            yield self.env.timeout(self.timeToProcess)
            self.timeToProcess = 0
            for res in self.otherResources:
                if res.resource_process != None:
                    if res.resource_process.is_alive:
                            res.resource_process.interrupt() 
            print (self.id, "finished")
        except simpy.Interrupt as interrupt:
            print(self.id, "interupted")
            self.timeToProcess = self.timeToProcess - self.env.now

def main():
    env = simpy.Environment()
    res1 = Resource(env, 1, list(), 10)
    res2 = Resource(env, 2, list(), 15)
    res3 = Resource(env, 3, list(), 20)
    #Add other resources to each
    res1.appendOtherResource(res2)
    res1.appendOtherResource(res3)
    res2.appendOtherResource(res1)
    res2.appendOtherResource(res3)
    res3.appendOtherResource(res2)
    res3.appendOtherResource(res1)

    Resources = list()
    Resources.append(res1)
    Resources.append(res2)
    Resources.append(res3)

    resource_processes = scheduleResources(Resources, env)

    # stop when all the resources process ends
    env.run(until=env.all_of(resource_processes))
    #env.run()
    print('end time', env.now)

main()