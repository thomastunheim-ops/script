
# klasse for meny
class Menu:
    def __init__(self):
        # en tom liste
        self.options = []

        self.add_option("Åpne ny konto") # legge til menyvalg
        self.add_option("Sett inn penger på konto")
        self.add_option("Ta ut penger fra kontoen")
        self.add_option("Legg til renter på konto")
        self.add_option("Se saldoen på kontoen din")
        self.add_option("Gå ut")

    def add_option(self, option):
        # adder en menyvalg i listen
        self.options.append(option)

    def get_input(self):
        # viser meny og leser brukerens valg
        print("\n=== Meny ===")
        for i, text in enumerate(self.options, start=1):
            print(f"{i}. {text}")
        try:
            return int(input("Velg et alternativ (1-6): "))
        except:
            return 0  # returnerer 0 vis det er ikek gyldig input

# klasse for bankkonto
class BankAccount:
    def __init__(self):
        self.balance = 0.0  # konto starter med 0 kr i den

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Du satte inn {amount} kr.")
        else:
            print("Beløpet må være positivt beløp.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Du tok ut {amount} kr.")
        else:
            print("Ugyldig beløp eller for lite penger på kontoen.")

    def add_interest(self):
        rente = self.balance * 0.05
        self.balance += rente
        print(f"5 % rente lagt til: {rente:.2f} kr.")

    def get_balance(self):
        print(f"Saldoen på kontoen din er: {self.balance:.2f} kr.")

# hovedprogramet
if __name__ == "__main__":
    account = None # kontoen er ikke opprettet ennå
    menu = Menu() # lage menyobjekt

    while True:
        choice = menu.get_input() # hente bruker valg

        if choice == 1: #tall i menyen
            account = BankAccount()
            print("Ny konto oppretta.")

        elif choice == 2:
            if account:
                try:
                    amount = float(input("Skriv inn beløpet du vil sette inn på kontoen: "))
                    account.deposit(amount)
                except:
                    print("Skriv et tall.")
            else:
                print("Du må opprette en konto først.") # gjenntar om bruker ikke lager konto før han skriver andre tall

        elif choice == 3:
            if account:
                try:
                    amount = float(input("Skriv inn beløpet du vil ta ut: "))
                    account.withdraw(amount)
                except:
                    print("Skriv et tall.")
            else:
                print("Du må opprette en konto først.")

        elif choice == 4:
            if account:
                account.add_interest()
            else:
                print("Du må opprette en konto først.")

        elif choice == 5:
            if account:
                account.get_balance()
            else:
                print("Du må opprette en konto først.")

        elif choice == 6:
            print("Ha det bra")
            break

        else:
            print("Ugyldig valg kan du prøv igjen.")
