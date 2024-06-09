from src.Odpowiedz import Odpowiedz


class TestOdpowiedz:
    def test_ilosc_mozliwych_odpowiedzi(self):
        lista_mozliwych_odpowiedzi = ["Odpowiedz_A", "Odpowiedz_B", "Odpowiedz_C"]
        for enum in Odpowiedz:
            assert str(enum).replace("Odpowiedz.", "") in lista_mozliwych_odpowiedzi
