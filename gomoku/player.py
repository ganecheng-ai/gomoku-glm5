"""
玩家类
"""

from .constants import *


class Player:
    """玩家类"""

    def __init__(self, player_type, name):
        """
        初始化玩家
        :param player_type: 玩家类型 (PLAYER_BLACK 或 PLAYER_WHITE)
        :param name: 玩家名称
        """
        self.player_type = player_type
        self.name = name
        self.moves = 0

    def get_piece_name(self):
        """获取棋子名称"""
        return "黑棋" if self.player_type == PLAYER_BLACK else "白棋"

    def add_move(self):
        """增加步数"""
        self.moves += 1

    def reset(self):
        """重置玩家状态"""
        self.moves = 0