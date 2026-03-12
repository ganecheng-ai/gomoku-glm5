"""
计时器模块
"""

import time
from .constants import TIMER_WARNING_THRESHOLD, TIMER_DANGER_THRESHOLD


class Timer:
    """计时器类"""

    def __init__(self, time_limit=0):
        """
        初始化计时器
        :param time_limit: 时间限制 (0表示无限制，单位：秒)
        """
        self.time_limit = time_limit
        self.elapsed_time = 0
        self.start_time = None
        self.is_running = False

    def start(self):
        """开始计时"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        """停止计时"""
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        """重置计时器"""
        self.elapsed_time = 0
        self.start_time = None
        self.is_running = False

    def get_time(self):
        """获取当前用时"""
        if self.is_running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def get_remaining_time(self):
        """获取剩余时间"""
        if self.time_limit == 0:
            return -1  # 无限制
        remaining = self.time_limit - self.get_time()
        return max(0, remaining)

    def is_time_up(self):
        """检查是否超时"""
        if self.time_limit == 0:
            return False
        return self.get_remaining_time() <= 0

    def get_status(self):
        """获取计时器状态 (用于显示颜色)"""
        remaining = self.get_remaining_time()
        if remaining < 0:  # 无限制
            return "normal"
        if remaining <= TIMER_DANGER_THRESHOLD:
            return "danger"
        if remaining <= TIMER_WARNING_THRESHOLD:
            return "warning"
        return "normal"

    def format_time(self, seconds=None):
        """格式化时间显示"""
        if seconds is None:
            seconds = self.get_time()

        if seconds < 0:
            return "--:--"

        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


class GameTimer:
    """游戏计时器 (管理双方计时)"""

    def __init__(self, time_limit=0):
        """
        初始化游戏计时器
        :param time_limit: 每方时间限制 (0表示无限制，单位：秒)
        """
        self.time_limit = time_limit
        self.black_timer = Timer(time_limit)
        self.white_timer = Timer(time_limit)
        self.current_is_black = True
        self.is_paused = True

    def start_turn(self, is_black):
        """开始回合"""
        self.current_is_black = is_black
        self.is_paused = False

        if is_black:
            self.black_timer.start()
            self.white_timer.stop()
        else:
            self.white_timer.start()
            self.black_timer.stop()

    def switch_turn(self):
        """切换回合"""
        # 停止当前计时器
        if self.current_is_black:
            self.black_timer.stop()
        else:
            self.white_timer.stop()

        # 切换并开始新计时器
        self.current_is_black = not self.current_is_black
        self.start_turn(self.current_is_black)

    def pause(self):
        """暂停计时"""
        if self.current_is_black:
            self.black_timer.stop()
        else:
            self.white_timer.stop()
        self.is_paused = True

    def resume(self):
        """恢复计时"""
        if self.current_is_black:
            self.black_timer.start()
        else:
            self.white_timer.start()
        self.is_paused = False

    def stop(self):
        """停止计时"""
        self.black_timer.stop()
        self.white_timer.stop()
        self.is_paused = True

    def reset(self):
        """重置计时器"""
        self.black_timer.reset()
        self.white_timer.reset()
        self.current_is_black = True
        self.is_paused = True

    def get_black_time(self):
        """获取黑棋用时"""
        return self.black_timer.get_time()

    def get_white_time(self):
        """获取白棋用时"""
        return self.white_timer.get_time()

    def get_current_time(self):
        """获取当前玩家用时"""
        if self.current_is_black:
            return self.get_black_time()
        return self.get_white_time()

    def is_time_up(self):
        """检查是否超时"""
        if self.current_is_black:
            return self.black_timer.is_time_up()
        return self.white_timer.is_time_up()

    def get_format_times(self):
        """获取格式化的时间显示"""
        return {
            "black": self.black_timer.format_time(),
            "white": self.white_timer.format_time(),
            "black_status": self.black_timer.get_status(),
            "white_status": self.white_timer.get_status()
        }