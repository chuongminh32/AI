import tkinter as tk
import time
import random
import math

# Sudoku puzzle: 0 là ô trống
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

board = [[puzzle[r][c] for c in range(9)] for r in range(9)]
fixed = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]

# Tkinter GUI setup
cell_size = 50
root = tk.Tk()
root.title("Sudoku Simulated Annealing")
canvas = tk.Canvas(root, width=9*cell_size, height=9*cell_size)
canvas.pack()

def get_conflict_matrix():
    # Tạo ma trận boolean 9x9: True nếu bị xung đột
    conflict_matrix = [[False for _ in range(9)] for _ in range(9)]

    # Kiểm tra xung đột hàng và cột
    for i in range(9):
        row_seen = {}
        col_seen = {}
        for j in range(9):
            r_val = board[i][j]
            c_val = board[j][i]
            # Hàng
            if r_val in row_seen:
                conflict_matrix[i][j] = True
                conflict_matrix[i][row_seen[r_val]] = True
            else:
                row_seen[r_val] = j
            # Cột
            if c_val in col_seen:
                conflict_matrix[j][i] = True
                conflict_matrix[col_seen[c_val]][i] = True
            else:
                col_seen[c_val] = j
    return conflict_matrix


def draw_board():
    canvas.delete("all")
    conflict = get_conflict_matrix()
    for i in range(9):
        for j in range(9):
            x = j * cell_size
            y = i * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="black", width=2 if (i%3==0 and j%3==0) else 1)
            num = board[i][j]
            if num != 0:
                if fixed[i][j]:
                    color = "black"  # số gốc
                else:
                    color = "red" if conflict[i][j] else "green"  # sai: đỏ, đúng: xanh
                canvas.create_text(x + cell_size//2, y + cell_size//2, text=str(num), fill=color, font=("Arial", 16, "bold"))

def initialize_board():
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            used = []
            for i in range(3):
                for j in range(3):
                    val = board[br+i][bc+j]
                    if val != 0:
                        used.append(val)
            fill = [x for x in range(1, 10) if x not in used]
            random.shuffle(fill)
            idx = 0
            for i in range(3):
                for j in range(3):
                    if board[br+i][bc+j] == 0:
                        board[br+i][bc+j] = fill[idx]
                        idx += 1

def compute_conflicts(b):
    count = 0
    for i in range(9):
        row = [0]*10
        col = [0]*10
        for j in range(9):
            row[b[i][j]] += 1
            col[b[j][i]] += 1
        count += sum([x-1 for x in row if x > 1])
        count += sum([x-1 for x in col if x > 1])
    return count

def generate_neighbor():
    while True:
        br = random.randint(0, 2)*3
        bc = random.randint(0, 2)*3
        cells = []
        for i in range(3):
            for j in range(3):
                r, c = br+i, bc+j
                if not fixed[r][c]:
                    cells.append((r, c))
        if len(cells) >= 2:
            a, b = random.sample(cells, 2)
            board[a[0]][a[1]], board[b[0]][b[1]] = board[b[0]][b[1]], board[a[0]][a[1]]
            return a, b

# SA with GUI update
def simulated_annealing_gui():
    T = 1.0
    T_min = 1e-4
    alpha = 0.995
    current = compute_conflicts(board)

    def step():
        nonlocal T, current
        if T < T_min or current == 0:
            draw_board()
            canvas.create_text(225, 460, text=f"Done! Conflict: {current}", font=("Arial", 14), fill="green")
            return

        a, b = generate_neighbor()
        new_conflicts = compute_conflicts(board)
        delta = new_conflicts - current

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new_conflicts
        else:
            board[a[0]][a[1]], board[b[0]][b[1]] = board[b[0]][b[1]], board[a[0]][a[1]]  # Undo

        T *= alpha
        draw_board()
        canvas.after(10, step)  # Delay để xem từng bước

    step()

initialize_board()
draw_board()
canvas.after(1000, simulated_annealing_gui)  # Delay trước khi bắt đầu
root.mainloop()
