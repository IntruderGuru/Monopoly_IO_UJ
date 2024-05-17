class Gracz:
    def __init__(self, id, kwota, pionek):
        self.id = id
        self.kwota = kwota
        self.pionek = pionek
        self.pozycja = 0
        self.uwiezienie = False
        self.tury_w_wiezieniu = 0  # Licznik tur w więzieniu

    def odczekajJednaTure(self):
        if self.uwiezienie:
            self.tury_w_wiezieniu += 1
            if self.tury_w_wiezieniu >= 2:
                self.uwiezienie = False
                self.tury_w_wiezieniu = 0
                print(f"Gracz {self.id} opuszcza więzienie po dwóch turach")
