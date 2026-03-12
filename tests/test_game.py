"""
五子棋游戏测试
"""

import unittest
import sys
import os
import tempfile
import shutil

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku.board import Board
from gomoku.player import Player
from gomoku.constants import PLAYER_BLACK, PLAYER_WHITE
from gomoku.timer import Timer, GameTimer
from gomoku.record import GameRecord, RecordManager


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


class TestTimer(unittest.TestCase):
    """计时器测试"""

    def test_timer_init(self):
        """测试计时器初始化"""
        timer = Timer()
        self.assertEqual(timer.time_limit, 0)
        self.assertEqual(timer.elapsed_time, 0)
        self.assertFalse(timer.is_running)

    def test_timer_format_time(self):
        """测试时间格式化"""
        timer = Timer()
        self.assertEqual(timer.format_time(0), "00:00")
        self.assertEqual(timer.format_time(61), "01:01")
        self.assertEqual(timer.format_time(3600), "60:00")

    def test_timer_time_limit(self):
        """测试时间限制"""
        timer = Timer(time_limit=60)
        self.assertEqual(timer.time_limit, 60)
        self.assertEqual(timer.get_remaining_time(), 60)

    def test_game_timer_init(self):
        """测试游戏计时器初始化"""
        game_timer = GameTimer()
        self.assertEqual(game_timer.time_limit, 0)
        self.assertIsNotNone(game_timer.black_timer)
        self.assertIsNotNone(game_timer.white_timer)

    def test_game_timer_switch(self):
        """测试游戏计时器切换"""
        game_timer = GameTimer()
        game_timer.start_turn(True)
        self.assertTrue(game_timer.current_is_black)
        game_timer.switch_turn()
        self.assertFalse(game_timer.current_is_black)

    def test_game_timer_format_times(self):
        """测试游戏计时器格式化"""
        game_timer = GameTimer()
        times = game_timer.get_format_times()
        self.assertIn("black", times)
        self.assertIn("white", times)
        self.assertEqual(times["black"], "00:00")
        self.assertEqual(times["white"], "00:00")


class TestGameRecord(unittest.TestCase):
    """游戏记录测试"""

    def setUp(self):
        """测试前准备"""
        self.record = GameRecord()

    def test_record_init(self):
        """测试记录初始化"""
        self.assertEqual(len(self.record.moves), 0)
        self.assertIsNone(self.record.start_time)
        self.assertIsNone(self.record.winner)

    def test_record_start(self):
        """测试记录开始"""
        self.record.start()
        self.assertIsNotNone(self.record.start_time)

    def test_record_add_move(self):
        """测试添加移动记录"""
        self.record.start()
        self.record.add_move(7, 7, PLAYER_BLACK)
        self.assertEqual(len(self.record.moves), 1)
        self.assertEqual(self.record.moves[0]["row"], 7)
        self.assertEqual(self.record.moves[0]["col"], 7)
        self.assertEqual(self.record.moves[0]["player"], PLAYER_BLACK)

    def test_record_set_winner(self):
        """测试设置获胜者"""
        self.record.set_winner(PLAYER_BLACK)
        self.assertEqual(self.record.winner, PLAYER_BLACK)
        self.assertIsNotNone(self.record.end_time)

    def test_record_set_draw(self):
        """测试设置平局"""
        self.record.set_draw()
        self.assertEqual(self.record.winner, 0)
        self.assertIsNotNone(self.record.end_time)

    def test_record_to_dict(self):
        """测试记录转换为字典"""
        self.record.start()
        self.record.add_move(7, 7, PLAYER_BLACK)
        self.record.set_winner(PLAYER_BLACK)
        data = self.record.to_dict()
        self.assertIn("moves", data)
        self.assertIn("winner", data)
        self.assertEqual(data["total_moves"], 1)

    def test_record_reset(self):
        """测试重置记录"""
        self.record.start()
        self.record.add_move(7, 7, PLAYER_BLACK)
        self.record.reset()
        self.assertEqual(len(self.record.moves), 0)
        self.assertIsNone(self.record.start_time)


class TestRecordManager(unittest.TestCase):
    """记录管理器测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = RecordManager(self.temp_dir)

    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_record(self):
        """测试保存和加载记录"""
        record = GameRecord()
        record.start()
        record.add_move(7, 7, PLAYER_BLACK)
        record.set_winner(PLAYER_BLACK)

        filepath = self.manager.save_record(record)
        self.assertTrue(os.path.exists(filepath))

        loaded = self.manager.load_record(os.path.basename(filepath))
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.winner, PLAYER_BLACK)
        self.assertEqual(len(loaded.moves), 1)

    def test_list_records(self):
        """测试列出记录"""
        record = GameRecord()
        record.start()
        record.set_winner(PLAYER_BLACK)
        self.manager.save_record(record)

        records = self.manager.list_records()
        self.assertEqual(len(records), 1)

    def test_delete_record(self):
        """测试删除记录"""
        record = GameRecord()
        record.start()
        record.set_winner(PLAYER_BLACK)
        filepath = self.manager.save_record(record)
        filename = os.path.basename(filepath)

        self.assertTrue(self.manager.delete_record(filename))
        records = self.manager.list_records()
        self.assertEqual(len(records), 0)


if __name__ == "__main__":
    unittest.main()