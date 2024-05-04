from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, nev, ar):
        self.szobaszam = szobaszam
        self.nev = nev
        self.ar = ar

    def __str__(self):
        return f"{self.nev} (Szoba #{self.szobaszam}, Ár: {self.ar} Ft)"

class EgyagyasSzoba(Szoba):
    pass

class KetagyasSzoba(Szoba):
    pass

class TizenKetagyasSzoba(Szoba):
    pass

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = {}

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum, pin_kod):
        if datetime.strptime(datum, '%Y-%m-%d') < datetime.now():
            return "A megadott dátum a múltban van."
        if not any(sz.szobaszam == szobaszam for sz in self.szobak):
            return "Nem létező szobaszám."
        if datum in self.foglalasok and pin_kod in self.foglalasok[datum]:
            return "Ez a PIN kód már használatban van ezen a dátumon."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                self.foglalasok.setdefault(datum, {})[pin_kod] = (szoba, pin_kod)
                return f"Foglalás sikeres. Ár: {szoba.ar} Ft"
        return "A megadott szobaszám nem létezik."

    def foglalas_lemondas(self, szobaszam, datum, pin_kod):
        if datum in self.foglalasok and pin_kod in self.foglalasok[datum] and \
           self.foglalasok[datum][pin_kod][0].szobaszam == szobaszam:
            del self.foglalasok[datum][pin_kod]
            if not self.foglalasok[datum]:
                del self.foglalasok[datum]
            return "Foglalás lemondva."
        return "Nincs ilyen foglalás, vagy hibás PIN kód."

    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        result = []
        for datum, foglalasok in self.foglalasok.items():
            for pin_kod, (szoba, _) in foglalasok.items():
                result.append(f"Dátum: {datum}, {szoba}, PIN: {pin_kod}")
        return '\n'.join(result)

def felhasznalo_interfesz(szalloda):
    while True:
        print("\nVálasszon egy opciót:\n1 - Foglalás\n2 - Foglalás lemondása\n3 - Foglalások listázása\n4 - Kilépés")
        valasztas = input("Opció: ")
        if valasztas == '1':
            szobaszam = int(input("Szobaszám: "))
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            pin_kod = input("Adjon meg egy 4 számjegyű PIN kódot: ")
            print(szalloda.foglalas(szobaszam, datum, pin_kod))
        elif valasztas == '2':
            szobaszam = int(input("Szobaszám a lemondáshoz: "))
            datum = input("Dátum a lemondáshoz (ÉÉÉÉ-HH-NN): ")
            pin_kod = input("Adja meg a foglaláshoz használt PIN kódot: ")
            print(szalloda.foglalas_lemondas(szobaszam, datum, pin_kod))
        elif valasztas == '3':
            print(szalloda.foglalasok_listaja())
        elif valasztas == '4':
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás.")

# Szálloda és szobák inicializálása
szalloda = Szalloda("The Moxxi's")
szalloda.szoba_hozzaadas(EgyagyasSzoba(101, "Leánybúcsú lakosztály", 10000))
szalloda.szoba_hozzaadas(KetagyasSzoba(102, "Legénybúcsú lakosztály", 15000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(103, "Ad-hoc romance", 9000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(104, "Forbidden love", 11000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(105, "Csak TV-znénk a gyerekek nélkül", 7000))
szalloda.szoba_hozzaadas(TizenKetagyasSzoba(112, "Wall Street farkasa ceges buli", 4155000))

# Felhasználói interfész elindítása
felhasznalo_interfesz(szalloda)
