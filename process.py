from message import message
from config import *

class Process:
    def __init__(self, pname, pmessages=[]):
        self.name = pname
        self.waitingFrom = ""
        self.active = True
        self.messages = []
    
    def showInConsole(self, isRecBlocking:bool, isDirectAdressing:bool, hasPriority:bool):
        print("-----------------------")
        print("Nombre de proceso: " + self.name)
        print("Estado: " + ("Activo." if self.active else "Bloqueado."))
        if self.waitingFrom != "":
            print("Esperando mensaje de: " + self.waitingFrom)
        if isDirectAdressing:
            print("Cola de mensajes: {" )
            for m in self.messages:
                m.showInConsole(hasPriority)
            print("}")

class ProcessController:
    def __init__(self, conf:config):
        self.configuration = conf
        self.processes = {}
        self.mailbox = [] # lista de objetos clases mensajes

    def addProcess(self, p:Process):
        if self.processes.get(p.name):
            raise RuntimeError("Ya hay un proceso con ese ID")
        if len(self.processes) >= self.configuration.lenProcesos:
            raise RuntimeError("No se pueden meter mas procesos. Ya hay el maximo de: "+str(self.configuration.lenProcesos))
        self.processes[p.name] = p

    def send(self, sender:str, receiver:str, msg:str, priority:int):
        #send, receive blocking, addressing directo
        if not self.processes[sender]:
            raise RuntimeError("No existe el proceso " + sender)
        if not self.processes[receiver]:
            raise RuntimeError("No existe el proceso " + receiver)
        receiverProc = self.processes[receiver]
        senderProc = self.processes[sender]
        m = message(senderProc, receiverProc, msg, priority)
        sendTo = receiverProc.messages if self.configuration.dir[0] == "direct" else self.mailbox
        if  len(sendTo) >= self.configuration.lenMensajes:
            print("Se ha exedido el límite de mensajes en cola.")
            return 
        if receiverProc.waitingFrom == sender:
            #es un receive blocking
            # print(self.configuration.queues)
            if self.configuration.recieve == "blocking":
                receiverProc.active = True
                receiverProc.waitingFrom = ""
                print("El proceso " + receiverProc.name + " recibio el mensaje: " + m.message + ". De parte de " + m.sender.name)
            else:
                sendTo.append(m)
                if self.configuration.queues == "priority":
                    sendTo.sort(key = lambda msg: msg.priority)
                    sendTo.reverse()

                print("El proceso " + senderProc.name + " ha enviado el mensaje. Pero no ha sido recibido.")
        else:
            sendTo.append(m)
            # print(self.configuration.queues)
            if self.configuration.queues == "priority":
                sendTo.sort(key = lambda msg: msg.priority)
                sendTo.reverse()
            senderProc.active = False
            print("El proceso " + senderProc.name + " ha enviado el mensaje. Pero no ha sido recibido.")

    def receive(self, sender:str, receiver:str):
        if not self.processes.get(sender):
            raise RuntimeError("No existe el proceso " + sender)
        if not self.processes.get(receiver):
            raise RuntimeError("No existe el proceso " + receiver)
        receiverProc = self.processes[receiver]
        senderProc = self.processes[sender]
        searchIn = receiverProc.messages if self.configuration.dir[0] == "direct" else self.mailbox
        for m in searchIn:
            if m.receiver.name == receiver and m.sender.name == sender:
                # addressing directo implicito/explicito
                senderSignature = "[Explicito] De parte de " + m.sender.name if self.configuration.dir[-1] == "explicit" else "[Implicito] Tiene la firma de " + m.sender.name
                foundIn = "" if self.configuration.dir[0] == "direct" else " del buzon"
                print("El proceso " + receiverProc.name + " recibio el mensaje"+foundIn+": " + m.message + ". " + senderSignature)
                searchIn.remove(m)
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


if __name__ == "__main__":
    c = ProcessController(config("blocking", "blocking", ["indirect"], ["lenght", "dynamic"], "priority"))
    c.addProcess(Process( "p1"))
    c.addProcess(Process("p2"))
    c.addProcess(Process("p3"))
    c.send("p1", "p2", "Hola mundo 1", 10)
    c.send("p1", "p2", "Hola mundo 2", 5)
    c.send("p1", "p3", "Hola mundo 3", 7)
    
    print(list(map(lambda elem: (elem.message, elem.priority), c.processes["p2"].messages)))
    print("Le buson: ", list(map(lambda elem: (elem.message, elem.priority), c.mailbox)))
    print("Config addressing", c.configuration.dir)

    c.receive("p1","p2")
    c.receive("p1","p3")

    print(list(map(lambda elem: (elem.message, elem.priority), c.processes["p2"].messages)))
    print("Le buson: ", list(map(lambda elem: (elem.message, elem.priority), c.mailbox)))