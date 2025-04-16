import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Cài đặt ---
ban_do = [
    [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0],[0,1,0,0,0,1,1,1,1,0],
    [0,1,0,0,0,1,0,0,0,0],[0,1,1,1,1,1,0,0,0,0],[0,0,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,0,0]
]
so_hang, so_cot = len(ban_do), len(ban_do[0])
huong = [(0,1),(1,0),(0,-1),(-1,0)]

# --- Nhập heuristic ---
while True:
    heuristic_mode = input("Chọn heuristic (euclid / manhattan): ").strip().lower()
    if heuristic_mode in ('manhattan', 'euclid'):
        break
    print("Heuristic không hợp lệ. Nhập lại.")

def heuristic(a, b):
    if heuristic_mode == 'manhattan':
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    return math.hypot(a[0] - b[0], a[1] - b[1])

# --- Nhập điểm bắt đầu/kết thúc ---
def nhap_diem(mes):
    while True:
        try:
            x, y = map(int, input(f"{mes} (hàng cột): ").split())
            if 0 <= x < so_hang and 0 <= y < so_cot and ban_do[x][y] == 0:
                return (x, y)
            else:
                print("Tọa độ không hợp lệ hoặc trùng tường.")
        except:
            print("Lỗi định dạng. Nhập lại.")

bat_dau = nhap_diem("Nhập điểm bắt đầu")
dich = nhap_diem("Nhập điểm kết thúc")

# --- Vẽ bản đồ ---
plt.ion()
fig, ax = plt.subplots()

def ve(luoi, duong=None, current=None):
    # Xóa toàn bộ nội dung cũ trên trục vẽ
    ax.clear()

    # Cài đặt lưới kẻ ô: tạo các đường grid dọc và ngang
    ax.set_xticks(range(len(luoi[0]) + 1))  # Đánh dấu theo cột
    ax.set_yticks(range(len(luoi) + 1))     # Đánh dấu theo hàng
    ax.grid(True)

    # Cài đặt giới hạn vùng vẽ theo kích thước lưới
    ax.set_xlim(0, len(luoi[0]))
    ax.set_ylim(0, len(luoi))

    # Đảo ngược trục Y để ô (0,0) nằm trên cùng bên trái (giống ma trận)
    ax.invert_yaxis()

    # Vẽ các ô chướng ngại (giá trị 1) màu đen
    for i in range(len(luoi)):
        for j in range(len(luoi[0])):
            if luoi[i][j] == 1:
                ax.add_patch(patches.Rectangle((j, i), 1, 1, color='black'))

    # Vẽ đường đi (nếu có) với màu cyan (xanh nhạt)
    if duong:
        for (i, j) in duong:
            ax.add_patch(patches.Rectangle((j, i), 1, 1, color='cyan'))

    # Vẽ vị trí hiện tại đang xét (nếu có) với màu đỏ
    if current:
        i, j = current
        ax.add_patch(patches.Rectangle((j, i), 1, 1, color='red'))

    # Vẽ ô bắt đầu màu xanh lá cây
    ax.add_patch(patches.Rectangle((bat_dau[1], bat_dau[0]), 1, 1, color='green'))

    # Vẽ ô đích màu xanh dương
    ax.add_patch(patches.Rectangle((dich[1], dich[0]), 1, 1, color='blue'))

    # Hiển thị cập nhật mới
    plt.draw()
    plt.pause(0.2)  # Tạm dừng 0.2 giây để dễ quan sát quá trình

# --- A* ---
tap_mo = [bat_dau]
duong_di = {}
gia_tri_g = {bat_dau: 0}
gia_tri_f = {bat_dau: heuristic(bat_dau, dich)}

buoc = 0
while tap_mo:
    hien_tai = min(tap_mo, key=lambda x: gia_tri_f[x])
    print(f"\n--- Bước {buoc} ---")
    print(f"Current node: {hien_tai} | g={gia_tri_g[hien_tai]} | h={heuristic(hien_tai, dich):.2f} | f={gia_tri_f[hien_tai]:.2f}")
    buoc += 1

    if hien_tai == dich:
        print("Đã tìm thấy điểm đích.")
        break

    tap_mo.remove(hien_tai)
    for dx, dy in huong:
        i, j = hien_tai[0]+dx, hien_tai[1]+dy
        if 0 <= i < so_hang and 0 <= j < so_cot and ban_do[i][j] == 0:
            hx = (i, j) # tọa độ hx = hàng xóm điểm lân cận 
            g = gia_tri_g[hien_tai] + 1
            h = heuristic(hx, dich)
            f = g + h
            # nếu chưa đi qua hoặc chi phí g điểm đã xét không tối ưu bằng điểm đang xét -> cập nhật đường đi 
            if hx not in gia_tri_g or g < gia_tri_g[hx]:
                duong_di[hx] = hien_tai
                gia_tri_g[hx] = g
                gia_tri_f[hx] = f
                if hx not in tap_mo:
                    tap_mo.append(hx)
                print(f"  Xét: {hx} | g={g} | h={h:.2f} | f={f:.2f}")
    ve(ban_do, duong_di.keys(), hien_tai)

# --- Truy vết ---
duong = []
nut = dich
while nut in duong_di:
    duong.append(nut)
    nut = duong_di[nut]
duong.append(bat_dau)
duong.reverse()

print("\nĐường đi từ bắt đầu đến đích:")
for d in duong:
    print(d)

ve(ban_do, duong)
plt.ioff()
plt.show()
