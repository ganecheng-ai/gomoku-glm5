"""
游戏记录模块
"""

import os
import json
import time
from datetime import datetime
from .constants import RECORD_DIR, MAX_RECORDS, PLAYER_BLACK, PLAYER_WHITE


class GameRecord:
    """游戏记录类"""

    def __init__(self):
        """初始化游戏记录"""
        self.moves = []  # [(row, col, player, timestamp), ...]
        self.start_time = None
        self.end_time = None
        self.winner = None
        self.black_time = 0  # 黑棋总用时
        self.white_time = 0  # 白棋总用时
        self.last_move_time = None

    def start(self):
        """开始记录"""
        self.start_time = datetime.now()
        self.last_move_time = time.time()

    def add_move(self, row, col, player, elapsed_time=0):
        """添加一步棋"""
        move_time = time.time()
        elapsed = elapsed_time if elapsed_time > 0 else (move_time - self.last_move_time if self.last_move_time else 0)

        self.moves.append({
            "row": row,
            "col": col,
            "player": player,
            "timestamp": datetime.now().isoformat(),
            "elapsed": elapsed
        })

        # 更新玩家用时
        if player == PLAYER_BLACK:
            self.black_time += elapsed
        else:
            self.white_time += elapsed

        self.last_move_time = move_time

    def set_winner(self, winner):
        """设置获胜者"""
        self.winner = winner
        self.end_time = datetime.now()

    def set_draw(self):
        """设置平局"""
        self.winner = 0
        self.end_time = datetime.now()

    def to_dict(self):
        """转换为字典"""
        return {
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "winner": self.winner,
            "black_time": round(self.black_time, 2),
            "white_time": round(self.white_time, 2),
            "total_moves": len(self.moves),
            "moves": self.moves
        }

    def from_dict(self, data):
        """从字典加载"""
        self.start_time = datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None
        self.end_time = datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        self.winner = data.get("winner")
        self.black_time = data.get("black_time", 0)
        self.white_time = data.get("white_time", 0)
        self.moves = data.get("moves", [])
        return self

    def reset(self):
        """重置记录"""
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.winner = None
        self.black_time = 0
        self.white_time = 0
        self.last_move_time = None


class RecordManager:
    """记录管理器"""

    def __init__(self, record_dir=None):
        """初始化记录管理器"""
        self.record_dir = record_dir or RECORD_DIR
        self._ensure_dir()

    def _ensure_dir(self):
        """确保记录目录存在"""
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)

    def save_record(self, record, filename=None):
        """保存游戏记录"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"game_{timestamp}.json"

        filepath = os.path.join(self.record_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)

        # 清理旧记录
        self._cleanup_old_records()

        return filepath

    def load_record(self, filename):
        """加载游戏记录"""
        filepath = os.path.join(self.record_dir, filename)

        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        record = GameRecord()
        return record.from_dict(data)

    def list_records(self):
        """列出所有记录"""
        if not os.path.exists(self.record_dir):
            return []

        records = []
        for filename in os.listdir(self.record_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.record_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    records.append({
                        "filename": filename,
                        "start_time": data.get("start_time"),
                        "winner": data.get("winner"),
                        "total_moves": data.get("total_moves", 0)
                    })
                except (json.JSONDecodeError, IOError):
                    continue

        # 按时间倒序排列
        records.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        return records

    def delete_record(self, filename):
        """删除记录"""
        filepath = os.path.join(self.record_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def _cleanup_old_records(self):
        """清理旧记录"""
        records = self.list_records()
        while len(records) > MAX_RECORDS:
            oldest = records.pop()
            self.delete_record(oldest["filename"])

    def get_record_summary(self, record):
        """获取记录摘要"""
        winner_text = "平局"
        if record.winner == PLAYER_BLACK:
            winner_text = "黑棋胜"
        elif record.winner == PLAYER_WHITE:
            winner_text = "白棋胜"

        return {
            "winner": winner_text,
            "total_moves": len(record.moves),
            "black_time": round(record.black_time, 1),
            "white_time": round(record.white_time, 1),
            "duration": round(record.black_time + record.white_time, 1)
        }