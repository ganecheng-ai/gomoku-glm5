"""
AI玩家模块
实现基于评分策略的五子棋AI
"""

import random
from .constants import PLAYER_BLACK, PLAYER_WHITE, BOARD_SIZE


class AIPlayer:
    """AI玩家类"""

    # 棋型评分
    SCORE_FIVE = 100000       # 连五
    SCORE_LIVE_FOUR = 10000   # 活四
    SCORE_RUSH_FOUR = 1000    # 冲四
    SCORE_LIVE_THREE = 1000   # 活三
    SCORE_SLEEP_THREE = 100   # 眠三
    SCORE_LIVE_TWO = 100      # 活二
    SCORE_SLEEP_TWO = 10      # 眠二

    def __init__(self, player_type, difficulty=2):
        """
        初始化AI玩家
        :param player_type: 玩家类型 (PLAYER_BLACK 或 PLAYER_WHITE)
        :param difficulty: 难度 (1-简单, 2-中等, 3-困难)
        """
        self.player_type = player_type
        self.difficulty = difficulty
        self.opponent = PLAYER_WHITE if player_type == PLAYER_BLACK else PLAYER_BLACK

    def get_best_move(self, board):
        """
        获取最佳落子位置
        :param board: 棋盘对象
        :return: (row, col) 最佳位置
        """
        # 获取所有可用的位置
        candidates = self._get_candidate_moves(board)

        if not candidates:
            # 如果没有候选位置，下在中心
            return BOARD_SIZE // 2, BOARD_SIZE // 2

        # 评估每个位置
        best_score = -float('inf')
        best_moves = []

        for row, col in candidates:
            # 计算进攻分数
            attack_score = self._evaluate_position(board, row, col, self.player_type)
            # 计算防守分数
            defense_score = self._evaluate_position(board, row, col, self.opponent)

            # 根据难度调整策略
            if self.difficulty == 1:
                # 简单模式：随机性更高
                score = attack_score * 0.6 + defense_score * 0.4 + random.randint(0, 100)
            elif self.difficulty == 2:
                # 中等模式：平衡进攻和防守
                score = max(attack_score, defense_score * 0.9)
            else:
                # 困难模式：更注重进攻，同时考虑防守
                score = max(attack_score, defense_score * 1.1)

            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))

        # 从最佳位置中随机选择一个
        return random.choice(best_moves)

    def _get_candidate_moves(self, board):
        """
        获取候选落子位置
        只考虑已有棋子周围的位置，提高效率
        """
        candidates = set()
        has_pieces = False

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board.grid[row][col] != 0:
                    has_pieces = True
                    # 添加周围的空位作为候选
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            r, c = row + dr, col + dc
                            if (board.is_valid_position(r, c) and
                                board.is_empty(r, c)):
                                candidates.add((r, c))

        if not has_pieces:
            # 如果棋盘为空，下在中心
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

        return list(candidates)

    def _evaluate_position(self, board, row, col, player):
        """
        评估某个位置的分数
        """
        # 临时放置棋子
        board.grid[row][col] = player

        score = 0

        # 检查四个方向
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            # 计算该方向的分数
            line_score = self._evaluate_line(board, row, col, dr, dc, player)
            score += line_score

        # 移除临时棋子
        board.grid[row][col] = 0

        return score

    def _evaluate_line(self, board, row, col, dr, dc, player):
        """
        评估某个方向的棋型分数
        """
        opponent = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK

        # 计算连续棋子数
        count = 1
        block = 0
        empty = 0

        # 正方向
        r, c = row + dr, col + dc
        while board.is_valid_position(r, c):
            if board.grid[r][c] == player:
                count += 1
            elif board.grid[r][c] == opponent:
                block += 1
                break
            else:
                empty += 1
                break
            r += dr
            c += dc

        # 如果超出边界
        if not board.is_valid_position(r, c):
            block += 1

        # 反方向
        r, c = row - dr, col - dc
        while board.is_valid_position(r, c):
            if board.grid[r][c] == player:
                count += 1
            elif board.grid[r][c] == opponent:
                block += 1
                break
            else:
                empty += 1
                break
            r -= dr
            c -= dc

        # 如果超出边界
        if not board.is_valid_position(r, c):
            block += 1

        # 根据棋型返回分数
        return self._get_shape_score(count, block, empty)

    def _get_shape_score(self, count, block, empty):
        """
        根据棋型返回分数
        """
        if count >= 5:
            return self.SCORE_FIVE

        if block >= 2:
            # 两端都被堵死
            return 0

        if count == 4:
            if block == 0:
                return self.SCORE_LIVE_FOUR  # 活四
            else:
                return self.SCORE_RUSH_FOUR  # 冲四

        if count == 3:
            if block == 0:
                return self.SCORE_LIVE_THREE  # 活三
            else:
                return self.SCORE_SLEEP_THREE  # 眠三

        if count == 2:
            if block == 0:
                return self.SCORE_LIVE_TWO  # 活二
            else:
                return self.SCORE_SLEEP_TWO  # 眠二

        if count == 1:
            return 1

        return 0

    def get_piece_name(self):
        """获取棋子名称"""
        return "AI黑棋" if self.player_type == PLAYER_BLACK else "AI白棋"