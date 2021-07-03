class message:
    # sender y receiver son procesos
    def __init__(self, psender, preciever, pmessage:str, ppriority:int = 0):
        self.sender = psender
        self.receiver = preciever
        self.message = pmessage
        self.priority = ppriority
    
    def showInConsole(self, showPriority=False, output=print):
        output("- - - - - - - - - - - - - - - ")
        output("Mensaje de: " + self.sender.name)
        output("Para: " + self.receiver.name)
        output("Contenido del mensaje: " + self.message)
        if self.priority != 0:
            output("Prioridad: " + str(self.priority))