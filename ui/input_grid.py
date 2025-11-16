import tkinter as tk

class InputGrid(tk.Frame):
    def __init__(self, master, prefix='G'):
        super().__init__(master)
        self.entries = []
        for r in range(3):
            row = []
            for c in range(3):
                e = tk.Entry(self, width=3, justify='center')
                e.grid(row=r, column=c, padx=2, pady=2)
                row.append(e)
            self.entries.append(row)

    def get_values(self):
        # returns list of lists of text values (strings)
        return [[e.get().strip() for e in row] for row in self.entries]

    def set_values(self, state):
        # state: tuple/list of 9 ints
        flat = list(state)
        for i, e in enumerate([ent for row in self.entries for ent in row]):
            e.delete(0, 'end')
            e.insert(0, str(flat[i]))

    def clear(self):
        for row in self.entries:
            for e in row:
                e.delete(0, 'end')
