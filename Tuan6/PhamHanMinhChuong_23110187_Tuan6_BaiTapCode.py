from collections import deque
import heapq


# Ánh xạ số → tên thành phố
ten_thanh_pho = {
    1: "TP. Hồ Chí Minh", 2: "An Giang", 3: "Cần Thơ", 4: "Cà Mau",
    5: "Vũng Tàu", 6: "Tây Ninh", 7: "Phan Thiết", 8: "Kiên Giang",
    9: "Bạc Liêu", 10: "Trà Vinh", 11: "Bến Tre"
}

# Danh sách các cạnh (u, v, w) u-----w------v
canh = [
    (8, 2, 54), (8, 3, 101), (3, 4, 116), (3, 9, 85),
    (4, 9, 54), (3, 10, 65), (3, 11, 71), (2, 11, 124),
    (2, 6, 127), (2, 1, 152), (6, 1, 82), (1, 11, 70),
    (1, 5, 72), (1, 7, 180), (5, 7, 141)
]

do_thi = {}  # dict lưu ds kề trong đồ thị { u: [(v1, w1), (v2, w2),..]}
def ds_ke():
    for u, v, w in canh:
        if u not in do_thi:
            do_thi[u] = []
        if v not in do_thi:
            do_thi[v] = []
        do_thi[u].append((v, w))
        do_thi[v].append((u, w))

# Hàm chuyển danh sách số → tên thành phố
def hien_thi_duong_di(path):
    if path:
        return " → ".join(ten_thanh_pho[diem] for diem in path)
    return "Không tìm thấy đường đi."

def dfs(s, e):
    st = deque([(s, [s])])  # mỗi phần tử là (đỉnh hiện tại, đường đi)
    vi = set()
    while st:
        u, path = st.pop()  # lấy phần tử cuối LIFO 
        if u == e:
            return path
        if u not in vi:
            vi.add(u)
            for u_ke, _ in do_thi.get(u, []):
                if u_ke not in vi:
                    st.append((u_ke, path + [u_ke])) 
    return None

def bfs(s, e):
    st = deque([(s, [s])])  # queue lưu (đỉnh hiện tại, đường đi từ s đến nó)
    vi = set()              # tập các đỉnh đã thăm

    while st:
        u, path = st.popleft()  # lấy phần tử đầu tiên trong queue (FIFO)
        if u == e:
            return path         # tìm thấy đích → trả về đường đi
        if u not in vi:
            vi.add(u)
            for u_ke, _ in do_thi.get(u, []):  # lặp các đỉnh kề
                if u_ke not in vi:
                    st.append((u_ke, path + [u_ke]))  # thêm đường đi mới vào queue
    return None

# Uniform Cost Search
def ucs(s, e):
    vi = set()  # Set để theo dõi các đỉnh đã thăm
    q = [(0, [s])]  # Hàng đợi ưu tiên (chi phí, đường đi)
    
    while q:
        c, p = heapq.heappop(q)  # Lấy phần tử có chi phí nhỏ nhất
        
        u = p[-1]  # Đỉnh cuối trong đường đi hiện tại
        
        if u in vi:  # Nếu đỉnh đã thăm, bỏ qua
            continue

        vi.add(u)  # Đánh dấu đỉnh đã thăm

        if u == e:  # Nếu đến đích, trả về đường đi
            return p, c
        
        for u_ke, k_c in do_thi.get(u, []):  # Duyệt các đỉnh kề
            if u_ke not in vi:  # Nếu đỉnh kề chưa thăm
                c_new = c + k_c  # Tính chi phí mới
                q.append((c_new, p + [u_ke]))  # Thêm đường đi mới vào hàng đợi
    
    return None, 0  # Nếu không tìm thấy đường đi

# Depth-Limited Search
def dls(s, e, L):
    st = [(s, [s], 0)]  # stack lưu đỉnh, đường đi, độ sâu hiện tại
    vi = set()  # set để theo dõi các đỉnh đã thăm

    while st:
        u, p, l = st.pop()  # lấy đỉnh hiện tại u, đường đi p, độ sâu hiện tại l trong st LIFO

        # return path if found
        if u == e:
            return p

        if u not in vi and l < L:
            vi.add(u)
            # Duyệt qua các đỉnh kề của u
            for u_ke, _ in do_thi.get(u, []):  # Assuming do_thi[u] is a list of neighbors
                if u_ke not in vi:
                    st.append((u_ke, p + [u_ke], l + 1))

    return None

# Iterative Deepening Depth-First Search
def iddfs(s, e, L):
    for d in range(L + 1):
        kq = dls(s, e, d)
        if kq:
            return kq
    return None 

# Xây dựng đồ thị
ds_ke()

# Hiển thị danh sách thành phố
print("Danh sách các thành phố:")
for so, ten in ten_thanh_pho.items():
    print(f"{so}: {ten}")

# Nhập điểm bắt đầu và điểm đích
bat_dau = int(input("Nhập điểm bắt đầu: "))
ket_thuc = int(input("Nhập điểm đích: "))

# Chạy các thuật toán
print("DFS Path:", hien_thi_duong_di(dfs(bat_dau, ket_thuc)))
print("BFS Path:", hien_thi_duong_di(bfs(bat_dau, ket_thuc)))
duong_di_UCS, chi_phi_UCS = ucs(bat_dau, ket_thuc)
print("UCS Path:", hien_thi_duong_di(duong_di_UCS), "with cost:", chi_phi_UCS)
print("DLS Path:", hien_thi_duong_di(dls(bat_dau, ket_thuc, 5)))
print("IDDFS Path:", hien_thi_duong_di(iddfs(bat_dau, ket_thuc, 5)))
