class Gracz:

    def __init__(self, Id, pieniadze):
        self.Id = Id
        self.pieniadze = pieniadze
        self.uwiezienie = False
        self.liczbaPostojow = 0
    
    def odczekajJednaTure(self):
        if self.liczbaPostojow != 0:
            self.liczbaPostojow -= 1