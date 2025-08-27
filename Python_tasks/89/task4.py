
import string

def is_palindrome(text): # sjekker at det er palindrom

    text = text.lower() # gjer tekst om til små bokstaver for å ignorere store ogsmå bokstaver

    cleaned = ''.join(char for char in text if char in string.ascii_lowercase) # fjerner allt som ikke er bokstaver A til Z, til og mefd mellomrom og skilletegn

    return cleaned == cleaned[::-1] # sjekker om teksten er lik når den leses baklengs

# hovedprogrammet starter
if __name__ == "__main__":

    while True:
        user_input = input("\nSkriv inn ett ord eller en setning for å sjekke om det er ett palindrom: ") # brukeren ska skrive inn tekst


        if not user_input.strip(): # sjekker om brukeren skrev inn en tom string (mellomrom er tomt)
            print("Du må skrive inn tekst.")

        elif not any(char.isalpha() for char in user_input): # sjekker om teksten har minst en bokstav
            print("Du må skrive inn ett ord, ikke bare tall eller symbol.")

        else:
            if is_palindrome(user_input): # hvis input er gyldig så sjekke om det er et palindrom
                print("Dette er ett palindrom!")
            else:
                print("Dette er ikke ett palindrom.")

        again = input("Vil du sjekke ett nytt ord? (ja elelr nei): ").strip().lower() # spør brukeren om di vil sjekka nytt ord

        if again != "ja": #vis svaret ikke er ja så avslutte programme
            print("Avslutter programmet. Ha en fin dag!")
            break
