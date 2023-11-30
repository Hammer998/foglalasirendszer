from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Szoba absztrakt osztály
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalasok = []

    def lemondas(self, datum):
        foglalas = next((f for f in self.foglalasok if f.datum == datum), None)
        if foglalas:
            self.foglalasok.remove(foglalas)
            return foglalas
        return None


    @abstractmethod
    def __str__(self):
        pass


# EgyagyasSzoba osztály
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar, klima=True):
        super().__init__(szobaszam, ar)
        self.klima = klima

    def __str__(self):
        return f"Egyágyas szoba {self.szobaszam}, Ár: {self.ar}, Klíma: {self.klima}"

# KetagyasSzoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar, erkely=False):
        super().__init__(szobaszam, ar)
        self.erkely = erkely

    def __str__(self):
        return f"Kétágyas szoba {self.szobaszam}, Ár: {self.ar}, Erkély: {self.erkely}"

# Szalloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def list_szobak(self):
        print(f"\n{self.nev} szálloda szobái:")
        for szoba in self.szobak:
            print(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
                if foglalas_datum < datetime.now():
                    print("Érvénytelen dátum, próbáld újra.")
                    return None

                for foglalas_szoba in szoba.foglalasok:
                    if foglalas_szoba.datum == datum:
                        print("A szoba már foglalt ezen a dátumon, próbáld újra.")
                        return None

                foglalas = Foglalas(szoba, datum)
                szoba.foglalasok.append(foglalas)
                return szoba.ar
        return None

    def foglalas_lemondas(self, foglalas):
        if foglalas.szoba.szobaszam != "DUMMY" and foglalas in foglalas.szoba.foglalasok:
            foglalas.szoba.foglalasok.remove(foglalas)
            print(f"Foglalás lemondva a(z) {foglalas.datum} dátumra a szobáról: {foglalas.szoba.szobaszam}")
        else:
            print("Érvénytelen foglalás, próbáld újra.")

    def list_foglalasok(self):
        print("\nÖsszes foglalás:")
        for szoba in self.szobak:
            for foglalas in szoba.foglalasok:
                print(f"Foglalás a(z) {foglalas.datum} dátumra a következő szobára:\n{szoba}")

# Foglalas osztály
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def __str__(self):
        return f"Foglalás a(z) {self.datum} dátumra a következő szobára: {self.szoba}"

# FelhasznaloiInterfesz osztály
class FelhasznaloiInterfesz:
    def __init__(self, szalloda):
        self.szalloda = szalloda

    def futtat(self):
        self.pelda_adatok_feltoltese()

        while True:
            print("\nVálassz műveletet:")
            print("1. Szobák listázása")
            print("2. Foglalás készítése")
            print("3. Foglalás lemondása")
            print("4. Foglalások listázása")
            print("5. Kilépés")

            valasztas = input("Választás: ")

            if valasztas == "1":
                self.szalloda.list_szobak()
            elif valasztas == "2":
                self.foglalas_keszitese()
            elif valasztas == "3":
                self.foglalas_lemondasa()
            elif valasztas == "4":
                self.szalloda.list_foglalasok()
            elif valasztas == "5":
                print("Kilépés...")
                break
            else:
                print("Érvénytelen választás, próbáld újra.")

    def foglalas_keszitese(self):
        szobaszam = input("Adja meg a szobaszámot: ")
        datum = input("Adja meg a foglalás dátumát (év-hó-nap formátumban): ")

        try:
            foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
            if foglalas_datum < datetime.now():
                print("Érvénytelen dátum, próbáld újra.")
                return
        except ValueError:
            print("Érvénytelen dátumformátum, próbáld újra.")
            return

        ar = self.szalloda.foglalas(szobaszam, datum)
        if ar is not None:
            print(f"Foglalás készítve a(z) {datum} dátumra a szoba árával: {ar}")
        else:
            print("Érvénytelen szobaszám, próbáld újra.")

    def foglalas_lemondasa(self):
        datum = input("Adja meg a lemondás dátumát (év-hó-nap formátumban): ")
        szobaszam = input("Adja meg a szobaszámot: ")

        try:
            lemondas_datum = datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            print("Érvénytelen dátumformátum, próbáld újra.")
            return

        for szoba in self.szalloda.szobak:
            foglalas = szoba.lemondas(datum)
            if foglalas:
                print(f"Foglalás lemondva a(z) {datum} dátumra a szobáról: {szobaszam}")
                return

        print("Érvénytelen szobaszám vagy dátum, próbáld újra.")
    def pelda_adatok_feltoltese(self):
        egyagyas1 = EgyagyasSzoba("101", 100)
        egyagyas2 = EgyagyasSzoba("102", 120, klima=False)
        ketagyas1 = KetagyasSzoba("201", 150, erkely=True)
        ketagyas2 = KetagyasSzoba("202", 180)

        self.szalloda.add_szoba(egyagyas1)
        self.szalloda.add_szoba(egyagyas2)
        self.szalloda.add_szoba(ketagyas1)
        self.szalloda.add_szoba(ketagyas2)

        self.szalloda.foglalas("101", "2023-12-01")
        self.szalloda.foglalas("201", "2023-12-02")
        self.szalloda.foglalas("102", "2023-12-01")
        self.szalloda.foglalas("201", "2023-12-03")
        self.szalloda.foglalas("202", "2023-12-04")

# Példa a használatra
szalloda = Szalloda("Luxury Hotel")
felhasznaloi_interfesz = FelhasznaloiInterfesz(szalloda)
felhasznaloi_interfesz.futtat()
