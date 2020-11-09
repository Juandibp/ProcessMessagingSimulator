class message:
    # sender y receiver son procesos
    def __init__(self, psender, preciever, pmessage:str):
        self.sender = psender
        self.reciever = preciever
        self.message = pmessage