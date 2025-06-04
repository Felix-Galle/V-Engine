import sys
import os
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from lexer import Lexer
from parser import Parser
from game import Game
from io import StringIO

class VEngineGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("V-Engine GUI")
        self.geometry("800x600")
        self.script_file = None

        self.create_widgets()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self)
        menubar.add_command(label="Open Script", command=self.open_script)
        menubar.add_command(label="Exit", command=self.quit)
        self.config(menu=menubar)

        # Script display
        self.script_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20)
        self.script_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Run button
        self.run_button = tk.Button(self, text="Run Script", command=self.run_script)
        self.run_button.pack(pady=5)

        # Output display
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def open_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("V Scripts", "*.v")])
        if file_path:
            self.script_file = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.script_text.delete('1.0', tk.END)
            self.script_text.insert(tk.END, content)
            logging.info(f"Loaded script: {file_path}")

    def run_script(self):
        try:
            text = self.script_text.get('1.0', tk.END)
            win, scenes = Parser(Lexer(text)).parse()
            logging.info("Script parsed successfully. Running game...")
            # Redirect stdout temporarily
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            try:
                Game(win, scenes).run(scenes[0].name)
            finally:
                sys.stdout = old_stdout
            output = mystdout.getvalue()
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, output)
            self.output_text.config(state='disabled')
            logging.info("Game run complete.")
        except Exception as e:
            logging.info(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def log(self, message):
        logging.info(message)
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"[LOG] {message}\n")
        self.output_text.config(state='disabled')

if __name__ == "__main__":
    app = VEngineGUI()
    app.mainloop()