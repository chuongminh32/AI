import random
import math
import tkinter as tk
from tkinter import ttk
import time  # Để sử dụng sleep trong Auto
"""
>> Nguyên lý hoạt động:
Bắt đầu từ một lời giải ban đầu.
Lặp lại:
Sinh lời giải "lân cận".
Tính độ thay đổi chất lượng (ΔE).
Nếu tốt hơn (ΔE < 0): chấp nhận lời giải mới.
Nếu tệ hơn: chấp nhận với xác suất P = e^(-ΔE / T).
Giảm nhiệt độ T theo thời gian (ví dụ: T *= 0.99).
Dừng khi T rất nhỏ hoặc tìm được lời giải tốt.

>>  Ý tưởng cốt lõi:
Không tham lam chọn lời giải tốt hơn.
Cho phép đi đến lời giải xấu hơn để thoát khỏi kẹt cục bộ.
Xác suất chấp nhận lời giải xấu giảm dần theo thời gian (nhiệt độ).
"""
# Kích thước bàn cờ & số quân hậu 
N = 15
b_size = 40 
his = []
log = []

def tinh_xd(b):
    cnt = 0
    for i in range(N - 1):
        for j in range(i + 1, N):
            if b[i] == b[j] or abs(b[i] - b[j]) == abs(i - j):
                cnt += 1
    return cnt

def hoan_doi_random(bang):
    b = bang[:]  # Sao chép bàn cờ

     # Chọn một cột ngẫu nhiên
    c = random.randint(0, N-1) 
    best_r = b[c]  # Vị trí hiện tại của quân hậu
    xd = tinh_xd(b)  # Số xung đột hiện tại

    f = False   # cờ đánh dấu đã không tìm được trạng thái tốt hơn (số xung đột >= trước đó) -> random 

    # tìm vị trí (val) có ít xung đột nhất 
    for r in range(N):
        if r != b[c]:  
            temp_b = b[:]  # Tạo bản sao tạm thời để thử di chuyển
            temp_b[c] = r # di chuyển hậu 
            new_xd = tinh_xd(temp_b)
            if new_xd < xd:  # Tìm vị trí tốt nhất để di chuyển
                f = True
                best_r = r
                xd = new_xd
    
    # random dòng khác để tránh kẹt 
    if not f:
        best_r = random.choice([r for r in range(N) if b[c] != r])

    b[c] = best_r  # Cập nhật bàn cờ với vị trí tối ưu
    return b, c, r, best_r


#  Hàm giảm nhiệt độ (schedule function)
def schedule_function(t):
    return max(0.01, 100 * (0.95 ** t))

#____________________SA________________________
def SA():
    global his, log, idx, chay_tu_dong

    b = [random.randint(0, N - 1) for _ in range(N)]
    T = 1000 
    i = 0
    his = []
    log = []
    chay_tu_dong = True
    idx = 0

    print("Bắt đầu giải bài toán với trạng thái khởi tạo:")
    print("  Vị trí quân hậu:", b)
    print("  Xung đột ban đầu:", tinh_xd(b))
    print("="*50)

    def run_step():

        nonlocal b, T, i
        if tinh_xd(b) == 0 :
            print("Đã tìm được lời giải hợp lệ:")
            print("  Trạng thái cuối:", b)
            print("  Xung đột:", tinh_xd(b))
            auto_button.config(text="Auto")
            return
        elif not chay_tu_dong:
            print("Chưa tìm ra rời giải:")
            print("  Trạng thái cuối:", b)
            print("  Xung đột:", tinh_xd(b))
            auto_button.config(text="Auto")
            return


        xd_truoc = tinh_xd(b)
        new_b, c, r, best_r = hoan_doi_random(b)
        xd_hienTai = tinh_xd(new_b)

        delta = xd_hienTai - xd_truoc

        # chỉ tính xs nếu trạng thái hiện tại xấu hơn ngược lại -> luôn chấp nhận 
        P = math.exp(-delta / T) if delta > 0 else 1
      
        if delta < 0 or random.uniform(0, 1) < P:
            b = new_b
            status = "=> Chấp nhận"
        else:
            status = "=> Từ chối"

        his.append(b[:])
        log.append((T, P, delta, xd_hienTai, xd_truoc))

        print(f"Bước {i}:")
        print(f"Đã di chuyển quân hậu tại cột {c} từ dòng {r} -> {best_r}")
        print(f"  Trạng thái mới: {new_b}")
        print(f"  Xung đột: {xd_hienTai} (trước: {xd_truoc})")
        print(f"  Δ = {delta:.2f}, P = {P:.4f}, T = {T:.2f} {status}")
        print("-" * 50)

        idx = len(his) - 1
        update_info(idx)

        T = schedule_function(i)
        i += 1
        root.after(100, run_step)

    run_step()

