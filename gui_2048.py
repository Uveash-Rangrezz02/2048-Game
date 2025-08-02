import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid = [[0]*4 for _ in range(4)]
        self.cells = []
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        background = tk.Frame(self.master, bg="#92877d")
        background.grid(sticky="nsew")
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(background, bg="#9e948a", width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(cell, text="", bg="#9e948a", justify=tk.CENTER, font=("Helvetica", 24, "bold"), width=4, height=2)
                label.grid()
                row.append(label)
            self.cells.append(row)

        self.master.bind("<Key>", self.key_handler)

    def start_game(self):
        self.add_tile()
        self.add_tile()
        self.update_ui()

    def add_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.grid[i][j] = random.choice([2]*9 + [4])

    def update_ui(self):
        colors = {
            2: ("#eee4da", "#776e65"),
            4: ("#ede0c8", "#776e65"),
            8: ("#f2b179", "#f9f6f2"),
            16: ("#f59563", "#f9f6f2"),
            32: ("#f67c5f", "#f9f6f2"),
            64: ("#f65e3b", "#f9f6f2"),
            128: ("#edcf72", "#f9f6f2"),
            256: ("#edcc61", "#f9f6f2"),
            512: ("#edc850", "#f9f6f2"),
            1024: ("#edc53f", "#f9f6f2"),
            2048: ("#edc22e", "#f9f6f2"),
        }

        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                if value == 0:
                    bg_color = "#9e948a"
                    fg_color = "#776e65"
                    display_text = ""
                else:
                    bg_color, fg_color = colors.get(value, ("#3c3a32", "#f9f6f2"))
                    display_text = str(value)

                self.cells[i][j].configure(
                    text=display_text,
                    bg=bg_color,
                    fg=fg_color
                )
        self.master.update_idletasks()

    def compress(self, row):
        new = [num for num in row if num != 0]
        new += [0] * (4 - len(new))
        return new

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move_left(self):
        changed = False
        new_grid = []
        for row in self.grid:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            if final != row:
                changed = True
            new_grid.append(final)
        self.grid = new_grid
        return changed

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        changed = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return changed

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def key_handler(self, event):
        key = event.keysym
        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()
        else:
            return

        if moved:
            self.add_tile()
            self.update_ui()
            if self.check_game_over():
                self.game_over()

    def game_over(self):
        over = tk.Toplevel(self.master)
        over.title("Game Over")
        tk.Label(over, text="Game Over!", font=("Helvetica", 20, "bold")).pack(padx=20, pady=20)
        tk.Button(over, text="Close", command=self.master.quit).pack(pady=10)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
