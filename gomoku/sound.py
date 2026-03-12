"""
音效管理模块
"""

import os
import pygame
from .constants import SOUND_ENABLED, SOUND_VOLUME


class SoundManager:
    """音效管理器"""

    def __init__(self):
        """初始化音效管理器"""
        self.enabled = SOUND_ENABLED
        self.volume = SOUND_VOLUME
        self.sounds = {}
        self._init_sounds()

    def _init_sounds(self):
        """初始化音效"""
        if not self.enabled:
            return

        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return

        # 尝试加载音效文件
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds')

        sound_files = {
            "place": "place.wav",      # 落子音效
            "win": "win.wav",          # 获胜音效
            "draw": "draw.wav",        # 平局音效
            "button": "button.wav",    # 按钮音效
            "undo": "undo.wav",        # 悔棋音效
        }

        for name, filename in sound_files.items():
            filepath = os.path.join(sound_dir, filename)
            if os.path.exists(filepath):
                try:
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(self.volume)
                    self.sounds[name] = sound
                except pygame.error:
                    pass

    def play(self, sound_name):
        """播放音效"""
        if not self.enabled:
            return

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def set_volume(self, volume):
        """设置音量"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def toggle(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        return self.enabled

    def play_place(self):
        """播放落子音效"""
        self.play("place")

    def play_win(self):
        """播放获胜音效"""
        self.play("win")

    def play_draw(self):
        """播放平局音效"""
        self.play("draw")

    def play_button(self):
        """播放按钮音效"""
        self.play("button")

    def play_undo(self):
        """播放悔棋音效"""
        self.play("undo")