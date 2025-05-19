# Import thư viện
import gymnasium as gym                 # Thư viện môi trường học tăng cường
import numpy as np                      # Thư viện tính toán số học (ma trận, vector)
import matplotlib.pyplot as plt         # Thư viện vẽ biểu đồ

# Khởi tạo môi trường LunarLander-v3
env = gym.make("LunarLander-v3")        # Môi trường có 4 hành động rời rạc: trái, phải, bật động cơ chính, không làm gì

# ========================== CÁC THAM SỐ HUẤN LUYỆN ==========================
so_dot = 50         # Tổng số đợt huấn luyện (iteration)
so_mau = 100        # Số dãy hành động được sinh ra trong mỗi đợt
top = 10            # Số lượng dãy hành động có điểm cao nhất sẽ được dùng để cập nhật xác suất
dai = 200           # Mỗi dãy hành động sẽ dài 200 bước (giới hạn số bước chơi)
so_hanh_dong = 4    # Số lượng hành động trong môi trường (Discrete(4))

# ========================== KHỞI TẠO PHÂN PHỐI HÀNH ĐỘNG BAN ĐẦU ==========================
# Mỗi bước trong dãy sẽ có một phân phối xác suất cho 4 hành động
# Ban đầu, xác suất là đều nhau: mỗi hành động có 25%
xac_suat = np.ones((dai, so_hanh_dong)) / so_hanh_dong  # Ma trận (200 x 4)

# Mảng lưu lại phần thưởng tốt nhất ở mỗi đợt huấn luyện để vẽ biểu đồ sau này
log_thuong = []

# ========================== HÀM ĐÁNH GIÁ MỘT DÃY HÀNH ĐỘNG ==========================
def danh_gia(mang_hanh_dong):
    tong = 0                    # Tổng phần thưởng nhận được
    tt, _ = env.reset()         # Đặt lại môi trường và lấy trạng thái ban đầu
    xong = False                # Biến đánh dấu đã kết thúc tập hay chưa
    i = 0                       # Bước hiện tại trong dãy
    while not xong and i < dai:
        a = mang_hanh_dong[i]                      # Lấy hành động tại bước thứ i
        tt, thuong, xong, _, _ = env.step(a)       # Thực hiện hành động, nhận lại trạng thái, phần thưởng, cờ kết thúc
        tong += thuong                             # Cộng dồn phần thưởng
        i += 1
    return tong              # Trả về tổng phần thưởng của dãy hành động này

# ========================== VÒNG LẶP HUẤN LUYỆN ==========================
for dot in range(so_dot):
    ds_mau = []          # Danh sách các dãy hành động được sinh ra
    ds_thuong = []       # Danh sách phần thưởng tương ứng

    # ------ Tạo ngẫu nhiên so_mau dãy hành động ------
    for _ in range(so_mau):
        hanh_dong = [np.random.choice(so_hanh_dong, p=xac_suat[i]) for i in range(dai)]
        # Mỗi bước i trong dãy sẽ chọn hành động theo xác suất tại bước đó
        ds_mau.append(hanh_dong)                   # Thêm dãy hành động vào danh sách
        ds_thuong.append(danh_gia(hanh_dong))      # Tính và lưu phần thưởng tương ứng

    ds_thuong = np.array(ds_thuong)                # Ép về dạng mảng numpy để dễ xử lý
    log_thuong.append(np.max(ds_thuong))           # Lưu phần thưởng cao nhất của đợt này

    # ------ Lấy ra top K dãy hành động tốt nhất ------
    chi_so_top = np.argsort(ds_thuong)[-top:]      # Sắp xếp chỉ số theo phần thưởng, lấy top cuối
    elite = np.array(ds_mau)[chi_so_top]           # Lấy các dãy hành động tương ứng

    # ------ Cập nhật xác suất hành động tại mỗi bước theo elite ------
    for i in range(dai):
        dem = np.zeros(so_hanh_dong)               # Khởi tạo vector đếm số lần mỗi hành động xuất hiện tại bước i
        for mau in elite:
            dem[mau[i]] += 1                       # Đếm số lần hành động j xuất hiện tại bước i
        if np.sum(dem) > 0:
            xac_suat[i] = dem / np.sum(dem)        # Cập nhật xác suất bằng tần suất xuất hiện (chuẩn hóa)

    # ------ In thông tin huấn luyện ------
    print(f"Đợt {dot+1}/{so_dot} | Thưởng cao nhất: {np.max(ds_thuong):.1f} | Trung bình: {np.mean(ds_thuong):.1f}")

    # ------ Kiểm tra nếu đã đạt mục tiêu thành công ------
    if np.max(ds_thuong) >= 200:
        print("Hạ cánh thành công!")
        break

# ========================== ĐÓNG MÔI TRƯỜNG ==========================
env.close()

# ========================== VẼ BIỂU ĐỒ ==========================
# Trục hoành: số đợt huấn luyện
# Trục tung: phần thưởng tốt nhất
plt.plot(log_thuong)
plt.title("Tiến trình huấn luyện")
plt.xlabel("Đợt")
plt.ylabel("Thưởng cao nhất")
plt.grid(True)
plt.show()
