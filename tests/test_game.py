"""
五子棋游戏测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku.board import Board
from gomoku.player import Player
from gomoku.constants import PLAYER_BLACK, PLAYER_WHITE


class TestBoard(unittest.TestCase):
    """棋盘测试"""

    def setUp(self):
        """测试前准备"""
        self.board = Board()

    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.board.size, 15)
        self.assertIsNone(self.board.last_move)
        self.assertEqual(len(self.board.move_history), 0)

    def test_valid_position(self):
        """测试位置有效性"""
        self.assertTrue(self.board.is_valid_position(0, 0))
        self.assertTrue(self.board.is_valid_position(14, 14))
        self.assertFalse(self.board.is_valid_position(-1, 0))
        self.assertFalse(self.board.is_valid_position(15, 0))

    def test_place_piece(self):
        """测试放置棋子"""
        self.assertTrue(self.board.place_piece(7, 7, PLAYER_BLACK))
        self.assertEqual(self.board.get_piece(7, 7), PLAYER_BLACK)
        self.assertEqual(self.board.last_move, (7, 7))
        self.assertFalse(self.board.place_piece(7, 7, PLAYER_WHITE))  # 已有棋子

    def test_undo_move(self):
        """测试悔棋"""
        self.board.place_piece(7, 7, PLAYER_BLACK)
        self.board.place_piece(8, 8, PLAYER_WHITE)
        self.assertEqual(len(self.board.move_history), 2)

        self.assertTrue(self.board.undo_last_move())
        self.assertEqual(len(self.board.move_history), 1)
        self.assertEqual(self.board.get_piece(8, 8), 0)

    def test_horizontal_win(self):
        """测试水平获胜"""
        for i in range(5):
            self.board.place_piece(7, i, PLAYER_BLACK)
        winner = self.board.check_winner(7, 4)
        self.assertEqual(winner, PLAYER_BLACK)

    def test_vertical_win(self):
        """测试垂直获胜"""
        for i in range(5):
            self.board.place_piece(i, 7, PLAYER_BLACK)
        winner = self.board.check_winner(4, 7)
        self.assertEqual(winner, PLAYER_BLACK)

    def test_diagonal_win(self):
        """测试对角线获胜"""
        for i in range(5):
            self.board.place_piece(i, i, PLAYER_BLACK)
        winner = self.board.check_winner(4, 4)
        self.assertEqual(winner, PLAYER_BLACK)

    def test_no_win(self):
        """测试未获胜"""
        self.board.place_piece(7, 7, PLAYER_BLACK)
        self.board.place_piece(7, 8, PLAYER_BLACK)
        self.board.place_piece(7, 9, PLAYER_BLACK)
        winner = self.board.check_winner(7, 9)
        self.assertIsNone(winner)

    def test_board_not_full(self):
        """测试棋盘未满"""
        self.assertFalse(self.board.is_full())

    def test_reset(self):
        """测试重置棋盘"""
        self.board.place_piece(7, 7, PLAYER_BLACK)
        self.board.reset()
        self.assertEqual(self.board.get_piece(7, 7), 0)
        self.assertIsNone(self.board.last_move)


class TestPlayer(unittest.TestCase):
    """玩家测试"""

    def setUp(self):
        """测试前准备"""
        self.black_player = Player(PLAYER_BLACK, "黑棋")
        self.white_player = Player(PLAYER_WHITE, "白棋")

    def test_player_type(self):
        """测试玩家类型"""
        self.assertEqual(self.black_player.player_type, PLAYER_BLACK)
        self.assertEqual(self.white_player.player_type, PLAYER_WHITE)

    def test_piece_name(self):
        """测试棋子名称"""
        self.assertEqual(self.black_player.get_piece_name(), "黑棋")
        self.assertEqual(self.white_player.get_piece_name(), "白棋")

    def test_move_count(self):
        """测试步数计数"""
        self.assertEqual(self.black_player.moves, 0)
        self.black_player.add_move()
        self.assertEqual(self.black_player.moves, 1)

    def test_reset(self):
        """测试重置玩家"""
        self.black_player.add_move()
        self.black_player.add_move()
        self.black_player.reset()
        self.assertEqual(self.black_player.moves, 0)


if __name__ == "__main__":
    unittest.main()