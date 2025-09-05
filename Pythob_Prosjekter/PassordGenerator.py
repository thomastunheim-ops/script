import tkinter as tk
import secrets
import random

class ModernPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_gui()

    def setup_window(self):
        self.root.title("Modern Passordgenerator")
        self.root.geometry("350x500")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)

    def create_gui(self):
        # Display
        self.password_var = tk.StringVar(value="Trykk 'Generer'")
        display = tk.Label(self.root, textvariable=self.password_var,
                          font=('Arial', 18, 'bold'), bg='#2a2a2a', fg='white',
                          height=3, wraplength=300, anchor='center', padx=10, pady=10)
        display.pack(fill=tk.X, padx=15, pady=15)

        # Knapperamme
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        buttons = [
            ("Generer", 0, 0, '#ff6b35'),
            ("Kopier", 0, 1, '#64b5f6'),
            ("Lengde +", 1, 0, '#333333'),
            ("Lengde -", 1, 1, '#333333'),
            ("Avslutt", 2, 0, '#f44336')
        ]

        for text, row, col, color in buttons:
            btn = tk.Button(button_frame, text=text, font=('Arial', 14, 'bold'),
                          bg=color, fg='white', relief=tk.FLAT, bd=0,
                          command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        # Grid config
        for i in range(3):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            button_frame.grid_columnconfigure(j, weight=1)

        # Standard lengde
        self.num_words = 3

    def button_click(self, action):
        if action == "Generer":
            pwd = self.generate_password()
            self.password_var.set(pwd)
        elif action == "Kopier":
            self.copy_password()
        elif action == "Lengde +":
            self.num_words += 1
        elif action == "Lengde -":
            if self.num_words > 2:
                self.num_words -= 1
        elif action == "Avslutt":
            self.root.quit()

    def generate_password(self):
        words = [
            "katt", "hund", "sol", "måne", "tre", "bil", "data", "sky", "fjell", "hav",
            "lys", "kode", "bok", "snø", "vann", "ild", "vind", "spill", "kraft", "natt"
        ]
        symbols = "!@#$%&*?-_+="
        chosen_words = [secrets.choice(words).capitalize() for _ in range(self.num_words)]
        number = str(secrets.randbelow(1000))  # tall fra 0–999
        symbol = secrets.choice(symbols)

        parts = chosen_words + [number, symbol]
        random.shuffle(parts)
        return "".join(parts)

    def copy_password(self):
        pwd = self.password_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.root.update()

def main():
    root = tk.Tk()
    app = ModernPasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
