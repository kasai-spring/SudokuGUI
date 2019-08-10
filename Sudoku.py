import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Solve import Solve
from Answer import Answer


def popup_message(code, title, message):  # 0:情報, 1:警告, 2:エラー
    if code == 0:
        messagebox.showinfo(title, message)
    elif code == 1:
        messagebox.showwarning(title, message)
    elif code == 2:
        messagebox.showerror(title, message)


class Sudoku(tk.Frame):  # GUI関係
    puzzle = [[0 for i in range(9)] for j in range(9)]
    puzzle_entry_list = []
    input_frame, answer_frame = None, None

    def __init__(self, master=None):
        super().__init__(master)
        self.input_frame = self.puzzle_input_scene()
        self.input_frame.pack(expand=True, fill=tk.BOTH, side="top", anchor=tk.CENTER)

    def puzzle_input_scene(self):
        puzzle_input_frame = ttk.Frame(root)
        self.create_input_widget(puzzle_input_frame).pack(expand=True, fill=tk.BOTH, side="top", anchor=tk.CENTER)
        submit_button = ttk.Button(puzzle_input_frame, text="solve", command=self.assign_list)
        submit_button.pack(expand=True, fill="x", padx=40, side="left")
        reset_button = ttk.Button(puzzle_input_frame, text="reset", command=self.reset_input_puzzle_frame)
        reset_button.pack(expand=True, fill="x", padx=40, side="left")
        return puzzle_input_frame

    def create_input_widget(self, frame):
        max_column = 0
        puzzle_frame = ttk.Frame(frame)
        v_cmd_t = (self.register(self.validate), '%s', '%S', '%V', '%W')
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                max_column = max(len(self.puzzle[i]), max_column)
                self.puzzle_entry_list.append(
                    ttk.Entry(puzzle_frame, validate="focusout", validatecommand=v_cmd_t, width=3,
                              font=("Helvetica", 14)))
                self.puzzle_entry_list[-1].grid(column=j, row=i, sticky=(tk.N, tk.S, tk.E, tk.W))
                self.puzzle_entry_list[-1].insert(0, 0)
                pass
        for i in range(len(self.puzzle)):  # 横
            puzzle_frame.grid_columnconfigure(i, weight=2)
        for i in range(max_column):  # 縦
            puzzle_frame.grid_rowconfigure(i, weight=1)
        return puzzle_frame

    def reset_input_puzzle_frame(self):
        self.input_frame.destroy()
        self.input_frame = self.puzzle_input_scene()
        self.input_frame.pack(expand=True, fill=tk.BOTH, side="top", anchor=tk.CENTER)
        pass

    def validate(self, s, _s, _v, w):
        try:
            if s == "":  # 何も入力されてないときにまでポップアップだしたら煩わしいため
                target_entry = self.nametowidget(w)
                target_entry.delete(0, tk.END)
                target_entry.insert(0, 0)
                return False
            num = int(s)
            if not 0 <= num <= 9:
                raise OverflowError
        except ValueError:
            target_entry = self.nametowidget(w)
            target_entry.delete(0, tk.END)
            target_entry.insert(0, 0)
            popup_message(1, "入力エラー", "数字を入力してください")
            return False
        except OverflowError:
            target_entry = self.nametowidget(w)
            target_entry.delete(0, tk.END)
            target_entry.insert(0, 0)
            popup_message(1, "入力エラー", "0-9以内の数字を入力してください")
            return False

        return True

    def assign_list(self):
        count = 0
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                self.puzzle[i][j] = int(self.puzzle_entry_list[count].get())
                count += 1
        try:
            solve = Solve(self.puzzle)
            answer_multiple, answer_puzzle = solve.solve()
            if not answer_puzzle:
                popup_message(2, "演算エラー", "答えが見つかりませんでした")
            else:
                if answer_multiple:
                    popup_message(0, "情報", "答えが二個以上存在します\nそのうちの一つだけ表示します")
                Answer(answer_puzzle, root.winfo_width(), root.winfo_height())
        except ArithmeticError as e:
            popup_message(2, "入力エラー", "入力された内容が誤ってる可能性があります\nエラーが発生した箇所:" + str(e))


root = tk.Tk()
root.columnconfigure(0, weight=1)
root.title("数独")
application = Sudoku(master=root)
application.mainloop()
