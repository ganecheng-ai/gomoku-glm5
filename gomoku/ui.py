"""
界面渲染模块
"""

import os
import pygame
from .constants import *


class UI:
    """界面渲染类"""

    def __init__(self, screen):
        """初始化界面"""
        self.screen = screen
        self.font_large = None
        self.font_normal = None
        self.font_small = None
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体"""
        # 尝试加载中文字体
        chinese_fonts = [
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'SimHei.ttf'),
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/System/Library/Fonts/PingFang.ttc',
            'C:\\Windows\\Fonts\\simhei.ttf',
            'C:\\Windows\\Fonts\\msyh.ttc',
        ]

        font_path = None
        for path in chinese_fonts:
            if os.path.exists(path):
                font_path = path
                break

        try:
            if font_path:
                self.font_large = pygame.font.Font(font_path, FONT_SIZE_TITLE)
                self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
                self.font_small = pygame.font.Font(font_path, FONT_SIZE_SMALL)
            else:
                # 使用系统默认字体
                self.font_large = pygame.font.SysFont('simhei', FONT_SIZE_TITLE)
                self.font_normal = pygame.font.SysFont('simhei', FONT_SIZE_NORMAL)
                self.font_small = pygame.font.SysFont('simhei', FONT_SIZE_SMALL)
        except Exception:
            # 如果中文字体加载失败，使用默认字体
            self.font_large = pygame.font.Font(None, FONT_SIZE_TITLE)
            self.font_normal = pygame.font.Font(None, FONT_SIZE_NORMAL)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    def draw_board(self, board):
        """绘制棋盘"""
        # 绘制棋盘背景
        board_rect = pygame.Rect(
            BOARD_MARGIN - 20,
            BOARD_MARGIN - 20,
            (BOARD_SIZE - 1) * CELL_SIZE + 40,
            (BOARD_SIZE - 1) * CELL_SIZE + 40
        )
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, board_rect)

        # 绘制棋盘网格线
        for i in range(BOARD_SIZE):
            # 水平线
            start_x = BOARD_MARGIN
            end_x = BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
            y = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_BOARD_LINE, (start_x, y), (end_x, y), 1)

            # 垂直线
            x = BOARD_MARGIN + i * CELL_SIZE
            start_y = BOARD_MARGIN
            end_y = BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_BOARD_LINE, (x, start_y), (x, end_y), 1)

        # 绘制星位（天元和四个角星）
        star_points = [
            (7, 7),   # 天元
            (3, 3), (3, 11), (11, 3), (11, 11),  # 四角星
            (3, 7), (11, 7), (7, 3), (7, 11),  # 边星
        ]
        for row, col in star_points:
            x = BOARD_MARGIN + col * CELL_SIZE
            y = BOARD_MARGIN + row * CELL_SIZE
            pygame.draw.circle(self.screen, COLOR_BOARD_LINE, (x, y), 4)

        # 绘制棋子
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece(row, col)
                if piece != 0:
                    self._draw_piece(row, col, piece, (row, col) == board.last_move)

    def _draw_piece(self, row, col, player, is_last_move=False):
        """绘制棋子"""
        x = BOARD_MARGIN + col * CELL_SIZE
        y = BOARD_MARGIN + row * CELL_SIZE

        # 选择颜色
        color = COLOR_BLACK_PIECE if player == PLAYER_BLACK else COLOR_WHITE_PIECE

        # 绘制棋子阴影
        shadow_offset = 2
        shadow_color = (100, 100, 100) if player == PLAYER_WHITE else (50, 50, 50)
        pygame.draw.circle(self.screen, shadow_color,
                          (x + shadow_offset, y + shadow_offset), PIECE_RADIUS)

        # 绘制棋子
        pygame.draw.circle(self.screen, color, (x, y), PIECE_RADIUS)

        # 绘制棋子边缘
        edge_color = (80, 80, 80) if player == PLAYER_BLACK else (180, 180, 180)
        pygame.draw.circle(self.screen, edge_color, (x, y), PIECE_RADIUS, 1)

        # 绘制棋子光泽
        if player == PLAYER_WHITE:
            highlight_pos = (x - 5, y - 5)
            pygame.draw.circle(self.screen, (255, 255, 255), highlight_pos, 4)
        else:
            highlight_pos = (x - 5, y - 5)
            pygame.draw.circle(self.screen, (60, 60, 60), highlight_pos, 3)

        # 标记最后一步
        if is_last_move:
            mark_color = COLOR_LAST_MOVE
            pygame.draw.circle(self.screen, mark_color, (x, y), 5)

    def draw_sidebar(self, game):
        """绘制侧边栏"""
        # 侧边栏位置
        sidebar_x = BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE + 60
        sidebar_width = WINDOW_WIDTH - sidebar_x - 20

        # 绘制侧边栏背景
        sidebar_rect = pygame.Rect(sidebar_x, 20, sidebar_width, WINDOW_HEIGHT - 40)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, (139, 69, 19), sidebar_rect, 2, border_radius=10)

        # 绘制标题
        title = self.font_large.render("五子棋", True, COLOR_TEXT)
        self.screen.blit(title, (sidebar_x + (sidebar_width - title.get_width()) // 2, 40))

        # 绘制当前玩家
        current_player = game.get_current_player_name()
        player_text = self.font_normal.render(f"当前: {current_player}", True, COLOR_TEXT)
        self.screen.blit(player_text, (sidebar_x + 15, 100))

        # 绘制步数
        moves_text = self.font_normal.render(f"步数: {game.get_total_moves()}", True, COLOR_TEXT)
        self.screen.blit(moves_text, (sidebar_x + 15, 140))

        # 绘制游戏状态
        status = game.get_status_text()
        status_text = self.font_normal.render(status, True, COLOR_HIGHLIGHT if game.is_game_over() else COLOR_TEXT)
        self.screen.blit(status_text, (sidebar_x + 15, 180))

        # 绘制按钮
        self._draw_button(sidebar_x + 15, 250, sidebar_width - 30, 40, "重新开始", game.restart_btn_rect)
        self._draw_button(sidebar_x + 15, 310, sidebar_width - 30, 40, "悔棋", game.undo_btn_rect)
        self._draw_button(sidebar_x + 15, 370, sidebar_width - 30, 40, "退出", game.quit_btn_rect)

        # 绘制帮助信息
        help_y = 440
        help_texts = [
            "游戏规则:",
            "1. 黑棋先行",
            "2. 轮流下棋",
            "3. 五子连珠获胜",
            "",
            "操作说明:",
            "• 点击棋盘落子",
            "• 支持悔棋功能",
        ]
        for i, text in enumerate(help_texts):
            help_text = self.font_small.render(text, True, COLOR_TEXT)
            self.screen.blit(help_text, (sidebar_x + 15, help_y + i * 25))

    def _draw_button(self, x, y, width, height, text, rect):
        """绘制按钮"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        # 按钮颜色
        color = COLOR_BUTTON_HOVER if is_hover else COLOR_BUTTON

        # 绘制按钮背景
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 50, 10), rect, 2, border_radius=5)

        # 绘制按钮文字
        text_surface = self.font_normal.render(text, True, (255, 255, 255))
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def draw_game_over(self, winner):
        """绘制游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # 获胜文字
        if winner == PLAYER_BLACK:
            text = "黑棋获胜!"
        elif winner == PLAYER_WHITE:
            text = "白棋获胜!"
        else:
            text = "平局!"

        # 绘制文字
        text_surface = self.font_large.render(text, True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # 绘制文字背景
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 215, 0), bg_rect, 3, border_radius=10)

        self.screen.blit(text_surface, text_rect)