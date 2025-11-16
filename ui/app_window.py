import tkinter as tk
from tkinter import ttk, messagebox
from .input_grid import InputGrid
from .log_viewer import LogViewer
from algorithms.uninformed_searches import bfs, dfs, dls, ids, bidirectional_search
from algorithms.informed_searches import a_star, uniform_cost_search, greedy_best_first_search, heuristics_map
from utils.puzzle_utils import state_from_entries, validate_state

class PuzzleApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(padx=12, pady=12)
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text='8-Puzzle Solver', font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=4, pady=(0,10))

        # Start and Goal grids
        tk.Label(self, text='Start State').grid(row=1, column=0)
        tk.Label(self, text='Goal State').grid(row=1, column=1)
        self.start_grid = InputGrid(self, prefix='S')
        self.start_grid.grid(row=2, column=0, padx=8)
        self.goal_grid = InputGrid(self, prefix='G')
        self.goal_grid.grid(row=2, column=1, padx=8)

        # Algorithm selection and options
        alg_frame = tk.Frame(self)
        alg_frame.grid(row=3, column=0, columnspan=2, pady=(10,0), sticky='w')
        tk.Label(alg_frame, text='Algorithm:').grid(row=0, column=0, sticky='w')
        self.alg_var = tk.StringVar(value='BFS')
        alg_menu = ttk.Combobox(
            alg_frame, 
            textvariable=self.alg_var, 
            values=[
                'BFS',
                'DFS',
                'DLS',
                'IDS',
                'Bidirectional',
                'A*',
                'UCS',
                'Greedy Best First Search'
                ], 
            state='readonly', 
            width=12
            )
        alg_menu.grid(row=0, column=1, padx=(6,12))

        tk.Label(alg_frame, text='Depth Limit:').grid(row=0, column=2, sticky='w')
        self.depth_entry = tk.Entry(alg_frame, width=5)
        self.depth_entry.grid(row=0, column=3, padx=(6,12))

        tk.Label(alg_frame, text='Heuristic:').grid(row=0, column=4, sticky='w')
        self.heur_var = tk.StringVar(value='manhattan')
        self.heur_menu = ttk.Combobox(alg_frame, textvariable=self.heur_var, values=list(heuristics_map.keys()), state='readonly', width=12)
        self.heur_menu.grid(row=0, column=5, padx=(6,12))

        # Solve / Reset / Close
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(8,0))

        solve_btn = tk.Button(btn_frame, text='SOLVE', width=10, command=self.on_solve)
        solve_btn.grid(row=0, column=0, padx=6)

        reset_btn = tk.Button(btn_frame, text='RESET', width=10, command=self.on_reset)
        reset_btn.grid(row=0, column=1, padx=6)

        close_btn = tk.Button(btn_frame, text='CLOSE', width=10, command=self.master.quit)
        close_btn.grid(row=0, column=2, padx=6)

        # Status labels
        status_frame = tk.Frame(self)
        status_frame.grid(row=5, column=0, columnspan=2, pady=(10,0), sticky='w')

        self.time_label = tk.Label(status_frame, text='Time taken: -')
        self.time_label.grid(row=0, column=0, sticky='w', padx=(0,12))

        self.complete_label = tk.Label(status_frame, text='Complete?: -')
        self.complete_label.grid(row=0, column=1, sticky='w', padx=(0,12))

        self.optimal_label = tk.Label(status_frame, text='Optimal?: -')
        self.optimal_label.grid(row=0, column=2, sticky='w', padx=(0,12))

        self.steps_label = tk.Label(status_frame, text='Moves: -')
        self.steps_label.grid(row=0, column=3, sticky='w', padx=(0,12))

        # Log viewer
        self.log = LogViewer(self, width=60, height=12)
        self.log.grid(row=6, column=0, columnspan=2, pady=(8,0))

    def on_reset(self):
        self.start_grid.clear()
        self.goal_grid.clear()
        self.log.clear()
        self.time_label.config(text='Time taken: -')
        self.complete_label.config(text='Complete?: -')
        self.optimal_label.config(text='Optimal?: -')
        self.steps_label.config(text='Moves: -')

    def on_solve(self):
        try:
            start = state_from_entries(self.start_grid.get_values())
            goal = state_from_entries(self.goal_grid.get_values())
        except ValueError as e:
            messagebox.showerror('Invalid input', str(e))
            return

        # Choose algorithm
        alg = self.alg_var.get()
        self.log.clear()

        import time
        t0 = time.time()

        if alg == 'BFS':
            result = bfs(start, goal)
        elif alg == 'DFS':
            result = dfs(start, goal)
        elif alg == 'DLS':
            try:
                limit = int(self.depth_entry.get())
            except:
                messagebox.showerror('Invalid input', 'Depth limit must be an integer for DLS.')
                return
            result = dls(start, goal, limit)
        elif alg == 'IDS':
            result = ids(start, goal)
        elif alg == 'Bidirectional':
            result = bidirectional_search(start, goal)
        elif alg == 'A*':
            hname = self.heur_var.get()
            result = a_star(start, goal, heuristic=heuristics_map[hname])
        elif alg == 'UCS':
            result = uniform_cost_search(start, goal)
        elif alg == 'Greedy Best First Search':
            hname = self.heur_var.get()
            result = greedy_best_first_search(start, goal, heuristic=heuristics_map[hname])
        t1 = time.time()

        if result is None:
            self.log.append('No solution found.')
            self.complete_label.config(text='Complete?: NO')
            self.optimal_label.config(text='Optimal?: -')
            self.time_label.config(text=f'Time taken: {t1 - t0:.4f}s')
            self.steps_label.config(text='Moves: -')
            return

        path, moves = result  # path: list of states, moves: list of move descriptions

        # Log results
        for i, (state, mv) in enumerate(zip(path, ['Start'] + moves)):
            self.log.append(f"{i}/{len(moves)} | {mv} | {state}")

        self.time_label.config(text=f'Time taken: {t1 - t0:.4f}s')
        self.complete_label.config(text='Complete?: YES')

        self.optimal_label.config(text='Optimal?: YES' if alg in ('BFS','A*', 'Bidirectional', 'IDS', 'UCS') else 'Optimal?: NO')
        self.steps_label.config(text=f'Moves: {len(moves)}')

