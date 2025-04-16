def is_safe(board, row, col):
    """Kiểm tra nếu đặt hậu ở (row, col) có an toàn không"""
    # Kiểm tra cột phía trên
    for i in range(row):
        if board[i] == col:
            return False
    
    # Kiểm tra đường chéo trái phía trên
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i] == j:
            return False
    
    # Kiểm tra đường chéo phải phía trên
    for i, j in zip(range(row-1, -1, -1), range(col+1, 6)):
        if board[i] == j:
            return False
    return True

def solve_6queens_and_or(board, row):
    """Hàm đệ quy giải bài toán sử dụng AND-OR (theo dòng)"""
    # Base case: nếu tất cả các hàng đã được đặt
    if row >= 6:
        return True
    
    # OR node: thử tất cả các cột trong hàng hiện tại
    for col in range(6):
        # AND condition: kiểm tra nếu cột này an toàn
        if is_safe(board, row, col):
            board[row] = col  # Đặt hậu
            
            # Đệ quy giải các bài toán con (các hàng tiếp theo)
            if solve_6queens_and_or(board, row + 1):
                return True
            
            # Nếu dẫn đến thất bại, bỏ đặt (backtrack)
            board[row] = -1
    return False

def print_solution(board):
    """Hiển thị bàn cờ"""
    for row in range(6):
        line = ""
        for col in range(6):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

# Khởi tạo và giải bài toán
initial_board = [-1] * 6  # -1 nghĩa là chưa đặt hậu
if solve_6queens_and_or(initial_board, 0):
    print("Giải pháp tìm được:")
    print_solution(initial_board)
else:
    print("Không tìm thấy giải pháp")