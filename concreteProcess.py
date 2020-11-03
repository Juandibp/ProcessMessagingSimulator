from processMethodInterface import *

class unblocking(processInterface):
    def send(self):
        return "{Result of the concreteProcess}"    #super().operation()

class blovkingrocess(processInterface):
    def send(self):
        return "{Result of the concreteProcess}" 
