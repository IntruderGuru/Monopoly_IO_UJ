class Pole:
    def __init__(self, numer: int, typ: str):
        self.numer = numer
        self.typ = typ
    
    def wyswietl_info(self) :
        return (f"Nazwa: {self.typ}")
