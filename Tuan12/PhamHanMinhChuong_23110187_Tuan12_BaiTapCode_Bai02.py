import tkinter as tk
from tkinter import messagebox
import random
import time

#  PHẦN 1: LỚP GIẢI THUẬT MIN-CONFLICTS - TÁCH BIỆT HOÀN TOÀN VỚI GUI (cải tiến)
class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.variables = list(range(n))  # Danh sách cột: mỗi biến là 1 cột (0 đến n-1)

    def random_assign(self):
        #  Gán ngẫu nhiên: mỗi cột được gán một dòng ngẫu nhiên
        return {var: random.randint(0, self.n - 1) for var in self.variables}

    def count_conflicts(self, var, val, assign):
        #  Tính số xung đột cho quân hậu ở vị trí (val, var)
        return sum(
            assign[other] == val or abs(assign[other] - val) == abs(other - var)
            for other in self.variables if other != var
        )

    def conflicted_vars(self, assign):
        #  Trả về danh sách các cột đang có xung đột
        return [var for var in self.variables if self.count_conflicts(var, assign[var], assign) > 0]

    def min_conflict_value(self, var, assign):
        #  Tìm dòng (val) cho cột var sao cho ít xung đột nhất
        min_conflicts = float('inf')
        best_vals = []

        for val in range(self.n):
            conflicts = self.count_conflicts(var, val, assign)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_vals = [val]
            elif conflicts == min_conflicts:
                best_vals.append(val)

        return random.choice(best_vals)  #  Random nếu có nhiều dòng cùng ít xung đột

    def is_solution(self, assign):
        #  Kiểm tra xem đây có phải lời giải không (không có xung đột)
        return not self.conflicted_vars(assign)


#  PHẦN 2: GIAO DIỆN - TÁCH BIỆT VỚI GIẢI THUẬT ( cải tiến lớn)
class NQueensApp:
    def __init__(self, root, n=100):
        self.root = root
        self.n = n
        self.size = 8  #  Kích thước mỗi ô vuông
        self.solver = NQueensSolver(n)
        self.assign = self.solver.random_assign()

        self.frame = tk.Frame(root)
        self.frame.pack()

        #  Canvas có scroll cho bàn cờ lớn
        self.canvas = tk.Canvas(self.frame, width=n*self.size, height=n*self.size, scrollregion=(0, 0, n*self.size, n*self.size))
        self.canvas.grid(row=0, column=0)

        #  Thanh cuộn ngang
        hbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky=tk.EW)
        hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hbar.set)

        #  Thanh cuộn dọc
        vbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky=tk.NS)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)

        #  Thanh trạng thái hiện thông báo tiến trình
        self.status = tk.Label(root, text="Trạng thái: Đã khởi tạo", anchor="w")
        self.status.pack(fill=tk.X)

        #  Nút điều khiển
        ctrl = tk.Frame(root)
        ctrl.pack()
        tk.Button(ctrl, text="Ngẫu nhiên", command=self.random_board).pack(side=tk.LEFT)
        tk.Button(ctrl, text="Giải", command=self.solve).pack(side=tk.LEFT)

        #  Cảnh báo nếu n quá lớn
        if n > 50:
            messagebox.showinfo("Thông báo", f"Bàn cờ có kích thước {n}x{n} có thể hiển thị chậm.\nVui lòng kiên nhẫn chờ...")

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")  # Xóa nội dung cũ

        #  Vẽ ô bàn cờ
        for row in range(self.n):
            for col in range(self.n):
                color = "white" if (row + col) % 2 == 0 else "light gray"  #  Xen kẽ trắng - xám
                self.canvas.create_rectangle(
                    col * self.size, row * self.size,
                    (col + 1) * self.size, (row + 1) * self.size,
                    fill=color, outline="gray"
                )

        self.draw_queens()  #  Vẽ quân hậu sau khi vẽ ô

    def draw_queens(self):
        for col, row in self.assign.items():
            #  Vẽ hình tròn nhỏ màu đỏ tại vị trí có hậu
            self.canvas.create_oval(
                col * self.size + 2, row * self.size + 2,
                (col + 1) * self.size - 2, (row + 1) * self.size - 2,
                fill="red"
            )

    def random_board(self):
        #  Gán lại ngẫu nhiên vị trí quân hậu và vẽ lại
        self.assign = self.solver.random_assign()
        self.status.config(text="Trạng thái: Khởi tạo ngẫu nhiên")
        self.draw_board()

    def solve(self):
        self.status.config(text="Trạng thái: Đang giải...")
        self.frame.update()

        for _ in range(10000):  #  Giới hạn bước lặp tránh treo máy
            if self.solver.is_solution(self.assign):
                self.status.config(text="Trạng thái: Đã giải xong!")
                self.draw_board()
                return

            var = random.choice(self.solver.conflicted_vars(self.assign))  #  Chọn biến xung đột ngẫu nhiên
            self.assign[var] = self.solver.min_conflict_value(var, self.assign)  #  Chuyển về giá trị xung đột thấp nhất

            self.draw_board()
            self.frame.update()
            time.sleep(0.02)  #  Hiệu ứng animation: tạm dừng 0.02s mỗi bước

        self.status.config(text="Trạng thái: Không tìm được lời giải!")
        messagebox.showinfo("Thất bại", "Không tìm được lời giải sau 10000 bước.")

#  PHẦN 3: CHẠY ỨNG DỤNG
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Giải bài toán N-Queens bằng Min-Conflicts")
    app = NQueensApp(root, n=8 )  # Bạn có thể thay đổi n ở đây (ví dụ: 8, 50, 100)
    root.mainloop()

# Tham khảo : 23110357_BuiThanhTung_BaiTap2_100Hau_Tuan12