import tkinter as tk

N = 15  # Số quân hậu

cell_size = 30
canvas_size = N * cell_size

idx = 0
his = [] # list lưu lịch sử trạng thái 
chay_tu_dong = False


# hàm kiểm tra vị trí đang xét có xd ? 
def is_safe(state, col, row):
    for c in range(col):
        if state[c] == row or abs(state[c] - row) == abs(c - col):
            return False
    return True

"""state: là danh sách độ dài N, trong đó state[i] là vị trí dòng của quân hậu ở cột i. Nếu state[i] = -1 thì chưa đặt quân hậu nào ở cột đó.

col: cột hiện tại đang xét để đặt quân hậu.

history: danh sách các bước đi, gồm các trạng thái bàn cờ và mô tả hành động để hiển thị lại từng bước"""


def and_or_search(state, col, history):
    # Hoàn tất khi đã đặt hết quân hậu
    if col == N:
        history.append((state[:], "Hoàn tất"))
        return [state[:]]  # Trả về danh sách chứa 1 lời giải

    results = []  # Lưu các lời giải
    for row in range(N):
        state[col] = row  # Đặt hậu tại vị trí (col, row)

        # Kiểm tra tính hợp lệ
        if is_safe(state, col, row):
            history.append((state[:], f"Đặt hậu tại cột {col}, dòng {row} -> đặt hậu thành công > đặt hậu cho cột kế tiếp"))
            res = and_or_search(state, col + 1, history)  # Tiếp tục kiểm tra cột tiếp theo
            results.extend(res)  # Thêm các lời giải vào kết quả
            if res: 
                return results

        else:
            history.append((state[:], f"Thử sai tại cột {col}, dòng {row} > gỡ hậu thử dòng khác!"))

    state[col] = -1  # Gỡ hậu sau khi thử xong
    return results  # Trả về danh sách các lời giải tìm được


def cap_nhat(idx):
    bang, action = his[idx]
    conflict = tinh_xd(bang)
    ve_ban_co(canvas, bang)

    # In conflict chỉ ở đây
    print(f"[Bước {idx + 1}] {action} | Conflict: {conflict}")


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
            # vẽ tọa độ góc trên trái 
            x1 = j * cell_size
            y1 = i * cell_size
            # dưới phải 
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            color = "#EEE" if (i + j) % 2 == 0 else "#555"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    for col, row in enumerate(board):
        if row != -1:
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            canvas.create_text(x, y, text="♛", font=("Arial", 16), fill="red")


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
    if not chay_tu_dong:
        chay_tu_dong = True
        auto_button.config(text="Stop")
        auto_step()
    else:
        chay_tu_dong = False
        auto_button.config(text="Auto")


def And_Or_Run():
    global his, log, idx, chay_tu_dong

    his = []
    idx = 0
    chay_tu_dong = False

    # trạng thai bd 
    empty_state = [-1] * N
    temp_history = []

    print("\n== Bắt đầu giải bài toán 15 quân hậu với AND-OR Search ==\n")
    giai_phap = and_or_search(empty_state, 0, temp_history)

    if giai_phap:
        his = temp_history
        print("\n==> Tìm thấy lời giải:")
        print(giai_phap[0])
        cap_nhat(0)
    else:
        print("Không tìm thấy lời giải.")


# === GUI ===
root = tk.Tk()
root.title("AND-OR Search - 15 Queens")

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
