"""
棋盘类
"""

from .constants import *


class Board:
    """五子棋棋盘类"""

    def __init__(self):
        """初始化棋盘"""
        self.size = BOARD_SIZE
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None
        self.move_history = []

    def reset(self):
        """重置棋盘"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None
        self.move_history = []

    def is_valid_position(self, row, col):
        """检查位置是否有效"""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        """检查位置是否为空"""
        return self.grid[row][col] == 0

    def place_piece(self, row, col, player):
        """放置棋子"""
        if self.is_valid_position(row, col) and self.is_empty(row, col):
            self.grid[row][col] = player
            self.last_move = (row, col)
            self.move_history.append((row, col, player))
            return True
        return False

    def get_piece(self, row, col):
        """获取指定位置的棋子"""
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None

    def undo_last_move(self):
        """悔棋"""
        if self.move_history:
            row, col, player = self.move_history.pop()
            self.grid[row][col] = 0
            if self.move_history:
                self.last_move = self.move_history[-1][:2]
            else:
                self.last_move = None
            return True
        return False

    def check_winner(self, row, col):
        """检查是否获胜"""
        player = self.grid[row][col]
        if player == 0:
            return None

        # 检查四个方向
        directions = [
            (0, 1),   # 水平
            (1, 0),   # 垂直
            (1, 1),   # 对角线
            (1, -1),  # 反对角线
        ]

        for dr, dc in directions:
            count = 1  # 当前棋子

            # 正方向计数
            r, c = row + dr, col + dc
            while self.is_valid_position(r, c) and self.grid[r][c] == player:
                count += 1
                r += dr
                c += dc

            # 反方向计数
            r, c = row - dr, col - dc
            while self.is_valid_position(r, c) and self.grid[r][c] == player:
                count += 1
                r -= dr
                c -= dc

            if count >= 5:
                return player

        return None

    def is_full(self):
        """检查棋盘是否已满"""
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def get_board_position(self, mouse_x, mouse_y):
        """将鼠标坐标转换为棋盘坐标"""
        # 计算棋盘起点
        start_x = BOARD_MARGIN
        start_y = BOARD_MARGIN

        # 计算棋盘坐标
        col = round((mouse_x - start_x) / CELL_SIZE)
        row = round((mouse_y - start_y) / CELL_SIZE)

        # 检查是否在有效范围内
        if self.is_valid_position(row, col):
            # 检查鼠标是否在格子中心附近
            center_x = start_x + col * CELL_SIZE
            center_y = start_y + row * CELL_SIZE
            distance = ((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2) ** 0.5
            if distance < PIECE_RADIUS + 5:
                return row, col

        return None, None