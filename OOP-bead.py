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

    def validate_date(self, datum):
        try:
            datetime.strptime(datum, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def foglalas(self, szobaszam, datum, pin_kod):
        if not self.validate_date(datum):
            return "\033[91mA megadott dátum érvénytelen vagy nem létezik.\033[0m"
        if datetime.strptime(datum, '%Y-%m-%d') < datetime.now():
            return "\033[91mA megadott dátum a múltban van.\033[0m"
        if not any(sz.szobaszam == szobaszam for sz in self.szobak):
            return "\033[91mNem létező szobaszám.\033[0m"
        if not pin_kod.isdigit() or len(pin_kod) < 4:
            return "\033[91mA PIN kód legalább 4 számjegyű kell legyen és csak számokat tartalmazhat.\033[0m"
        if datum in self.foglalasok and any(pin_kod == p[1] for p in self.foglalasok[datum].values()):
            return "\033[91mEz a PIN kód már használatban van ezen a dátumon.\033[0m"
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                self.foglalasok.setdefault(datum, {})[szobaszam] = (szoba, pin_kod)
                return f"\033[92mFoglalás sikeres. Ár: {szoba.ar} Ft\033[0m"
        return "\033[91mA megadott szobaszám nem létezik.\033[0m"

    def foglalas_lemondas(self, szobaszam, datum, pin_kod):
        if datum in self.foglalasok and szobaszam in self.foglalasok[datum] and \
           self.foglalasok[datum][szobaszam][1] == pin_kod:
            del self.foglalasok[datum][szobaszam]
            if not self.foglalasok[datum]:
                del self.foglalasok[datum]
            return "\033[92mFoglalás lemondva.\033[0m"
        return "\033[91mNincs ilyen foglalás, vagy hibás PIN kód.\033[0m"

    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        result = []
        for szoba in self.szobak:
            foglalasok = [datum for datum, foglalas in self.foglalasok.items() if szoba.szobaszam in foglalas]
            if foglalasok:
                result.append(f"{szoba} foglalt időpontok:")
                result.extend(sorted(foglalasok))
        return '\n'.join(result)

    def szobak_kilistazasa(self):
        return '\n'.join(str(szoba) for szoba in self.szobak)

def felhasznalo_interfesz(szalloda):
    while True:
        print("\nElérhető szobák:")
        print(szalloda.szobak_kilistazasa())
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
            print("\033[91mÉrvénytelen választás.\033[0m")

# Szálloda és szobák inicializálása
szalloda = Szalloda("The Moxxi's")
szalloda.szoba_hozzaadas(EgyagyasSzoba(101, "Leánybúcsú lakosztály", 10000))
szalloda.szoba_hozzaadas(KetagyasSzoba(102, "Legénybúcsú lakosztály", 15000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(103, "Ad-hoc romance", 9000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(104, "Forbidden love", 11000))
szalloda.szoba_hozzaadas(EgyagyasSzoba(105, "Csak TV-znénk a gyerekek nélkül", 7000))
szalloda.szoba_hozzaadas(TizenKetagyasSzoba(112, "Wall Street farkasa ceges buli", 4155000))

# Kezdő foglalások
szalloda.foglalas(101, "2024-06-20", "1234")
szalloda.foglalas(101, "2024-07-15", "1235")
szalloda.foglalas(102, "2024-06-21", "2234")
szalloda.foglalas(102, "2024-07-16", "2235")
szalloda.foglalas(103, "2024-06-22", "3234")
szalloda.foglalas(103, "2024-07-17", "3235")
szalloda.foglalas(104, "2024-06-23", "4234")
szalloda.foglalas(104, "2024-07-18", "4235")
szalloda.foglalas(105, "2024-06-24", "5234")
szalloda.foglalas(105, "2024-07-19", "5235")
szalloda.foglalas(112, "2024-06-25", "6234")
szalloda.foglalas(112, "2024-07-20", "6235")

# Felhasználói interfész elindítása
print (r"""\
      {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
    {}                                                                                                    {}
    {}  HHHHHHHHH     HHHHHHHHH                          tttt                              lllllll        {}
    {}  H:::::::H     H:::::::H                       ttt:::t                              l:::::l        {}
    {}  H:::::::H     H:::::::H                       t:::::t                              l:::::l        {}
    {}  HH::::::H     H::::::HH                       t:::::t                              l:::::l        {}
    {}    H:::::H     H:::::H     ooooooooooo   ttttttt:::::ttttttt        eeeeeeeeeeee     l::::l        {}
    {}    H:::::H     H:::::H   oo:::::::::::oo t:::::::::::::::::t      ee::::::::::::ee   l::::l        {}
    {}    H::::::HHHHH::::::H  o:::::::::::::::ot:::::::::::::::::t     e::::::eeeee:::::ee l::::l        {}
    {}    H:::::::::::::::::H  o:::::ooooo:::::otttttt:::::::tttttt    e::::::e     e:::::e l::::l        {}
    {}    H:::::::::::::::::H  o::::o     o::::o      t:::::t          e:::::::eeeee::::::e l::::l        {}
    {}    H::::::HHHHH::::::H  o::::o     o::::o      t:::::t          e:::::::::::::::::e  l::::l        {}
    {}    H:::::H     H:::::H  o::::o     o::::o      t:::::t          e::::::eeeeeeeeeee   l::::l        {}
    {}    H:::::H     H:::::H  o::::o     o::::o      t:::::t    tttttte:::::::e            l::::l        {}
    {}  HH::::::H     H::::::HHo:::::ooooo:::::o      t::::::tttt:::::te::::::::e          l::::::l       {}
    {}  H:::::::H     H:::::::Ho:::::::::::::::o      tt::::::::::::::t e::::::::eeeeeeee  l::::::l       {}
    {}  H:::::::H     H:::::::H oo:::::::::::oo         tt:::::::::::tt  ee:::::::::::::e  l::::::l       {}
    {}  HHHHHHHHH     HHHHHHHHH   ooooooooooo             ttttttttttt      eeeeeeeeeeeeee  llllllll       {}
    {}  MMMMMMMM               MMMMMMMM                                                           iiii    {}
    {}  M:::::::M             M:::::::M                                                          i::::i   {}
    {}  M::::::::M           M::::::::M                                                           iiii    {}
    {}  M:::::::::M         M:::::::::M                                                                   {}
    {}  M::::::::::M       M::::::::::M   ooooooooooo   xxxxxxx      xxxxxxxxxxxxxx      xxxxxxxiiiiiii   {}
    {}  M:::::::::::M     M:::::::::::M oo:::::::::::oo  x:::::x    x:::::x  x:::::x    x:::::x i:::::i   {}
    {}  M:::::::M::::M   M::::M:::::::Mo:::::::::::::::o  x:::::x  x:::::x    x:::::x  x:::::x   i::::i   {}
    {}  M::::::M M::::M M::::M M::::::Mo:::::ooooo:::::o   x:::::xx:::::x      x:::::xx:::::x    i::::i   {}
    {}  M::::::M  M::::M::::M  M::::::Mo::::o     o::::o    x::::::::::x        x::::::::::x     i::::i   {}
    {}  M::::::M   M:::::::M   M::::::Mo::::o     o::::o     x::::::::x          x::::::::x      i::::i   {}
    {}  M::::::M    M:::::M    M::::::Mo::::o     o::::o     x::::::::x          x::::::::x      i::::i   {}
    {}  M::::::M     MMMMM     M::::::Mo::::o     o::::o    x::::::::::x        x::::::::::x     i::::i   {}
    {}  M::::::M               M::::::Mo:::::ooooo:::::o   x:::::xx:::::x      x:::::xx:::::x   i::::::i  {}
    {}  M::::::M               M::::::Mo:::::::::::::::o  x:::::x  x:::::x    x:::::x  x:::::x  i::::::i  {}
    {}  M::::::M               M::::::M oo:::::::::::oo  x:::::x    x:::::x  x:::::x    x:::::x i::::::i  {}
    {}  MMMMMMMM               MMMMMMMM   ooooooooooo   xxxxxxx      xxxxxxxxxxxxxx      xxxxxxxiiiiiiii  {}
    {}                                                                                                    {}
    {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
""")
felhasznalo_interfesz(szalloda)
