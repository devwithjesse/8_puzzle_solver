from ui.app_window import PuzzleApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("8-Puzzle Solver")
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
