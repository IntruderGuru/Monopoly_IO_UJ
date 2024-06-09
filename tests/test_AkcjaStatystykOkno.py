from src.okno.AkcjaStatystykOkno import AkcjaStatystykOkno, MAKSYMALNA_DLUGOSC_NAZWY_GRACZA


class TestAkcjaStatystykOkno:
    def setup_method(self):
        pass

    def test_sprawdz_czy_nazwa_gracza_nie_za_dluga_jest_za_dluga(self):
        AkcjaStatystykOkno.sprawdz_czy_nazwa_gracza_nie_za_dluga(self, nazwa='{message: <{width}}'.format(
            message=' ',
            width=MAKSYMALNA_DLUGOSC_NAZWY_GRACZA + 1,
        ))