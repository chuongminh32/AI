import time

# Hàm giải Sudoku sử dụng Backtracking
def backtracking_core(board, size):
    # Hàm kiểm tra nếu một số có thể được điền vào ô (r, c)
    def is_safe(board, r, c, num):
        # Kiểm tra hàng
        for col in range(size):
            if board[r][col] == num:
                return False
        # Kiểm tra cột
        for row in range(size):
            if board[row][c] == num:
                return False
        # Kiểm tra khối (box)
        box_size = int(size ** 0.5)  # Kích thước của mỗi khối (box)
        box_row_start = (r // box_size) * box_size
        box_col_start = (c // box_size) * box_size
        for i in range(box_row_start, box_row_start + box_size):
            for j in range(box_col_start, box_col_start + box_size):
                if board[i][j] == num:
                    return False
        return True

    # Hàm giải đệ quy
    def solve():
        # Tìm ô trống
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    # Thử các số từ 1 đến size
                    for num in range(1, size + 1):
                        if is_safe(board, r, c, num):
                            board[r][c] = num  # Điền số vào ô
                            if solve():  # Đệ quy giải tiếp
                                return True
                            board[r][c] = 0  # Nếu không giải được, quay lại (backtrack)
                    return False  # Nếu không tìm được số hợp lệ, quay lại (backtrack)
        return True  # Nếu không còn ô trống, đã giải xong

    return solve()

# Hàm main để chạy giải bài Sudoku
if __name__ == "__main__":
    # Bảng Sudoku mẫu (0 là ô trống cần điền)
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # Kích thước bảng Sudoku
    size = 9

    # Thời gian bắt đầu
    start_time = time.perf_counter()

    # Giải bài toán Sudoku
    if backtracking_core(sudoku_board, size):
        print("Bài toán đã được giải!")
    else:
        print("Không thể giải được bài toán.")

    # In ra bảng Sudoku đã giải
    for row in sudoku_board:
        print(row)

    # Thời gian kết thúc
    end_time = time.perf_counter()
    print(f"Thời gian giải: {end_time - start_time:.4f} giây.")
