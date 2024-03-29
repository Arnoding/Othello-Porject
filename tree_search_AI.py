import random


class AI(object):

    def __init__(self, level_ix=0):
        self.level = ['beginner', 'intermediate', 'advanced'][level_ix]
        '''Reference：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py'''
        self.board_weights = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]
        ]

    # evaluate
    def evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    score += self.board_weights[i][j]
                elif board[i][j] == uncolor:
                    score -= self.board_weights[i][j]
        return score

    # AI
    def brain(self, board, opponent, depth):
        if self.level == 'beginer':
            _, action = self.randomchoice(board)
        elif self.level == 'intermediate':
            _, action = self.minimax(board, opponent, depth)
        elif self.level == 'advanced':
            _, action = self.minimax_alpha_beta(board, opponent, depth)
        assert action is not None, 'action is None'
        return action

    # Random choice（from all legal actions）
    def randomchoice(self, board):
        color = self.color
        action_list = list(board.get_legal_actions(color))
        return None, random.choice(action_list)

    # MiniMax Tree Search
    def minimax(self, board, opfor, depth=4):  # 其中 opfor 是假想敌、陪练
        """ Reference：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py"""
        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax(board, self, depth - 1)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            if score > best_score:
                best_score = score
                best_action = action
        return best_score, best_action

    # alpha-beta pruning
    def minimax_alpha_beta(self, board, opfor, depth=8, my_best=-float('inf'), opp_best=float('inf')):
        '''参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py'''
        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = my_best
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子

            score, _ = opfor.minimax_alpha_beta(board, self, depth - 1, -opp_best, -best_score)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            if score > best_score:
                best_score = score
                best_action = action

            if best_score > opp_best:
                break

        return best_score, best_action
