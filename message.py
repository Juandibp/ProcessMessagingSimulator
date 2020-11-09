class message:
    # sender y receiver son procesos
    def __init__(self, psender, preciever, pmessage:str, ppriority:int = 0):
        self.sender = psender
        self.receiver = preciever
        self.message = pmessage
        self.priority = ppriority