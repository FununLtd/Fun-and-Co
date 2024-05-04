from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def __str__(self):
        pass

class EgyagyasSzoba(Szoba):
    def __str__(self):
        return f"Egyágyas Szoba #{self.szobaszam}, Ár: {self.ar} Ft"

class KetagyasSzoba(Szoba):
    def __str__(self):
        return f"Kétágyas Szoba #{self.szobaszam}, Ár: {self.ar} Ft"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        if datetime.strptime(datum, '%Y-%m-%d') < datetime.now():
            return "Ne élj a múltban."
        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                return "Erre a napra már lefoglalták ezt a szobát."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                self.foglalasok.append(Foglalas(szobaszam, datum, szoba.ar))
                return f"Foglalás sikeres. Ár: {szoba.ar} Ft"
        return "Nincs ilyen szobánk."

    def foglalas_lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return "Foglalás lemondva."
        return "Nincs ilyen foglalás."

    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Egyáltalán nincsenek foglalások."
        return '\n'.join(str(f) for f in self.foglalasok)

class Foglalas:
    def __init__(self, szobaszam, datum, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.ar = ar

    def __str__(self):
        return f"Foglalás: Szoba #{self.szobaszam}, Dátum: {self.datum}, Ár: {self.ar} Ft"

def felhasznalo_interfesz(szalloda):
    while True:
        print("\nVálassz egy opciót:\n1 - Foglalás\n2 - Foglalás lemondása\n3 - Foglalások listázása\n4 - Kilépés")
        valasztas = input("Opció: ")
        if valasztas == '1':
            szobaszam = int(input("Szobaszám: "))
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            print(szalloda.foglalas(szobaszam, datum))
        elif valasztas == '2':
            szobaszam = int(input("Szobaszám a lemondáshoz: "))
            datum = input("Dátum a lemondáshoz (ÉÉÉÉ-HH-NN): ")
            print(szalloda.foglalas_lemondas(szobaszam, datum))
        elif valasztas == '3':
            print(szalloda.foglalasok_listaja())
        elif valasztas == '4':
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás.")

# Szálloda és szobák inicializálása
szalloda = Szalloda("Budapest Hotel")
szalloda.szoba_hozzaadas(EgyagyasSzoba(101, 10000))
szalloda.szoba_hozzaadas(KetagyasSzoba(102, 15000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(103, 9000))

# Kezdő foglalások
szalloda.foglalas(101, "2024-06-20")
szalloda.foglalas(102, "2024-06-21")
szalloda.foglalas(103, "2024-06-19")
szalloda.foglalas(101, "2024-06-23")
szalloda.foglalas(102, "2024-06-25")

# Felhasználói interfész elindítása
felhasznalo_interfesz(szalloda)


