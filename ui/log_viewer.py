import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class LogViewer(tk.Frame):
    def __init__(self, master, width=50, height=10):
        super().__init__(master)
        self.text = ScrolledText(self, width=width, height=height, state='normal', wrap='none')
        self.text.pack(fill='both', expand=True)

    def append(self, line):
        self.text.insert('end', line + '\n')
        self.text.see('end')

    def clear(self):
        self.text.delete('1.0', 'end')
