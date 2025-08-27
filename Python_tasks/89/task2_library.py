
# denne klassen skal være en bok
class Book:
    def __init__(self, tittel, forfatter, sider): #starter bokobjektet med tittel, forfatter og kor mange side
        self.tittel = tittel
        self.forfatter = forfatter
        self.sider = sider
        self.tilgjengelig = True # boken er ledig som standard ikke som utlånt

# klasse som er biblioteket
class Library:
    def __init__(self):# lage en tom liste       
        self.boker = []

    def legg_til_bok(self, bok): # legger til en bok i biblioteket
        self.boker.append(bok)
        print(f"La til: {bok.tittel}")

    def fjern_bok(self, tittel): # fjerner bok med tittelen

        for bok in self.boker:
            if bok.tittel.lower() == tittel.lower():
                self.boker.remove(bok)
                print(f"Fjerna: {tittel}")
                return
        print(f"Fant ikke boka: {tittel}")

    def laan_bok(self, tittel):# gjør en bok utilgjengelig eller lånt ut, hvis den finnes og hvis den ikkje allerede er utlånt
        for bok in self.boker:
            if bok.tittel.lower() == tittel.lower():
                if bok.tilgjengelig:
                    bok.tilgjengelig = False
                    print(f"Du lånte: {tittel}")
                else:
                    print("Boken er allerede utlånt.")
                return
        print("Boken finnes ikke i biblioteket.")

    def lever_bok(self, tittel):# gjør bok tilgjengelig igjen
        for bok in self.boker:
            if bok.tittel.lower() == tittel.lower():
                if not bok.tilgjengelig:
                    bok.tilgjengelig = True
                    print(f"Du leverte tilbake: {tittel}")
                else:
                    print("Boken var ikke utlånt.")
                return
        print("Boken finnes ikke i biblioteket.")

    def vis_boker(self): # skriver ut alle bøker i biblioteket og vise til statusen
        
        print("\nBøker i biblioteket:")
        for bok in self.boker:
            status = "Tilgjengelig" if bok.tilgjengelig else "Utlånt"
            print(f"- {bok.tittel} av {bok.forfatter} ({status})")
        print()

# her tester me systemet
if __name__ == "__main__":
    # lage bibliotek objektet
    bibliotek = Library()

    # lage to Harry Potter bøker
    bok1 = Book("Harry Potter og De Vises Stein", "J.K. Rowling", 320)
    bok2 = Book("Harry Potter og Mysteriekammeret", "J.K. Rowling", 341)

    # legger bøkene i biblioteket
    bibliotek.legg_til_bok(bok1)
    bibliotek.legg_til_bok(bok2)

    # låner og returnere en bok
    bibliotek.laan_bok("Harry Potter og De Vises Stein")
    bibliotek.lever_bok("Harry Potter og De Vises Stein")

    # fjerne en bok frå bibliotek
    bibliotek.fjern_bok("Harry Potter og Mysteriekammeret")

    # viser alle bøkene som er igjen
    bibliotek.vis_boker()