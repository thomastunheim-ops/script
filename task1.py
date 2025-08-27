# Kandidatnummer: 89 og 75

import random
import os

# klasse som viser til ordspillet
class WordGame:
    def __init__(self, word_file):
        self.word = self._choose_word(word_file) # velger tilfeldig ord
        self.guessed = ['_' for _ in self.word] # lager liste med "_" for kvær bokstav
        self.attempts_left = len(self.word) # antall feilforsøk somm kan bli gjort er same som lengden på ordene
        self.guessed_letters = set() # holder styr på kefor en bokstaver som er gjetta på

    # leser filen og velger et tilfeldig ord fra filen
    def _choose_word(self, path):
        try:
            with open(path, 'r') as file:
                return random.choice([w.strip().lower() for w in file if w.strip()])
        except FileNotFoundError:
            print("Fant ikke ordlista.")
            exit()

    # kjører spille
    def play(self):
        print(f"Ordet har {len(self.word)} bokstaver. Du har {self.attempts_left} forsøk.\n")

        # spillet kjører så lenge spilleren har forsøk igjen, og ikke har gjetta heile ordet
        while self.attempts_left and '_' in self.guessed:
            print(' '.join(self.guessed)) # viser ordet med _ og riktige bokstav
            guess = input("Gjett en bokstav: ").lower()

            # sjekker at inputen er gyldig
            if len(guess) != 1 or not guess.isalpha():
                print("Skriv en bokstav (A-Z).\n")
                continue

            # hvis bokstaven er allerede har blitt gjetta, hoppe me over
            if guess in self.guessed_letters:
                print("Du har allerede prøvd den bokstaven.\n")
                continue

            self.guessed_letters.add(guess) # legger til bokstav i sett med gjetta bokstaver

            # hvis riktig bokstav så oppdater visningen
            if guess in self.word:
                self.guessed = [guess if c == guess else g for c, g in zip(self.word, self.guessed)]
            else:
                self.attempts_left -= 1 # feil bokstav så trekk ett forsøk
                print("Feil bokstav.")

            # viser antall forsøk så erigjen
            print(f"Prøv igjen: {self.attempts_left}\n{'-'*30}")

        # viser resultatene
        if '_' not in self.guessed:
            print(f"\nDu fant ordet: \"{self.word}\" - Gratulerer!")
        else:
            print(f"\nDu tapte. Ordet var: \"{self.word}\"")

# starter spillet til slutt
if __name__ == "__main__":
    # bruker absolutt bane slik at words.txt alltid finnes
    path = os.path.join(os.path.dirname(__file__), "words.txt")
    WordGame(path).play()
