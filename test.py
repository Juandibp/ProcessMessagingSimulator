import random

import simpy

RANDOM_SEED = 69
SIM_TIME = 100

class BroadcastPipe(object):
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def put(self, value):
        if not self.pipes:
            raise RuntimeError("There are no pipes")
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)

    def get_output_connection(self):
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe

def sendDirectMessage(sender, receiver):
    global env
    pipe = simpy.Store(env)
    env.process(sender(sender, env, pipe))
    env.process(receiver(receiver, env, pipe))



def sender(process, env, out_pipe): # en este caso el sender es nonblocking 
    while True:
        # Esperar a transmision
        yield env.timeout(random.randint(6,10))

        msg = (env.now, '%s holis en %d' % (process.id, env.now))
        out_pipe.put(msg)

def receiver(process, env, in_pipe): # en este caso el receiver es blocking 
    while True:
        msg = yield in_pipe.get() #block until message is received

        if msg[0] < env.now:
            print("Recibio el mensaje tarde: en tiempo %d: %s received message: %s." % (env.now, process.id, msg[1]))
            
        else:
            print("en tiempo %d: %s received message: %s." % (env.now, process.id, msg[1]))

        yield env.timeout(random.randint(4,8))


#empezamos la sim
print("Comunicacion de procesos")
random.seed(RANDOM_SEED)
env = simpy.Environment()

#para uno a uno o muchos a uno usar store           MENSAJERIA DIRECTA
pipe = simpy.Store(env)
env.process(sender('Sender A', env, pipe))
env.process(receiver('Receiver A', env, pipe))

print('\mComunicacion Uno a Uno\n')
env.run(until=SIM_TIME)


#Para uno a muchos usar el BroadcastPipe                 MENSAJERIA INDIRECTA
#TAmbien sirve para uno a uno, muchos a muchos o muchos a uno
env = simpy.Environment()
bcPipe = BroadcastPipe(env)
env.process(sender('Sender A2', env, bcPipe))
env.process(receiver('Receiver A2', env, bcPipe.get_output_connection()))
env.process(receiver('Receiver B2', env, bcPipe.get_output_connection()))

print('\nComunicacion Uno a muchos\n')
env.run(until=SIM_TIME)