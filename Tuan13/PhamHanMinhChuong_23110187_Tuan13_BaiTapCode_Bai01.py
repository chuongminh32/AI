import gymnasium as gym
import time

# Cấu hình cho thử nghiệm
cac_moi_truong = ["CartPole-v1", "MountainCar-v0", "Pendulum-v1"]
so_luong_episode = 2  # Số lượng episode cho mỗi môi trường
so_buoc_toi_da = 5  # Số bước tối đa trong mỗi episode

# Hàm in thông tin để tránh lặp lại mã
# Điểm tối ưu: Thay vì lặp lại mã in thông tin ở nhiều nơi, ta sử dụng một hàm duy nhất để in
def print_step_info(buoc_hien_tai, hanh_dong, quan_sat_moi, phan_thuong, ket_thuc, bi_cat, thong_tin_them):
    print(f"Bước {buoc_hien_tai + 1}: Hành động = {hanh_dong}")
    print(f"  Quan sát mới: {quan_sat_moi}")
    print(f"  Phần thưởng: {phan_thuong}")
    print(f"  Đã kết thúc: {ket_thuc}")
    print(f"  Bị cắt: {bi_cat}")
    print(f"  Thông tin: {thong_tin_them}")

# Lặp qua các môi trường
for ten_moi_truong in cac_moi_truong:
    print(f"\n--- Thử nghiệm môi trường: {ten_moi_truong} ---")
    
    try:
        # Tạo môi trường - Chỉ gọi `gym.make()` một lần cho mỗi môi trường
        # Điểm tối ưu: Trước đây có thể phải gọi lại `gym.make()` nhiều lần, nhưng giờ chỉ gọi 1 lần cho mỗi môi trường.
        moi_truong = gym.make(ten_moi_truong)
        
        # Lấy không gian hành động của môi trường - Đây là không gian mà agent có thể chọn hành động
        khong_gian_hanh_dong = moi_truong.action_space
        print(f"Không gian hành động: {khong_gian_hanh_dong}")

        # Thử nghiệm trên mỗi môi trường với nhiều episode
        for episode_hien_tai in range(so_luong_episode):
            print(f"\nBắt đầu episode {episode_hien_tai + 1}")
            
            # Reset môi trường cho mỗi episode - Chỉ gọi lại `reset()` khi bắt đầu episode
            # Điểm tối ưu: Trước đây có thể phải gọi `reset()` nhiều lần, bây giờ chỉ gọi một lần trong mỗi episode.
            quan_sat, _ = moi_truong.reset()

            # Lặp qua các bước trong mỗi episode
            for buoc_hien_tai in range(so_buoc_toi_da):
                # Chọn hành động ngẫu nhiên từ không gian hành động
                hanh_dong_ngau_nhien = khong_gian_hanh_dong.sample()
                
                # Thực hiện hành động và nhận thông tin về bước tiếp theo
                quan_sat_moi, phan_thuong, ket_thuc, bi_cat, thong_tin_them = moi_truong.step(hanh_dong_ngau_nhien)
                
                # In thông tin về bước, sử dụng hàm `print_step_info` để giảm sự lặp lại mã
                # Điểm tối ưu: Dùng hàm `print_step_info` để giảm bớt việc lặp lại mã trong vòng lặp
                print_step_info(buoc_hien_tai, hanh_dong_ngau_nhien, quan_sat_moi, phan_thuong, ket_thuc, bi_cat, thong_tin_them)

                # Cập nhật trạng thái cho bước tiếp theo
                quan_sat = quan_sat_moi

                # Kiểm tra nếu episode đã kết thúc
                # Nếu kết thúc hoặc bị cắt (timed-out), dừng vòng lặp
                if ket_thuc or bi_cat:
                    print(f"Episode {episode_hien_tai + 1} kết thúc sau {buoc_hien_tai + 1} bước.")
                    break

            # Thêm độ trễ để quan sát môi trường rõ ràng hơn
            # Điểm tối ưu: Độ trễ giúp dễ dàng quan sát kết quả trong quá trình chạy thử
            time.sleep(1)

        # Đóng môi trường sau khi thử nghiệm xong
        # Điểm tối ưu: Sau khi thử nghiệm xong, ta giải phóng tài nguyên môi trường bằng cách gọi `close()`
        moi_truong.close()

    except Exception as e:
        # Xử lý lỗi nếu có khi tải hoặc chạy môi trường
        print(f"Lỗi khi tải hoặc chạy môi trường {ten_moi_truong}: {e}")

# Thông báo hoàn thành
# Điểm tối ưu: Thông báo khi hoàn thành toàn bộ thử nghiệm để dễ dàng theo dõi.
print("\n--- Hoàn thành thử nghiệm ---")
