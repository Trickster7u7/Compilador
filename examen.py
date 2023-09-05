import re
import tkinter as tk
from tkinter import ttk

class Lexer:
    def __init__(self):
        self.reserved_keywords = ['if', 'else', 'while', 'for', 'int', 'float', 'Cadena', 'print', 'programa', 'read', 'terminar', 'imprimir', 'public', 'static', 'void', 'main', 'Area', 'area', 'Base', 'base', 'altura', 'Altura']
        self.Simboloss = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '[', ']', '(', ')', '{', '}', ';', ',', '"', "'"]
        self.name = ['Diego', 'Gonzalez', 'Carpio','diego', 'gonzalez', 'carpio',]
        self.token_patterns = [
            ('VARIABLE', r'\$\w+'),
            ('Numero', r'^\-?[0-9]+(\.[0-9]+)?$|[0-9]+|-?[0-9]+'),
            ('reservada', r'\b(?:' + '|'.join(map(re.escape, self.reserved_keywords)) + r')\b'),
            ('Nombre', r'\b(?:' + '|'.join(map(re.escape, self.name)) + r')\b'),
            ('Identificador', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('Simbolos', '|'.join(map(re.escape, self.Simboloss))),
            ('SPACE', r'\s+'),
        ]
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)
        self.token_pattern = re.compile(self.token_regex)

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = self.token_pattern.match(text, position)
            if match:
                token_type = match.lastgroup
                if token_type != 'SPACE':
                    token_value = match.group(token_type)
                    tokens.append((token_type, token_value))
                position = match.end()
            else:
                position += 1
        return tokens

class LexerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Analizador léxico")

        self.text_label = tk.Label(text="ANALIZADOR LÉXICO ", height=2, width=50,)
        self.text_label.pack(pady=5)

        self.text_input = tk.Text(self.window, height=8, width=70, font=("Arial", 14))
        self.text_input.pack(pady=5)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text)
        self.analyze_button.grid(row=0, column=0, padx=30, pady=10)

        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text)
        self.clean_button.grid(row=0, column=1, padx=30, pady=10)

        self.tree = ttk.Treeview(self.window, columns=("Linea", "Token", "Funcion", "Reservada", "Identificador", "Símbolo", "Numero",), show="headings")
        self.tree.heading("Linea", text="Linea")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Funcion", text="Funcion")
        self.tree.heading("Reservada", text="Reservada")
        self.tree.heading("Identificador", text="Identificador")
        self.tree.heading("Símbolo", text="Símbolo")
        self.tree.heading("Numero", text="Numero")


        self.tree.pack()

    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        lines = text.split('\n')
        tokens_by_line = [lexer.tokenize(line) for line in lines]

        self.tree.delete(*self.tree.get_children())

        for line_number, line_tokens in enumerate(tokens_by_line, start=1):
            for token_type, token_value in line_tokens:
                row_data = [line_number, token_type, token_value, "", "", "", "","", ""]  
                if token_type == 'Numero':
                    row_data[6] = "x"
                elif token_type == 'reservada':
                    row_data[3] = "x"
                elif token_type == 'Identificador':
                    row_data[4] = "x"
                elif token_type == 'Simbolos':
                    row_data[5] = "x"
                elif token_type == 'operador':
                    row_data[7] = "x"

                self.tree.insert("", "end", values=row_data)

    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())

    def run(self):
        self.window.mainloop()

app = LexerApp()
app.run()
