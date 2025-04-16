import tkinter as tk

N = 6 
cell_size = 60
canvas_size = N * cell_size

idx = 0
his = []
chay_tu_dong = False
all_solutions = []

def is_safe(state, col, row):
    for c in range(col):
        if state[c] == row or abs(state[c] - row) == abs(c - col):
            return False
    return True

def and_or_search(state, col, history, solutions):
    if col == N:
        history.append((state[:], f"Tìm thấy lời giải hoàn chỉnh{state[:]}"))
        solutions.append(state[:])
        return

    for row in range(N):
        state[col] = row
        if is_safe(state, col, row):
            history.append((state[:], f"Đặt hậu tại cột {col}, dòng {row}"))
            and_or_search(state, col + 1, history, solutions)
        else:
            history.append((state[:], f"Thử sai tại cột {col}, dòng {row}"))
    state[col] = -1

def tinh_xd(board):
    cnt = 0
    for i in range(N):
        for j in range(i + 1, N):
            if board[i] == -1 or board[j] == -1:
                continue
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                cnt += 1
    return cnt

def ve_ban_co(canvas, board):
    canvas.delete("all")
    for i in range(N):
        for j in range(N):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = "#EEE" if (i + j) % 2 == 0 else "#555"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    for col, row in enumerate(board):
        if row != -1:
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            canvas.create_text(x, y, text="♛", font=("Arial", 24), fill="red")

def cap_nhat(idx):
    bang, action = his[idx]
    conflict = tinh_xd(bang)
    ve_ban_co(canvas, bang)
    print(f"[Bước {idx + 1}] {action} | Conflict: {conflict}")

def buoc_tiep_theo():
    global idx
    if idx < len(his) - 1:
        idx += 1
        cap_nhat(idx)

def buoc_truoc_do():
    global idx
    if idx > 0:
        idx -= 1
        cap_nhat(idx)

def auto_step():
    global idx, chay_tu_dong
    if idx < len(his) - 1 and chay_tu_dong:
        idx += 1
        cap_nhat(idx)
        canvas.after(300, auto_step)
    else:
        auto_button.config(text="Auto")
        chay_tu_dong = False

def auto_run():
    global chay_tu_dong
    chay_tu_dong = not chay_tu_dong
    auto_button.config(text="Stop" if chay_tu_dong else "Auto")
    if chay_tu_dong:
        auto_step()

def And_Or_Run():
    global idx, his, all_solutions, chay_tu_dong
    print("\n== Bắt đầu giải bài toán 6 quân hậu bằng AND-OR Search ==\n")

    idx = 0
    chay_tu_dong = False
    his.clear()
    all_solutions.clear()

    state = [-1] * N
    and_or_search(state, 0, his, all_solutions)

    if all_solutions:
        print(f"\nTổng số lời giải tìm được: {len(all_solutions)}\n")
        for i, sol in enumerate(all_solutions, 1):
            print(f"Lời giải {i}: {sol}")
        cap_nhat(0)
    else:
        print("Không tìm thấy lời giải.")

# === GUI ===
root = tk.Tk()
root.title("AND-OR Search - 6 Queens")

canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
canvas.grid(row=0, column=0, columnspan=4)

start_button = tk.Button(root, text="Chạy AND-OR", command=And_Or_Run)
start_button.grid(row=2, column=0, pady=5)

prev_button = tk.Button(root, text="<<", command=buoc_truoc_do)
prev_button.grid(row=2, column=1)

auto_button = tk.Button(root, text="Auto", command=auto_run)
auto_button.grid(row=2, column=2)

next_button = tk.Button(root, text=">>", command=buoc_tiep_theo)
next_button.grid(row=2, column=3)

root.mainloop()
