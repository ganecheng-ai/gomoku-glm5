"""
游戏常量定义
"""

# 窗口设置
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_TITLE = "五子棋 - Gomoku"

# 棋盘设置
BOARD_SIZE = 15  # 15x15 棋盘
CELL_SIZE = 40  # 每个格子大小
BOARD_MARGIN = 50  # 棋盘边距

# 颜色定义 (RGB)
COLOR_BACKGROUND = (222, 184, 135)  # 棋盘背景色 (浅棕色)
COLOR_BOARD_LINE = (0, 0, 0)  # 棋盘线颜色 (黑色)
COLOR_BLACK_PIECE = (20, 20, 20)  # 黑棋颜色
COLOR_WHITE_PIECE = (250, 250, 250)  # 白棋颜色
COLOR_HIGHLIGHT = (255, 0, 0)  # 高亮颜色
COLOR_LAST_MOVE = (255, 165, 0)  # 最后一步标记颜色
COLOR_TEXT = (50, 50, 50)  # 文字颜色
COLOR_BUTTON = (139, 69, 19)  # 按钮颜色
COLOR_BUTTON_HOVER = (160, 82, 45)  # 按钮悬停颜色
COLOR_PANEL_BG = (245, 222, 179)  # 面板背景色

# 棋子设置
PIECE_RADIUS = 17  # 棋子半径

# 游戏状态
GAME_STATE_PLAYING = "playing"
GAME_STATE_BLACK_WIN = "black_win"
GAME_STATE_WHITE_WIN = "white_win"
GAME_STATE_DRAW = "draw"

# 玩家
PLAYER_BLACK = 1
PLAYER_WHITE = 2

# 字体
FONT_SIZE_TITLE = 36
FONT_SIZE_NORMAL = 20
FONT_SIZE_SMALL = 16