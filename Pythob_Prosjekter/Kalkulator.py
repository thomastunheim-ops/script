import tkinter as tk
import math

class ModernKalkulator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Variabler
        self.current = '0'
        self.previous = ''
        self.operation = ''
        self.should_reset = False
        
        self.create_gui()
        
    def setup_window(self):
        self.root.title("Modern Kalkulator")
        self.root.geometry("350x500")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
    def create_gui(self):
        # Display
        self.display_var = tk.StringVar(value='0')
        display = tk.Label(self.root, textvariable=self.display_var,
                          font=('Arial', 24, 'bold'), bg='#2a2a2a', fg='white',
                          height=3, anchor='e', padx=20)
        display.pack(fill=tk.X, padx=15, pady=15)
        
        # Knapper
        self.create_buttons()
        
    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        buttons = [
            ('C', 0, 0, '#f44336'), ('±', 0, 1, '#64b5f6'), ('%', 0, 2, '#64b5f6'), ('÷', 0, 3, '#ff6b35'),
            ('7', 1, 0, '#333333'), ('8', 1, 1, '#333333'), ('9', 1, 2, '#333333'), ('×', 1, 3, '#ff6b35'),
            ('4', 2, 0, '#333333'), ('5', 2, 1, '#333333'), ('6', 2, 2, '#333333'), ('−', 2, 3, '#ff6b35'),
            ('1', 3, 0, '#333333'), ('2', 3, 1, '#333333'), ('3', 3, 2, '#333333'), ('+', 3, 3, '#ff6b35'),
            ('0', 4, 0, '#333333'), ('.', 4, 1, '#333333'), ('⌫', 4, 2, '#64b5f6'), ('=', 4, 3, '#ff6b35')
        ]
        
        for text, row, col, color in buttons:
            btn = tk.Button(button_frame, text=text, font=('Arial', 16, 'bold'),
                          bg=color, fg='white', relief=tk.FLAT, bd=0,
                          command=lambda t=text: self.button_click(t))
            
            columnspan = 2 if text == '0' else 1
            btn.grid(row=row, column=col, columnspan=columnspan, 
                    sticky='nsew', padx=3, pady=3)
        
        # Grid konfiguration
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def button_click(self, char):
        if char.isdigit() or char == '.':
            self.input_number(char)
        elif char in ['÷', '×', '−', '+']:
            self.set_operator(char)
        elif char == '=':
            self.calculate()
        elif char == 'C':
            self.clear()
        elif char == '±':
            self.toggle_sign()
        elif char == '%':
            self.percent()
        elif char == '⌫':
            self.backspace()
    
    def input_number(self, num):
        if self.should_reset:
            self.current = '0'
            self.should_reset = False
        
        if self.current == '0' and num != '.':
            self.current = num
        elif num == '.' and '.' not in self.current:
            self.current += num
        elif num != '.':
            self.current += num
        
        self.update_display()
    
    def set_operator(self, op):
        if self.operation and not self.should_reset:
            self.calculate()
        
        self.previous = self.current
        self.operation = op
        self.should_reset = True
    
    def calculate(self):
        if not self.operation or not self.previous:
            return
        
        try:
            prev = float(self.previous)
            curr = float(self.current)
            
            if self.operation == '+':
                result = prev + curr
            elif self.operation == '−':
                result = prev - curr
            elif self.operation == '×':
                result = prev * curr
            elif self.operation == '÷':
                result = prev / curr if curr != 0 else float('inf')
            
            self.current = str(int(result) if result == int(result) else round(result, 8))
            self.operation = ''
            self.previous = ''
            self.should_reset = True
            
        except:
            self.current = 'Error'
            self.should_reset = True
        
        self.update_display()
    
    def clear(self):
        self.current = '0'
        self.previous = ''
        self.operation = ''
        self.should_reset = False
        self.update_display()
    
    def toggle_sign(self):
        if self.current != '0':
            self.current = self.current[1:] if self.current.startswith('-') else '-' + self.current
            self.update_display()
    
    def percent(self):
        try:
            self.current = str(float(self.current) / 100)
            self.should_reset = True
            self.update_display()
        except:
            pass
    
    def backspace(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = '0'
        self.update_display()
    
    def update_display(self):
        display_text = self.current[:12]  # Begrens lengde
        self.display_var.set(display_text)

def main():
    root = tk.Tk()
    app = ModernKalkulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()