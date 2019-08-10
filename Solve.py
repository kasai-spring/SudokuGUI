from collections import deque


class Solve:  # 解く
    puzzle = []

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.integrity_check()

    def integrity_check(self):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                count = 0
                check_value = self.puzzle[i][j]
                if check_value == 0:
                    continue
                for k in range(9):  # 横
                    if self.puzzle[i][k] == check_value:
                        count += 1
                if count >= 2:
                    raise ArithmeticError("縦:" + str(i+1) + "マス目 横:" + str(j+1) + str("マス目"))
                count = 0
                for k in range(9):  # 縦
                    if self.puzzle[k][j] == check_value:
                        count += 1
                if count >= 2:
                    raise ArithmeticError("縦:" + str(i+1) + "マス目 横:" + str(j+1) + str("マス目"))
                count = 0
                for k in range(3):  # 箱
                    for l in range(3):
                        if self.puzzle[int(i / 3) * 3 + k][int(j / 3) * 3 + l] == check_value:
                            count += 1
                if count >= 2:
                    raise ArithmeticError("縦:" + str(i+1) + "マス目 横:" + str(j+1) + str("マス目"))

    def solve(self):
        answer = []
        q = deque([])
        q.append(self.puzzle)
        while len(q) > 0:
            break_turn = False
            now_q = q.pop()  # 深さ優先探索
            for i in range(len(now_q)):
                for j in range(len(now_q[i])):
                    if now_q[i][j] != 0:
                        continue
                    can_not_input = []
                    can_not_input.extend(self.check_x(i, now_q))
                    can_not_input.extend(self.check_y(j, now_q))
                    can_not_input.extend(self.check_box(i, j, now_q))
                    set(can_not_input)
                    can_input = [i for i in range(1, 10) if i not in can_not_input]

                    for k in can_input:
                        input_q = [[x for x in now_q[y]] for y in range(len(now_q))]
                        input_q[i][j] = k
                        q.append(input_q)
                    else:
                        break_turn = True
                        break

                if break_turn:
                    break
            else:  # 全部0以外だった場合
                if not answer:  # はじめての解だった場合
                    answer = now_q
                else:
                    return True, answer  # 答えが複数あるか、答え

        return False, answer  # 答えが複数あるか、答え

    @staticmethod
    def check_x(x, puzzle):  # 横探索
        can_not_input_x = []
        for i in range(len(puzzle[x])):
            if puzzle[x][i] != 0:
                can_not_input_x.append(puzzle[x][i])

        return can_not_input_x

    @staticmethod
    def check_y(y, puzzle):  # 縦探索
        can_not_input_y = []
        for i in range(len(puzzle[y])):
            if puzzle[i][y] != 0:
                can_not_input_y.append(puzzle[i][y])
        return can_not_input_y

    @staticmethod
    def check_box(x, y, puzzle):
        can_not_input_box = []
        for i in range(3):
            for j in range(3):
                if puzzle[int(x / 3) * 3 + i][int(y / 3) * 3 + j] != 0:
                    can_not_input_box.append(puzzle[int(x / 3) * 3 + i][int(y / 3) * 3 + j])
        return can_not_input_box
