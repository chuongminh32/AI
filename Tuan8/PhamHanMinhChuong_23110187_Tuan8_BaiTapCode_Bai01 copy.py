import random
import math
import tkinter as tk
from PIL import Image, ImageTk


# Khai báo các biến toàn cục
lichSu = []
arrP = []
arrT = []
vongHienTai = 0
T = 100
delta = 0
P = 1.0

# Tính số xung đột giữa các quân hậu
def tinhXungDot(bang):
    cnt = 0
    n = len(bang)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if bang[i] == bang[j] or abs(bang[i] - bang[j]) == abs(i - j):
                cnt += 1
    return cnt

# # Di chuyển ngẫu nhiên một quân hậu
def diChuyenNgauNhien(bang):
    bangMoi = bang[:]
    cot = random.randint(0, 7)
    hangMoi = random.randint(0, 7)
    bangMoi[cot] = hangMoi
    return bangMoi, cot, hangMoi

# def diChuyenNgauNhien(bang):
#     bangMoi = bang[:]  # Sao chép danh sách
#     cot = random.randint(0, 7)  # Chọn cột ngẫu nhiên trong 15 cột
#     hangHienTai = bangMoi[cot]  # Lấy hàng hiện tại của quân hậu tại cột này
    
    # Chọn hàng mới KHÁC hàng hiện tại
    # hangMoi = random.choice([h for h in range(7) if h != hangHienTai])

    # bangMoi[cot] = hangMoi  # Cập nhật vị trí mới
    # return bangMoi, cot, hangMoi

# Hàm vẽ bàn cờ
def veBanCo(canvas, bang):
    canvas.delete("all")
    size = 50  # Kích thước của mỗi ô bàn cờ
    
    # Tạo các ô bàn cờ
    for i in range(8):
        for j in range(8):
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=color)
    # vẽ chấm tròn đại diện quân hậu 
    for j in range(8):
        # tọa độ (trên,trái) (dưới, phải)
        canvas.create_oval(j * size + 10, bang[j] * size + 10, (j + 1) * size - 10, (bang[j] + 1) * size - 10, fill="red")
    canvas.update()


# Cập nhật trạng thái bàn cờ
def capNhatBanCo(canvas, labelVong, labelMang):
    if 0 <= vongHienTai < len(lichSu):
        veBanCo(canvas, lichSu[vongHienTai])
        labelVong.config(text=f"Vòng lặp: {vongHienTai + 1}/{len(lichSu)}")
        labelMang.config(text=f"Vị trí quân hậu: {lichSu[vongHienTai]}")

        p_value = arrP[vongHienTai] if 0 <= vongHienTai < len(arrP) else "Chưa có"
        t_value = arrT[vongHienTai] if 0 <= vongHienTai < len(arrP) else "Chưa có"

        # Hiển thị trên một hàng
        labelMang.config(text=f"Vị trí quân hậu: {lichSu[vongHienTai]}, T: {t_value}, P: {p_value}")

# Chức năng xử lý nút Next
def nextStep(canvas, labelVong, labelMang):
    global vongHienTai
    if vongHienTai < len(lichSu) - 1:
        vongHienTai += 1
        capNhatBanCo(canvas, labelVong, labelMang)

# Chức năng xử lý nút Back
def backStep(canvas, labelVong, labelMang):
    global vongHienTai
    if vongHienTai > 0:
        vongHienTai -= 1
        capNhatBanCo(canvas, labelVong, labelMang)

# Hàm thuật toán Simulated Annealing
def simulatedAnnealing(root, canvas, labelVong, labelMang, maxVong=5, T_start=100, TMin=0.01, alpha=0.95):
    global lichSu, vongHienTai, T, delta, P
    lichSu = []  # Xóa lịch sử cũ để không bị ghi đè**
    vongHienTai = 0
    T = T_start
    bangHienTai = [random.randint(0,7) for _ in range(8)]
    xungDotHienTai = tinhXungDot(bangHienTai)
    lichSu.append(bangHienTai[:])
    print(f"Vòng 1: {bangHienTai}")
    
    # Chạy 5 vòng lặp đầu tiên
    for i in range(1, maxVong + 1):

        # giow han nhiet do T ( neu nho hon -> ct xsP sai)
        if T < TMin:
            break
        bangMoi, cot, hangMoi = diChuyenNgauNhien(bangHienTai)
        xungDotMoi = tinhXungDot(bangMoi)
        delta = xungDotMoi - xungDotHienTai
        
        # Tính xác suất P
        P = math.exp(-delta / T) if delta > 0 else 1
        if delta < 0 or random.uniform(0, 1) < P:
            hangCu = bangHienTai[cot] # lay hang cu 
            bangHienTai = bangMoi
            xungDotHienTai = xungDotMoi
            lichSu.append(bangHienTai[:])
            arrP.append(P)
            arrT.append(T)
            print(f"Vòng {i+1}: {bangHienTai}, T: {T}, Vị trí hoán đổi: Cột {cot+1} từ hàng: {hangCu} thành {hangMoi} , P: {P}, Số xung đột delta: {delta}")
    

        # Giảm nhiệt độ
        T *= alpha
    
    vongHienTai = 0
    capNhatBanCo(canvas, labelVong, labelMang)
    print("Trạng thái cuối:", bangHienTai, "Xung đột hiện tại :", xungDotHienTai)


# Khởi tạo giao diện Tkinter
def main():
    root = tk.Tk()
    root.title("Mô phỏng Simulated Annealing - 8 Queens")
    
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()
    
    labelVong = tk.Label(root, text="Vòng lặp: 0/0")
    labelVong.pack()
    
    labelMang = tk.Label(root, text="Vị trí quân hậu: ")
    labelMang.pack()

    tk.Button(root, text="Chạy Simulated Annealing", command=lambda: simulatedAnnealing(root, canvas, labelVong, labelMang)).pack()
    tk.Button(root, text="Back", command=lambda: backStep(canvas, labelVong, labelMang)).pack(side=tk.LEFT)
    tk.Button(root, text="Next", command=lambda: nextStep(canvas, labelVong, labelMang)).pack(side=tk.RIGHT)
    
    root.mainloop()

if __name__ == "__main__":
    main()
