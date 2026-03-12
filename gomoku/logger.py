"""
日志系统模块
提供统一的日志记录功能，方便问题定位和分析
"""

import logging
import os
from datetime import datetime
from .constants import PLAYER_BLACK, PLAYER_WHITE


class GameLogger:
    """游戏日志记录器"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化日志系统"""
        if self._initialized:
            return

        self._initialized = True
        self.logger = logging.getLogger('gomoku')
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加 handler
        if not self.logger.handlers:
            # 创建日志目录
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 文件处理器 - 记录所有日志
            log_filename = datetime.now().strftime('gomoku_%Y%m%d_%H%M%S.log')
            file_handler = logging.FileHandler(
                os.path.join(log_dir, log_filename),
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)

            # 控制台处理器 - 只显示重要日志
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # 日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message):
        """记录严重错误"""
        self.logger.critical(message)

    def log_game_start(self):
        """记录游戏开始"""
        self.info("="*50)
        self.info("游戏开始")
        self.info("="*50)

    def log_game_end(self, winner):
        """记录游戏结束"""
        if winner == PLAYER_BLACK:
            winner_text = "黑棋"
        elif winner == PLAYER_WHITE:
            winner_text = "白棋"
        else:
            winner_text = "平局"

        self.info("="*50)
        self.info(f"游戏结束 - {winner_text}{'获胜' if winner != 0 else ''}")
        self.info("="*50)

    def log_move(self, row, col, player, move_count):
        """记录落子"""
        player_name = "黑棋" if player == PLAYER_BLACK else "白棋"
        self.debug(f"第{move_count}步: {player_name} 落子位置 ({row}, {col})")

    def log_undo(self, row, col, player):
        """记录悔棋"""
        player_name = "黑棋" if player == PLAYER_BLACK else "白棋"
        self.info(f"悔棋: {player_name} 撤销位置 ({row}, {col})")

    def log_reset(self):
        """记录游戏重置"""
        self.info("游戏重置")

    def log_error(self, error_type, error_message):
        """记录错误"""
        self.error(f"{error_type}: {error_message}")

    def log_event(self, event_type, details):
        """记录事件"""
        self.info(f"[{event_type}] {details}")


# 全局日志实例
_logger = None


def get_logger():
    """获取全局日志实例"""
    global _logger
    if _logger is None:
        _logger = GameLogger()
    return _logger