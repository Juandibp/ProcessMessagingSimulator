from message import message
from config import *

class Process:
    def __init__(self, pname, pmessages=[]):
        self.name = pname
        self.waitingFrom = ""
        self.active = True
        self.messages = []

class ProcessController:
    def __init__(self, conf:config):
        self.configuration = conf
        self.processes = {}

    def addProcess(self, p:Process):
        if self.processes.get(p.name):
            raise RuntimeError("Ya hay un proceso con ese ID")
        self.processes[p.name] = p

    def send(self, sender:str, receiver:str, msg):
        #send, receive blocking, addressing directo
        if not self.processes[sender]:
            raise RuntimeError("No existe el proceso " + sender)
        if not self.processes[receiver]:
            raise RuntimeError("No existe el proceso " + receiver)
        receiverProc = self.processes[receiver]
        senderProc = self.processes[sender]
        m = message(senderProc, receiverProc, msg)
        if receiverProc.waitingFrom == sender:
            #es un receive blocking
            receiverProc.active = True
            receiverProc.waitingFrom = ""
            print("El proceso " + receiverProc.name + " recibio el mensaje: " + m.message + ". De parte de " + m.sender.name)
        else:
            receiverProc.messages.append(m)
            senderProc.active = False
            print("El proceso " + senderProc.name + " ha enviado el mensaje. Pero no ha sido recibido.")


    def receive(self, sender:str, receiver:str):
        if not self.processes[sender]:
            raise RuntimeError("No existe el proceso " + sender)
        if not self.processes[receiver]:
            raise RuntimeError("No existe el proceso " + receiver)
        receiverProc = self.processes[receiver]
        senderProc = self.processes[sender]
        for m in receiverProc.messages:
            if m.sender.name == sender:
                # addressing directo implicito/explicito
                senderSignature = "[Explicito] De parte de " + m.sender.name if self.configuration.dir[-1] == "explicit" else "[Implicito] Tiene la firma de " + m.sender.name
                print("El proceso " + receiverProc.name + " recibio el mensaje: " + m.message + ". " + senderSignature)
                senderProc.active = True
                receiverProc.waitingFrom = ""
                receiverProc.active = True                
                return
        # no hay mensaje enviado por el sender
        if self.configuration.recieve == "blocking":
            receiverProc.active = False 
            receiverProc.waitingFrom = sender

        elif self.configuration.recieve == "arrival-test":
            print("No, no hay un mensaje de esa direccion. Puedes probar de nuevo.")
