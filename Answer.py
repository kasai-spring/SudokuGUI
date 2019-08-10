import tkinter as tk
from tkinter import ttk


class Answer:
    puzzle = None

    def __init__(self, puzzle, width, height):
        self.puzzle = puzzle
        answer_window = tk.Toplevel()
        answer_window.geometry(str(width) + "x" + str(height))
        self.puzzle_answer_scene(answer_window).pack(expand=True, fill=tk.BOTH, side="top", anchor=tk.CENTER)

    def puzzle_answer_scene(self, window):
        puzzle_answer_frame = ttk.Frame(window)
        self.create_answer_widget(puzzle_answer_frame).pack(expand=True, fill="both", side="top")
        back_button = ttk.Button(puzzle_answer_frame, text="閉じる", command=window.destroy)
        back_button.pack(expand="True", fill="x", padx=40, side="left")
        return puzzle_answer_frame

    def create_answer_widget(self, frame):
        max_column = 0
        puzzle_frame = ttk.Frame(frame)
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                max_column = max(len(self.puzzle[i]), max_column)
                entry = ttk.Entry(puzzle_frame, font=("Helvetica", 14), width=3)
                entry.grid(column=j, row=i, sticky=(tk.N, tk.S, tk.E, tk.W))
                entry.insert(0, self.puzzle[i][j])
                entry.configure(state="readonly")
        for i in range(len(self.puzzle)):  # 横
            puzzle_frame.grid_columnconfigure(i, weight=2)
        for i in range(max_column):  # 縦
            puzzle_frame.grid_rowconfigure(i, weight=1)
        return puzzle_frame
