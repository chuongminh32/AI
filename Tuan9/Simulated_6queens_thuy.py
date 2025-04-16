import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

class NQueensSolver:
    def __init__(self, n=6):
        self.n = n
        self.board = self.generate_random_board()
        self.attacks = self.calculate_attacks(self.board)
        self.history = []
        self.solution_found = False

    def calculate_attacks(self, board):
        """Tính số cặp hậu tấn công lẫn nhau"""
        attacks = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                    attacks += 1
        return attacks

    def generate_random_board(self):
        """Tạo bàn cờ ngẫu nhiên"""
        return [random.randint(0, self.n-1) for _ in range(self.n)]

    def simulated_annealing_step(self, temp, cooling_rate):
        """Thực hiện một bước của thuật toán Simulated Annealing"""
        if self.attacks == 0:
            self.solution_found = True
            return temp * cooling_rate

        # Tạo trạng thái mới
        new_board = list(self.board)
        col = random.randint(0, self.n-1)
        new_row = random.randint(0, self.n-1)
        new_board[col] = new_row
        new_attacks = self.calculate_attacks(new_board)

        # Tính toán delta E
        delta_e = self.attacks - new_attacks

        # Quyết định chấp nhận trạng thái mới
        if delta_e > 0 or (temp > 0 and random.random() < math.exp(delta_e / max(temp, 0.1))):
            self.board = new_board
            self.attacks = new_attacks

        # Lưu lại trạng thái hiện tại để hiển thị
        self.history.append((list(self.board), self.attacks, temp))

        return temp * cooling_rate

    def visualize_board(self, board, attacks, temp, ax):
        """Hiển thị bàn cờ với đường viền chính xác"""
        # Tạo bàn cờ với màu sắc
        chessboard = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                chessboard[i][j] = (i + j) % 2

        # Hiển thị bàn cờ với kích thước nhỏ
        cmap = ListedColormap(['#f0d9b5', '#b58863'])
        ax.imshow(chessboard, cmap=cmap, extent=[0, self.n, 0, self.n], aspect='auto')

        # Vẽ đường viền grid chính xác
        for i in range(self.n + 1):
            ax.axhline(i, color='black', linewidth=0.5)
            ax.axvline(i, color='black', linewidth=0.5)

        # Đặt các quân hậu
        for col, row in enumerate(board):
            ax.text(col + 0.5, row + 0.5, '♕', fontsize=18, ha='center', va='center',
                   color='black' )

        # Thông tin trạng thái
        ax.set_title(f'6 Queens Problem - Simulated Annealing\n'
                    f'Attacks: {attacks} - Temperature: {temp:.2f}')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, self.n)
        ax.set_ylim(0, self.n)

def animate(i):
    """Hàm animation với tốc độ chậm"""
    if i < len(solver.history):
        board, attacks, temp = solver.history[i]
        ax.clear()
        solver.visualize_board(board, attacks, temp, ax)

        # Dừng animation khi tìm thấy giải pháp
        if attacks == 0:
            ax.text(solver.n/2, -0.5, 'SOLUTION FOUND!',
                   fontsize=12, ha='center', color='green', weight='bold')
            ani.event_source.stop()
    else:
        ani.event_source.stop()

# Tham số thuật toán
initial_temp = 100
cooling_rate = 0.95
max_iter = 5000

# Khởi tạo solver
solver = NQueensSolver(n=6)

# Chạy thuật toán
temp = initial_temp
for _ in range(max_iter):
    temp = solver.simulated_annealing_step(temp, cooling_rate)
    if solver.solution_found:
        break

# Tạo figure với kích thước nhỏ
fig, ax = plt.subplots(figsize=(6, 6))

# Animation với interval 200ms (chậm)
ani = FuncAnimation(fig, animate, frames=len(solver.history), interval=200, repeat=False)

plt.tight_layout()
plt.show()