#__________________________________________________________GIAO DIEN_______________________________________________________________________

# Hàm vẽ đường nối giữa các quân hậu xung đột
def ve_xd(canvas, b, size, offset):
    for i in range(N):
        for j in range(i + 1, N):
            if b[i] == b[j] or abs(b[i] - b[j]) == abs(i - j):
                # Vị trí trung tâm của quân hậu i
                x1 = i * size + offset + size // 2
                y1 = b[i] * size + offset + size // 2
                # Vị trí trung tâm của quân hậu j
                x2 = j * size + offset + size // 2
                y2 = b[j] * size + offset + size // 2
                canvas.create_line(x1, y1, x2, y2, fill="red", width=2)


#_______________________________________________________
def ve_ban_co(canvas, b):
    canvas.delete("all")
    size = b_size
    offset = 22 

    # Resize canvas nếu cần
    canvas.config(width=N * size + offset * 2, height=N * size + offset * 2)

    # Vẽ các ô bàn cờ
    for i in range(N):
        for j in range(N):
            x1 = j * size + offset
            y1 = i * size + offset
            x2 = x1 + size
            y2 = y1 + size
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    # Vẽ chỉ số hàng
    for i in range(N):
        canvas.create_text(5, i * size + offset + size // 2, text=str(i), anchor="w", font=("Arial", 12))

    # Vẽ chỉ số cột
    for j in range(N):
        canvas.create_text(j * size + offset + size // 2, 5, text=str(j), anchor="n", font=("Arial", 12))

    # Vẽ quân hậu
    for col, row in enumerate(b):
        x = col * size + offset + size // 2
        y = row * size + offset + size // 2
        canvas.create_text(x, y, text="♛", font=("Arial", 20), fill="black")

    # Vẽ xung đột
    ve_xd(canvas, b, size, offset)

    canvas.update()

# Chạy giao diện
root = tk.Tk()
root.title("Simulated Annealing - 15 Queens")

# Tạo frame để chứa bàn cờ và các nút
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)  # Tạo khoảng cách giữa frame và các cạnh cửa sổ

# Thêm tiêu đề
title_label = tk.Label(frame, text="Simulated Annealing - 15 Queens", font=("Arial", 18))
title_label.grid(row=0, column=0, columnspan=3, pady=5)  # Tiêu đề

# Tạo canvas để vẽ bàn cờ
canvas = tk.Canvas(frame, width=N*b_size, height=N*b_size)
canvas.grid(row=1, column=0, columnspan=3)

idx = 0
chay_tu_dong = False  # Biến đánh dấu trạng thái tự động

# Thêm label để hiển thị thông tin T, P, delta và xung đột
info_label = tk.Label(frame, text="", font=("Arial", 16 ), width=55, anchor='w')
info_label.grid(row=2, column=0, columnspan=3, pady=5, padx=(20, 0))

# Hiển thị từng bước
def next_step():
    global idx
    if idx < len(his) - 1:
        idx += 1
        ve_ban_co(canvas, his[idx])
        update_info(idx)
        print(f"Bước {idx}: {his[idx]}")  # In ra trạng thái

def prev_step():
    global idx
    if idx > 0:
        idx -= 1
        ve_ban_co(canvas, his[idx])
        update_info(idx)
        print(f"Bước {idx}: {his[idx]}")  # In ra trạng thá

def auto_run():
    global chay_tu_dong
    if not chay_tu_dong:
        auto_button.config(text="Stop")
        SA()
    else:
        chay_tu_dong = False
        auto_button.config(text="Auto")

# Cập nhật thông tin T, P, delta và số xung đột vào label
def update_info(idx):
    T, P, d, xd_hienTai, xd_truocDo = log[idx]
    info_label.config(
        text=f"T: {T:.2f} | P: {P:.4f} | Δ: {d} | Conflict Now: {xd_hienTai} | Conflict Before:{xd_truocDo}"
    )
    ve_ban_co(canvas, his[idx])


# Tạo nút điều khiển
ttk.Button(frame, text="Back", command=prev_step).grid(row=3, column=0, padx=10, pady=10)
auto_button = ttk.Button(frame, text="Auto", command=auto_run)
auto_button.grid(row=3, column=1, padx=10, pady=10)
ttk.Button(frame, text="Next", command=next_step).grid(row=3, column=2, padx=10, pady=10)

# Bắt đầu hiển thị
if his:
    ve_ban_co(canvas, his[0])
    update_info(0)
else:
    info_label.config(text="Chưa có dữ liệu. Nhấn Auto để bắt đầu.")

root.mainloop()
