from src.Pole import Pole
from src.Gracz import Gracz
from src.Gra import Gra




class PodatekDochodowy(Pole):

    def __init__(self, numer: int, podatek: int):
        super().__init__(numer, "Podatek Dochodowy")
        self.podatek = podatek

    def wyswietl_info(self):
        return (f"Stanąłeś na polu podatek dochodowy. Musisz zapłacić podatek w wysokości {self.podatek}")
