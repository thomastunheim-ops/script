import tkinter as tk
import re

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_gui()

    def setup_window(self):
        self.root.title("Modern Passordstyrke-analyse")
        self.root.geometry("380x520")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)

    def create_gui(self):
        title = tk.Label(self.root, text="🔒 Passordstyrke-analyse",
                         font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white')
        title.pack(pady=14)

        # Input
        self.entry_var = tk.StringVar()
        entry = tk.Entry(self.root, textvariable=self.entry_var,
                         font=('Arial', 16), bg='#2a2a2a', fg='white',
                         insertbackground="white", relief=tk.FLAT)
        entry.pack(fill=tk.X, padx=20, pady=6, ipady=10)

        # Resultat (vi beholder en StringVar, men trenger også label ref for farge)
        self.result_var = tk.StringVar(value="Skriv inn et passord og trykk Analyser")
        self.result_label = tk.Label(self.root, textvariable=self.result_var,
                                     font=('Arial', 13), bg='#2a2a2a', fg='white',
                                     wraplength=340, justify="center", height=6)
        self.result_label.pack(fill=tk.X, padx=20, pady=12)

        # Knapper
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        buttons = [
            ("Analyser", 0, 0, '#ff6b35'),
            ("Tøm", 0, 1, '#64b5f6'),
            ("Avslutt", 1, 0, '#f44336')
        ]

        for text, row, col, color in buttons:
            btn = tk.Button(button_frame, text=text, font=('Arial', 14, 'bold'),
                            bg=color, fg='white', relief=tk.FLAT, bd=0,
                            command=lambda t=text: self.button_click(t))
            # Avslutt knappen tar begge kolonner
            colspan = 2 if text == "Avslutt" else 1
            btn.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=6, pady=6)

        # Grid
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def button_click(self, action):
        if action == "Analyser":
            pwd = self.entry_var.get()
            text, color = self.analyze_password(pwd)
            self.result_var.set(text)
            self.result_label.config(bg=color)
        elif action == "Tøm":
            self.entry_var.set("")
            self.result_var.set("Skriv inn et passord og trykk Analyser")
            self.result_label.config(bg='#2a2a2a')
        elif action == "Avslutt":
            self.root.quit()

    # --- Ny, forbedret del: del opp i "segmenter" ved typeendring (bokstav/tall/symbol) og CamelCase ---
    def count_segments(self, s: str) -> int:
        if not s:
            return 0

        def ch_type(c):
            if c.isalpha():
                return 'L'
            if c.isdigit():
                return 'D'
            return 'S'  # symbol / annet

        segments = []
        current = s[0]
        cur_type = ch_type(s[0])

        for ch in s[1:]:
            t = ch_type(ch)
            # split når type endres (f.eks. bokstav -> tall, tall -> symbol)
            if t != cur_type:
                segments.append((current, cur_type))
                current = ch
                cur_type = t
            else:
                # split også ved camelCase (lower -> Upper innenfor letter-type)
                if cur_type == 'L' and current[-1].islower() and ch.isupper():
                    segments.append((current, cur_type))
                    current = ch
                    cur_type = 'L'
                else:
                    current += ch
        segments.append((current, cur_type))

        # tell kun "meningsfulle" segmenter: bokstaver eller tall (ikke rene symbol-segmenter)
        word_like = [seg for seg, t in segments if t in ('L', 'D')]
        return len(word_like)

    def analyze_password(self, password: str):
        if not password:
            return ("⚠️ Vennligst skriv inn et passord.", '#2a2a2a')

        feedback = []

        # krav
        length_ok = len(password) >= 12
        has_digit = any(ch.isdigit() for ch in password)
        has_special = any(not ch.isalnum() for ch in password)  # spesialtegn = ikke alfanumerisk
        segments = self.count_segments(password)
        multi_segment = segments >= 2

        # samle hva som mangler
        if not length_ok:
            feedback.append("❌ For kort (må være minst 12 tegn).")
        if not has_digit:
            feedback.append("❌ Mangler tall.")
        if not has_special:
            feedback.append("❌ Mangler spesialtegn.")
        if not multi_segment:
            feedback.append("❌ Består bare av ett sammenhengende segment/ord. Bruk flere ord/segmenter eller skil med symboler/bindestrek/CamelCase.")

        # hvis alt bra:
        if not feedback:
            text = "✅ Sterkt passord! Oppfyller lengde, tall, spesialtegn og flere segmenter."
            color = '#2ecc71'  # grønn
            return (text, color)

        # Ellers returner hva som mangler — og farge avhengig av hvor mange krav som er oppfylt
        passed = sum([length_ok, has_digit, has_special, multi_segment])
        if passed >= 3:
            color = '#f1c40f'  # gul (nesten bra)
        else:
            color = '#e74c3c'  # rød (svakt)

        text = "🔴 Ikke sterkt nok:\n\n" + "\n".join(feedback)
        return (text, color)

def main():
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
