class message:
    # sender y receiver son procesos
    def __init__(self, psender, preciever, pmessage:str, ppriority:int = 0):
        self.sender = psender
        self.receiver = preciever
        self.message = pmessage
        self.priority = ppriority
    
    def showInConsole(self, showPriority=False):
        print("- - - - - - - - - - - - - - - ")
        print("Mensaje de: " + self.sender.name)
        print("Para: " + self.receiver.name)
        print("Contenido del mensaje: " + self.message)
        if self.priority != 0:
            print("Prioridad: " + str(self.priority))