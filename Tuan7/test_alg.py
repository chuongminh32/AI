import math

"""A* (A-star) là thuật toán tìm đường tối ưu từ điểm bắt đầu đến đích. Nó kết hợp:

g(n): chi phí từ điểm bắt đầu đến nút hiện tại n.

h(n): ước lượng chi phí từ n đến đích (heuristic).

f(n) = g(n) + h(n): tổng chi phí ước lượng.
"""
# Heuristic euclid 
def h(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Hàm tìm ô có f nhỏ nhất trong danh sách tap_mo
def tim_f_min(tap_mo, gia_tri_f):
    min_i = 0
    for i in range(1, len(tap_mo)):
        if gia_tri_f[tap_mo[i]] < gia_tri_f[tap_mo[min_i]]:
            min_i = i
    return tap_mo[min_i] # toạ độ h(min) 

# Dữ liệu đầu vào
ban_do = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 0], 
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], 
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
]
bat_dau = (0, 0)
dich = (8, 9)

# Khởi tạo
so_hang = len(ban_do)
so_cot = len(ban_do[0])
tap_mo = [bat_dau] # [(i,j),..]
duong_di = {}
gia_tri_g = {bat_dau: 0}
gia_tri_f = {bat_dau: h(bat_dau, dich)} # { (i,j): f = h(i,j) + g(i,j),..}
huong_di_chuyen = [(0, 1), (1, 0), (0, -1), (-1, 0)]

dem = 0
tim_thay = False
while len(tap_mo) > 0:

    hien_tai = tim_f_min(tap_mo, gia_tri_f)

    if hien_tai == dich:
        tim_thay = True
        break

    tap_mo.remove(hien_tai)

    if dem < 10:
        print(f"\n* Vòng {dem + 1}")
        print("Node hiện tại:", hien_tai)
        print(f"Tap mo da xoa node h min: {hien_tai} khoi ds")
        print("tap_mo hiện tại:", tap_mo)

        print(f"    g = {gia_tri_g[hien_tai]:.2f}")
        print(f"    h = {h(hien_tai, dich):.2f}")
        print(f"    f = {gia_tri_f[hien_tai]:.2f}")


    print(" Cac gia tri g,h,f node hang xom:")

    for huong in huong_di_chuyen:
        hang = hien_tai[0] + huong[0]
        cot = hien_tai[1] + huong[1]

        # check còn trong grid và ô hợp lệ 
        if 0 <= hang < so_hang and 0 <= cot < so_cot and ban_do[hang][cot] == 0:
            
            hang_xom = (hang, cot)
            g_hx = gia_tri_g[hien_tai] + 1 # g giả định nếu đi qua ô hàng xóm 

            # chỉ cập nhật đường đi nếu node chưa xét hoặc đã đi qua và có chi phí thấp hơn 
            if hang_xom not in gia_tri_g or g_hx < gia_tri_g[hang_xom]:
                duong_di[hang_xom] = hien_tai # lưu để truy vết về sau nếu tìm thấy đích duong_di[con] = cha 
                gia_tri_g[hang_xom] = g_hx
                gia_tri_f[hang_xom] = g_hx + h(hang_xom, dich)

                if hang_xom not in tap_mo:
                    tap_mo.append(hang_xom)
                    print(f"tap mo dang them node {hang_xom}")
                
                if dem < 10:
                    print(f"  Xét hàng xóm: {hang_xom}")
                    print(f"    g = {gia_tri_g[hang_xom]:.2f}")
                    print(f"    h = {h(hang_xom, dich):.2f}")
                    print(f"    f = {gia_tri_f[hang_xom]:.2f}")
    print(f"duong di hien tai: {duong_di} = node con : node cha")
    print(f"Tap mo hien tai: {tap_mo}")
    dem += 1
# truy vết từ điểm đích -> tìm trong duong_di (node cha) -> đường đi 
if tim_thay:
    duong_di_toi_dich = []
    nut = dich
    while nut in duong_di: # neu node cha duoc tim thay -> tiep tuc truy vet node cha cua cha 
        duong_di_toi_dich.append(nut)
        nut = duong_di[nut] # lay node cha 
    duong_di_toi_dich.append(bat_dau)
    duong_di_toi_dich.reverse()
    print("Đường đi tìm được:")
    print(duong_di_toi_dich)
else:
    print("Không tìm thấy đường đi.")
