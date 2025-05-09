from collections import defaultdict, deque
import itertools

class CSP:
    """Lớp cơ sở mô tả bài toán Ràng buộc (Constraint Satisfaction Problem)."""
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables                      # Danh sách biến
        self.domains = domains                          # Miền giá trị cho từng biến
        self.neighbors = neighbors                      # Hàng xóm của từng biến
        self.constraints = constraints                  # Hàm ràng buộc giữa 2 biến


class Sudoku(CSP):
    """Lớp Sudoku mở rộng từ CSP để mô tả bài toán Sudoku."""
    def __init__(self, grid):
        # Danh sách ô từ A1 đến I9
        self.variables = [r + c for r in "ABCDEFGHI" for c in "123456789"]

        # Thiết lập hàng, cột
        self.rows = "ABCDEFGHI"
        self.cols = "123456789"

        # Tạo danh sách các đơn vị (unit): hàng, cột, khối
        self.unitlist = (
            [self.cross(r, self.cols) for r in self.rows] +
            [self.cross(self.rows, c) for c in self.cols] +
            [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        )

        # Tạo từ điển: mỗi ô liên quan đến các unit của nó
        self.units = {s: [u for u in self.unitlist if s in u] for s in self.variables}

        # Hàng xóm của mỗi ô: tất cả các ô trong cùng unit (trừ chính nó)
        self.neighbors = {s: set(sum(self.units[s], [])) - {s} for s in self.variables}

        # Parse lưới Sudoku đầu vào
        values = self.parse_grid(grid)

        # Khởi tạo miền giá trị cho từng biến
        domains = {var: [values[var]] if values[var] in "123456789" else list("123456789")
                   for var in self.variables}

        # Gọi constructor của lớp CSP
        super().__init__(self.variables, domains, self.neighbors, self.sudoku_constraints)

    def cross(self, A, B):
        """Tạo tích Descartes giữa 2 chuỗi."""
        return [a + b for a in A for b in B]

    def parse_grid(self, grid):
        """Chuyển chuỗi Sudoku 81 ký tự thành dict {ô: giá trị}."""
        chars = [c for c in grid if c in "123456789." or c == '0']
        assert len(chars) == 81
        return dict(zip(self.variables, chars))

    def sudoku_constraints(self, A, a, B, b):
        """Ràng buộc Sudoku: hai ô liên kết thì không được có cùng giá trị."""
        return a != b

    # def display(self):
    #     """Hiển thị bảng Sudoku."""
    #     width = 2 + max(len(self.domains[s]) for s in self.variables)
    #     line = "+".join(["-" * (width * 3)] * 3)
    #     for r in self.rows:
    #         print("".join(self.domains[r + c][0] if len(self.domains[r + c]) == 1
    #                      else ".".center(width)
    #                      for c in self.cols))
    #         if r in "CF":
    #             print(line)
    #     print()
    def display(self):
        """Hiển thị bảng Sudoku đẹp hơn."""
        width = 2 + max(len(self.domains[s]) for s in self.variables)
        line = "+".join(["-" * (width * 3)] * 3)

        for r in self.rows:
            row = ""
            for c in self.cols:
                var = r + c
                # Nếu miền chỉ có một giá trị, in giá trị đó, ngược lại in dấu chấm
                value = self.domains[var][0] if len(self.domains[var]) == 1 else "."
                row += value.center(width) + " "
                # Thêm dấu "|" sau mỗi cột 3
                if c in "36":
                    row += "| "
            print(row)
            # Thêm dòng phân cách sau mỗi 3 hàng
            if r in "CF":
                print(line)
        print()


def AC3(csp):
    """
    Thuật toán AC-3 để duy trì tính nhất quán cung.
    Trả về True nếu giải được một phần hoặc hoàn chỉnh, False nếu mâu thuẫn.
    """
    queue = deque([(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]])

    while queue:
        Xi, Xj = queue.popleft()
        if revise(csp, Xi, Xj):
            if not csp.domains[Xi]:  # Nếu miền rỗng → mâu thuẫn
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def revise(csp, Xi, Xj):
    """
    Thử rút gọn miền của Xi sao cho đảm bảo nhất quán với Xj.
    Trả về True nếu miền của Xi bị thay đổi.
    """
    revised = False
    for x in csp.domains[Xi][:]:  # Duyệt qua bản sao để tránh lỗi khi xóa
        if not any(csp.constraints(Xi, x, Xj, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
    return revised


if __name__ == "__main__":
    # Bạn có thể thay chuỗi grid này bằng bất kỳ đề bài Sudoku nào khác
    grid = ".2...194881.6.......4.276..17..9...33.........48.53.....61....2....74..6.5.9....7"
    print(len(grid))
    sudoku = Sudoku(grid)

    print("Sudoku ban đầu:")    
    sudoku.display()

    if AC3(sudoku):
        print("Sau khi áp dụng AC-3:")
        sudoku.display()
    else:
        print("Không thể giải Sudoku bằng AC-3 do có mâu thuẫn.")
