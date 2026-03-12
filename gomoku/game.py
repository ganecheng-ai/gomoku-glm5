"""
五子棋游戏主模块
"""

import sys
import pygame
from .constants import *
from .board import Board
from .player import Player
from .ui import UI
from .timer import GameTimer
from .sound import SoundManager
from .record import GameRecord, RecordManager
from .logger import get_logger
from .ai import AIPlayer


class Game:
    """五子棋游戏类"""

    def __init__(self):
        """初始化游戏"""
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        # 初始化日志
        self.logger = get_logger()
        self.logger.log_game_start()

        # 创建窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # 初始化游戏组件
        self.board = Board()
        self.ui = UI(self.screen)

        # 初始化计时器
        self.timer = GameTimer(DEFAULT_TIME_LIMIT)
        self.timer_enabled = TIMER_ENABLED

        # 初始化音效
        self.sound = SoundManager()

        # 初始化记录管理器
        self.record_manager = RecordManager()
        self.record = GameRecord()

        # 初始化玩家
        self.black_player = Player(PLAYER_BLACK, "黑棋")
        self.white_player = Player(PLAYER_WHITE, "白棋")
        self.current_player = self.black_player

        # 游戏模式和AI设置
        self.game_mode = GAME_MODE_PVP  # 默认双人对战
        self.ai_difficulty = AI_DIFFICULTY_MEDIUM  # 默认中等难度
        self.ai_player = None  # AI玩家实例

        # 游戏状态
        self.state = GAME_STATE_PLAYING
        self.winner = None
        self.is_selecting_mode = True  # 是否在模式选择界面

        # 按钮区域
        self.restart_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.undo_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.quit_btn_rect = pygame.Rect(0, 0, 0, 0)
        self._update_button_rects()

        # 模式选择按钮区域
        self.pvp_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.pve_btn_rect = pygame.Rect(0, 0, 0, 0)
        self._update_mode_button_rects()

        # 运行标志
        self.running = True

        self.logger.info("游戏初始化完成")

    def _update_button_rects(self):
        """更新按钮区域"""
        sidebar_x = BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE + 60
        sidebar_width = WINDOW_WIDTH - sidebar_x - 20

        self.restart_btn_rect = pygame.Rect(sidebar_x + 15, 280, sidebar_width - 30, 35)
        self.undo_btn_rect = pygame.Rect(sidebar_x + 15, 325, sidebar_width - 30, 35)
        self.quit_btn_rect = pygame.Rect(sidebar_x + 15, 370, sidebar_width - 30, 35)

    def _update_mode_button_rects(self):
        """更新模式选择按钮区域"""
        center_x = WINDOW_WIDTH // 2
        self.pvp_btn_rect = pygame.Rect(center_x - 150, 300, 120, 50)
        self.pve_btn_rect = pygame.Rect(center_x + 30, 300, 120, 50)

    def set_game_mode(self, mode):
        """
        设置游戏模式
        :param mode: GAME_MODE_PVP 或 GAME_MODE_PVE
        """
        self.game_mode = mode

        if mode == GAME_MODE_PVE:
            # 人机模式：AI执白棋
            self.ai_player = AIPlayer(PLAYER_WHITE, self.ai_difficulty)
            self.logger.info(f"游戏模式: 人机对战 (AI难度: {self.ai_difficulty})")
        else:
            self.ai_player = None
            self.logger.info("游戏模式: 双人对战")

        self.is_selecting_mode = False
        self.sound.play_button()

    def reset(self):
        """重置游戏"""
        # 保存上一局记录（如果有）
        if self.record.moves:
            self.record_manager.save_record(self.record)

        self.board.reset()
        self.black_player.reset()
        self.white_player.reset()
        self.current_player = self.black_player
        self.state = GAME_STATE_PLAYING
        self.winner = None

        # 重置计时器
        self.timer.reset()

        # 重置记录
        self.record = GameRecord()
        self.record.start()

        # 返回模式选择界面
        self.is_selecting_mode = True
        self.ai_player = None

        # 播放按钮音效
        self.sound.play_button()

        # 记录日志
        self.logger.log_reset()

    def get_current_player_name(self):
        """获取当前玩家名称"""
        return self.current_player.get_piece_name()

    def get_total_moves(self):
        """获取总步数"""
        return len(self.board.move_history)

    def get_status_text(self):
        """获取游戏状态文字"""
        if self.state == GAME_STATE_BLACK_WIN:
            return "黑棋获胜!"
        elif self.state == GAME_STATE_WHITE_WIN:
            return "白棋获胜!"
        elif self.state == GAME_STATE_DRAW:
            return "平局!"
        else:
            return "游戏进行中"

    def get_timer_info(self):
        """获取计时器信息"""
        if not self.timer_enabled:
            return None
        return self.timer.get_format_times()

    def is_game_over(self):
        """检查游戏是否结束"""
        return self.state != GAME_STATE_PLAYING

    def handle_click(self, pos):
        """处理鼠标点击"""
        if self.is_game_over():
            return

        # 人机模式下，如果是AI回合，不允许玩家点击
        if self.game_mode == GAME_MODE_PVE and self.ai_player:
            if self.current_player.player_type == self.ai_player.player_type:
                return

        # 将鼠标坐标转换为棋盘坐标
        row, col = self.board.get_board_position(pos[0], pos[1])

        if row is not None and col is not None:
            # 放置棋子
            if self.board.place_piece(row, col, self.current_player.player_type):
                self.current_player.add_move()

                # 记录这一步
                elapsed = self.timer.get_current_time() if self.timer_enabled else 0
                self.record.add_move(row, col, self.current_player.player_type, elapsed)

                # 播放落子音效
                self.sound.play_place()

                # 记录落子日志
                self.logger.log_move(row, col, self.current_player.player_type, len(self.board.move_history))

                # 检查胜负
                if not self._check_game_end(row, col):
                    # 切换玩家和计时器
                    self._switch_player()

                    # 人机模式下，AI自动落子
                    if self.game_mode == GAME_MODE_PVE and self.ai_player:
                        if self.current_player.player_type == self.ai_player.player_type:
                            self.ai_move()

    def _check_game_end(self, row, col):
        """检查游戏是否结束"""
        winner = self.board.check_winner(row, col)
        if winner == PLAYER_BLACK:
            self.state = GAME_STATE_BLACK_WIN
            self.winner = winner
            self._end_game(winner)
            return True
        elif winner == PLAYER_WHITE:
            self.state = GAME_STATE_WHITE_WIN
            self.winner = winner
            self._end_game(winner)
            return True
        elif self.board.is_full():
            self.state = GAME_STATE_DRAW
            self._end_game(0)
            return True
        return False

    def _switch_player(self):
        """切换玩家"""
        self.current_player = (
            self.white_player if self.current_player == self.black_player
            else self.black_player
        )
        if self.timer_enabled:
            self.timer.switch_turn()

    def ai_move(self):
        """AI落子"""
        if not self.ai_player or self.is_game_over():
            return

        # 获取AI的最佳落子位置
        row, col = self.ai_player.get_best_move(self.board)

        if self.board.place_piece(row, col, self.ai_player.player_type):
            self.current_player.add_move()

            # 记录这一步
            elapsed = self.timer.get_current_time() if self.timer_enabled else 0
            self.record.add_move(row, col, self.ai_player.player_type, elapsed)

            # 播放落子音效
            self.sound.play_place()

            # 记录AI落子日志
            self.logger.log_move(row, col, self.ai_player.player_type, len(self.board.move_history))

            # 检查胜负
            if not self._check_game_end(row, col):
                self._switch_player()

    def _end_game(self, winner):
        """结束游戏"""
        self.timer.stop()

        if winner == PLAYER_BLACK:
            self.record.set_winner(PLAYER_BLACK)
            self.sound.play_win()
        elif winner == PLAYER_WHITE:
            self.record.set_winner(PLAYER_WHITE)
            self.sound.play_win()
        else:
            self.record.set_draw()
            self.sound.play_draw()

        # 保存记录
        self.record_manager.save_record(self.record)

        # 记录日志
        self.logger.log_game_end(winner)

    def handle_button_click(self, pos):
        """处理按钮点击"""
        if self.restart_btn_rect.collidepoint(pos):
            self.reset()
        elif self.undo_btn_rect.collidepoint(pos):
            self.undo()
        elif self.quit_btn_rect.collidepoint(pos):
            self.running = False

    def undo(self):
        """悔棋"""
        if self.is_game_over():
            return

        if not self.board.move_history:
            return

        # 人机模式下，需要撤销两步（玩家和AI各一步）
        if self.game_mode == GAME_MODE_PVE and self.ai_player:
            # 撤销AI的一步
            if self.board.move_history:
                last_move = self.board.move_history[-1]
                if self.board.undo_last_move():
                    self.sound.play_undo()
                    self.logger.log_undo(last_move[0], last_move[1], last_move[2])

            # 撤销玩家的一步
            if self.board.move_history:
                last_move = self.board.move_history[-1]
                if self.board.undo_last_move():
                    self.sound.play_undo()
                    self.logger.log_undo(last_move[0], last_move[1], last_move[2])

            # 重置计时器到玩家回合
            self.current_player = self.black_player
            if self.timer_enabled:
                self.timer.start_turn(True)
        else:
            # 双人模式，撤销一步
            last_move = self.board.move_history[-1]
            if self.board.undo_last_move():
                # 播放悔棋音效
                self.sound.play_undo()

                # 记录悔棋日志
                self.logger.log_undo(last_move[0], last_move[1], last_move[2])

                # 切换回上一个玩家
                self.current_player = (
                    self.white_player if self.current_player == self.black_player
                    else self.black_player
                )

                # 切换计时器
                if self.timer_enabled:
                    self.timer.switch_turn()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if self.is_selecting_mode:
                            # 模式选择界面
                            if self.pvp_btn_rect.collidepoint(event.pos):
                                self.set_game_mode(GAME_MODE_PVP)
                                # 开始记录
                                self.record.start()
                                # 开始计时
                                if self.timer_enabled:
                                    self.timer.start_turn(True)
                            elif self.pve_btn_rect.collidepoint(event.pos):
                                self.set_game_mode(GAME_MODE_PVE)
                                # 开始记录
                                self.record.start()
                                # 开始计时
                                if self.timer_enabled:
                                    self.timer.start_turn(True)
                        else:
                            # 游戏界面
                            if self.restart_btn_rect.collidepoint(event.pos):
                                self.reset()
                            elif self.undo_btn_rect.collidepoint(event.pos):
                                self.undo()
                            elif self.quit_btn_rect.collidepoint(event.pos):
                                self.running = False
                            else:
                                # 检查是否点击棋盘
                                self.handle_click(event.pos)

            # 渲染
            self.screen.fill((240, 230, 210))  # 背景色

            if self.is_selecting_mode:
                # 绘制模式选择界面
                self.ui.draw_mode_selection(self)
            else:
                # 绘制游戏界面
                self.ui.draw_board(self.board)
                self.ui.draw_sidebar(self)

                # 如果游戏结束，显示结果
                if self.is_game_over():
                    self.ui.draw_game_over(self.winner)

            # 更新显示
            pygame.display.flip()

            # 控制帧率
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """游戏入口函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()