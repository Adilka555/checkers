import pygame
from checks import checker
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
GRAY = (192, 192, 192)
MAX_ROW = 7
MAX_COL = 7


class Board:
    def __init__(self):
        self.board = []
        self.create_bord()
        self.all_counter()
        self.black_left = self.gray_left = 12
        self.black_q = 0
        self.gray_q = 0


    def create_bord(self):
        for row in range(8):
            nul = []
            for col in range(8):
                nul.append(0)
            self.board.append(nul)
        for row in range(8):
            for col in range(8):
                if col%2 == (row + 1)%2:
                    if row < 3:
                        self.board[row][col] = checker(row, col, GRAY)
                    elif row > 4:
                        self.board[row][col] = checker(row, col, BLACK)
                    else:
                        self.board[row][col] = 0
                else:
                    self.board[row][col] = 0
        # self.board[5][2] = checker(5, 2, BLACK)
        # self.board[5][2].is_q = True
        # self.board[3][4] = checker(3, 4, GRAY)
        # self.board[6][3] = checker(6, 3, GRAY)
        # self.board[6][5] = checker(6, 5, GRAY)
        # self.board[1][4] = checker(1, 4, GRAY)
        # self.board[3][6] = checker(3, 6, GRAY)


    def winner(self):
        if self.black_left <= 0 and self.black_q <= 0:
            return BLACK
        elif self.gray_left <= 0 and self.gray_q <= 0:
            return GRAY

        return None


    def draw_squares(self, win):
        win.fill(BROWN)
        for row in range(800):
            for col in range(row % 2, 800, 2):
                pygame.draw.rect(win, WHITE, (row*100, col *100, 100, 100))

    def draw_all(self, win):
        self.draw_squares(win)
        for row in range(8):
            for col in range(8):
                checker = self.board[row][col]
                if checker != 0:
                    checker.draw(win)


    def move(self, checker, row, col):
            self.board[checker.pos_row][checker.pos_col], self.board[row][col] = self.board[row][col], self.board[checker.pos_row][checker.pos_col]
            checker.pos_row = row
            checker.pos_col = col
            checker.move(row, col)
            if checker.color == BLACK and row == 0:
                checker.make_king()
                self.black_q+=1
            if checker.color == GRAY and row == MAX_ROW:
                checker.make_king()
                self.gray_q+=1


    def get_checker(self, row, col):
        return self.board[row][col]

    def put_checker(self, row, col, color):
        self.board[row][col] = checker(row, col, color)

    def remove_checker(self, row, col):
        # if self.board[row][col].color == GRAY:
        #     self.gray_left-=1
        # if self.board[row][col].color == BLACK:
        #     self.black_left-=1
        self.board[row][col] = 0


    def remove(self, pieces):
        for piece in pieces:
            if self.board[piece[0]][piece[1]].color == GRAY:
                self.gray_left-=1
            if self.board[piece[0]][piece[1]].color == BLACK:
                self.black_left-=1
            if self.board[piece[0]][piece[1]].color == GRAY and self.board[piece[0]][piece[1]].is_q == True :
                self.gray_left-=1
                self.gray_q-=1
            if self.board[piece[0]][piece[1]].color == BLACK and self.board[piece[0]][piece[1]].is_q == True :
                self.black_left-=1
                self.black_q-=1
            self.board[piece[0]][piece[1]] = 0

    def get_valid_moves(self, checker):
        moves = {}
        if checker.color == GRAY:
            moves = self.check_all_for_eat_gray(checker)
        if checker.color == BLACK:
            moves = self.check_all_for_eat_black(checker)
        return moves

    def check_all_for_eat_black(self, checker):
        flag = True
        moves = {}
        for row in range(MAX_ROW + 1):
            for col in range(MAX_COL + 1):
                if self.board[row][col]!= 0 and self.get_checker(row, col).color == BLACK:
                    if self.analyze_black_1(self.get_checker(row, col), moves)!= {}:
                        moves = self.analyze_black_1(self.get_checker(row, col), moves)
                        flag = False
        if flag == True:
            moves = self.analyze_black_2(checker, moves)
            return moves
        else:
            moves_for_checker = {}
            moves_for_checker = self.analyze_black_1(checker, moves_for_checker)
            res = moves.keys() & moves_for_checker.keys()
            dict3 = {}
            for i in res:
                dict3[i] = moves_for_checker[i]
            moves = dict3
            buffer = {}
            flag_q = False
            if checker.is_q == True:
                flag_q = True
            for m in moves.keys():
                buffer.update(self.recursive_check_black(m, checker.color, moves[m], flag_q))
            moves = buffer
        return moves

    def recursive_check_black(self, move, ch_color, key_value, flag_q):
        if move[0] == 0:
            flag_q = True
        self.put_checker(move[0], move[1], color = ch_color)
        self.board[move[0]][move[1]].is_q = flag_q
        new_moves = {}
        if self.analyze_black_1(self.get_checker(move[0], move[1]), new_moves):
            rec = {}
            flag = False
            for m in new_moves:
                if new_moves[m][0] not in key_value:
                    flag = True
                    new_moves[m].extend(key_value)
                    rec.update(self.recursive_check_black(m, ch_color, new_moves[m], flag_q))

            if not flag:
                self.remove_checker(move[0], move[1])
                dict = {}
                dict.update({move: key_value})
                return dict
        else:
            self.remove_checker(move[0], move[1])
            dict = {}
            dict.update({move: key_value})
            return dict
        self.remove_checker(move[0], move[1])
        return rec


    def recursive_check_gray(self, move, ch_color, key_value, flag_q = False):
        if move[0] == 0:
            flag_q = True
        self.put_checker(move[0], move[1], color = ch_color)
        self.board[move[0]][move[1]].is_q = flag_q
        new_moves = {}
        if self.analyze_gray_1(self.get_checker(move[0], move[1]), new_moves):
            rec = {}
            flag = False
            for m in new_moves:
                if new_moves[m][0] not in key_value:
                    flag = True
                    new_moves[m].extend(key_value)
                    rec.update(self.recursive_check_black(m, ch_color, new_moves[m], flag_q))
            if not flag:
                self.remove_checker(move[0], move[1])
                dict = {}
                dict.update({move: key_value})
                return dict
        else:
            self.remove_checker(move[0], move[1])
            dict = {}
            dict.update({move: key_value})
            return dict
        self.remove_checker(move[0], move[1])
        return rec

    def check_all_for_eat_gray(self, checker):
        flag = True
        moves = {}
        for row in range(MAX_ROW + 1):
            for col in range(MAX_COL + 1):
                if self.board[row][col]!= 0 and self.get_checker(row, col).color == GRAY:
                    if self.analyze_gray_1(self.get_checker(row, col), moves)!= {}:
                        move = self.analyze_gray_1(self.get_checker(row, col), moves)
                        flag = False
        if flag == True:
            self.analyze_gray_2(checker, moves)
            moves = self.analyze_gray_2(checker, moves)
            return moves
        else:
            moves_for_checker = {}
            self.analyze_gray_1(checker, moves_for_checker)
            res = moves.keys() & moves_for_checker.keys()
            dict3 = {}
            for i in res:
                dict3[i] = moves_for_checker[i]
            moves = dict3
            buffer = {}
            flag_q = False
            if checker.is_q == True:
                flag_q = True
            for m in moves.keys():
                buffer.update(self.recursive_check_gray(m, checker.color, moves[m], flag_q))
            moves = buffer
        return moves


    def analyze_black_1(self, checker, moves):
        r = checker.pos_row
        c = checker.pos_col
        c_start = c - 1
        c_stop = c + 2
        r_start = r + 1
        r_stop = r - 2
        if c == 0:
            c_start = c
        if c == 7:
            c_stop = c + 1
        if r == 7:
            r_start = r
        if r == 0:
            r_stop = r - 1
        if checker.is_q == False:
            buffer = self.boundaries_black(checker, r_start, r_stop, c_start, c_stop, moves)
        if checker.is_q:
            c_start = 0
            c_stop = MAX_COL + 1
            r_start = 0
            r_stop = MAX_ROW + 1
            buffer2 = self.boundaries_q(checker, r_start, r_stop, c_start, c_stop, moves)
        return moves

    def analyze_black_2(self, checker, moves):
        r = checker.pos_row
        c = checker.pos_col
        c_start = c - 1
        c_stop = c + 2
        r_start = r + 1
        r_stop = r - 2
        if c == 0:
            c_start = c
        if c == 7:
            c_stop = c + 1
        if r == 7:
            r_start = r
        if r == 0:
            r_stop = r - 1
        if checker.is_q == False:
            for row in range(r_start, r_stop, -1):
                for col in range(c_start, c_stop, 1):
                    if self.get_checker(row, col) == 0 and (row + col)%2 != 0 and r > row:
                        moves.update({(row, col) : []})
        if checker.is_q:
            self.boundaries_q_2(checker, moves)
        return moves

    def boundaries_black(self, checker ,r_start, r_stop, c_start, c_stop, moves):
        r = checker.pos_row
        c = checker.pos_col
        for row in range(r_start, r_stop, -1):
            for col in range(c_start, c_stop, 1):
                if row!= r and col!= c and self.board[row][col]!= 0 and self.get_checker(row, col).color!= checker.color:
                    if (row + (row - r)) <= MAX_ROW and (col + (col - c)) <= MAX_COL:
                        if  (row + (row - r)) >= 0 and (col + (col - c)) >= 0:
                            if self.board[row + (row - r)][col + (col - c)] == 0:
                                skipped_r_c = []
                                skipped = []
                                skipped_r_c.append(row)
                                skipped_r_c.append(col)
                                skipped.append(skipped_r_c)
                                moves.update({(row + (row - r), col + (col - c)) : skipped})
        return moves

    def analyze_gray_1(self, checker, moves):
        r = checker.pos_row
        c = checker.pos_col
        c_start = c - 1
        c_stop = c + 2
        r_start = r - 1
        r_stop = r + 2
        if c == 0:
            c_start = c
        if c == 7:
            c_stop = c + 1
        if r == 7:
            r_stop = r + 1
        if r == 0:
            r_start = r
        if checker.is_q == False:
            self.boundaries_gray(checker, r_start, r_stop, c_start, c_stop, moves)
        if checker.is_q:
            c_start = 0
            c_stop = MAX_COL + 1
            r_start = 0
            r_stop = MAX_ROW + 1
            self.boundaries_q(checker, r_start, r_stop, c_start, c_stop, moves)
        return moves

    def boundaries_gray(self, checker ,r_start, r_stop, c_start, c_stop, moves):
        r = checker.pos_row
        c = checker.pos_col
        for row in range(r_start, r_stop, 1):
            for col in range(c_start, c_stop, 1):
                if row!= r and col!= c and self.board[row][col]!= 0 and self.get_checker(row, col).color!= checker.color:
                    if (row + (row - r)) <= MAX_ROW and (col + (col - c)) <= MAX_COL:
                        if  (row + (row - r)) >= 0 and (col + (col - c)) >= 0:
                            if self.board[row + (row - r)][col + (col - c)] == 0:
                                skipped_r_c = []
                                skipped = []
                                skipped_r_c.append(row)
                                skipped_r_c.append(col)
                                skipped.append(skipped_r_c)
                                moves.update({(row + (row - r), col + (col - c)) : skipped})
        return moves

    def boundaries_q(self, checker ,r_start, r_stop, c_start, c_stop, moves):
        r = checker.pos_row
        c = checker.pos_col
        buffer = []
        buffer = self.seek_diagonal_friendly(r_start, r_stop, c_start, c_stop, checker, buffer)
        for row in range(r_start, r_stop, 1):
            for col in range(c_start, c_stop, 1):
                if abs(row - r) == abs(col - c):
                    if row!= r and col!= c and self.board[row][col]!= 0 and self.get_checker(row, col).color!= checker.color:
                        if row - r > 0 and col - c > 0 and (self.board[row - 1][col - 1] == 0 or self.board[row - 1][col - 1] == checker):
                            if row + 1 <= MAX_ROW and col + 1 <= MAX_COL and self.board[row + 1][col + 1] == 0:
                                if self.diagonal_check(buffer, row, col, 1, checker) == False:
                                    self.filling_dict(row, col, row + 1, col + 1 ,moves)

                        if row - r < 0 and col - c < 0 and (self.board[row + 1][col + 1] == 0 or self.board[row + 1][col + 1] == checker):
                            if row - 1 >= 0 and col - 1 >= 0 and self.board[row -1][col - 1] == 0:
                                if self.diagonal_check(buffer, row, col, 2, checker) == False:
                                    self.filling_dict(row, col, row - 1, col - 1 ,moves)

                        if row - r > 0 and col - c < 0 and (self.board[row - 1][col + 1] == 0 or self.board[row - 1][col + 1] == checker):
                            if row + 1 <= MAX_ROW  and col - 1 >= 0 and self.board[row + 1][col - 1] == 0:
                                if self.diagonal_check(buffer, row, col, 3, checker) == False:
                                    self.filling_dict(row, col, row + 1, col - 1 ,moves)

                        if row - r < 0 and col - c > 0 and (self.board[row + 1][col - 1] == 0 or self.board[row + 1][col - 1] == checker):
                            if row - 1 >= 0 and col + 1 <= MAX_COL and self.board[row - 1][col + 1] == 0:
                                if self.diagonal_check(buffer, row, col, 4, checker) == False:
                                    self.filling_dict(row, col, row - 1, col + 1 ,moves)
        # print("moves:", moves)
        return moves

    def seek_diagonal_friendly(self, r_start, r_stop, c_start, c_stop, checker, buffer):
        r = checker.pos_row
        c = checker.pos_col
        for row in range(r_start, r_stop, 1):
            for col in range(c_start, c_stop, 1):
                if abs(row - r) == abs(col - c):
                    if row!= r and col!= c and self.board[row][col]!= 0 and self.get_checker(row, col).color == checker.color:
                        buffer_for_r_c = []
                        buffer_for_r_c.append(row)
                        buffer_for_r_c.append(col)
                        buffer.append(buffer_for_r_c)
        return buffer

    def diagonal_check(self, buffer, row, col, option, checker):
        r = checker.pos_row
        c = checker.pos_col
        for i in buffer:
            if abs(i[0] - row) == abs(i[1] - col):
                if option == 1:
                    if row - i[0] > 0 and col - i[1] > 0 and i[0] > r and i[1] > c:
                        return True
                if option == 2:
                    if row - i[0] < 0 and col - i[1] < 0 and i[0] < r and i[1] < c:
                        return True
                if option == 3:
                    if row - i[0] > 0 and col - i[1] < 0 and i[0] > r and i[1] < c:
                        return True
                if option == 4:
                    if row - i[0] < 0 and col - i[1] > 0 and i[0] < r and i[1] > c:
                        return True
        return False



    def filling_dict(self, row, col, step_row, step_col ,moves):
         skipped_r_c = []
         skipped = []
         skipped_r_c.append(row)
         skipped_r_c.append(col)
         skipped.append(skipped_r_c)
         moves.update({(step_row, step_col) : skipped})



    def boundaries_q_2(self, checker ,moves):
        # print("moves", moves)
        r = checker.pos_row
        c = checker.pos_col
        self.boundaries_q_2_moves(r-1, -1, c-1, -1, -1, -1, moves, checker)
        self.boundaries_q_2_moves(r+1, MAX_ROW+1, c+1, MAX_COL+1, 1, 1, moves, checker)
        self.boundaries_q_2_moves(r+1, MAX_ROW+1, c-1, -1, 1, -1, moves, checker)
        self.boundaries_q_2_moves(r-1, -1, c+1, MAX_COL+1, -1, 1, moves, checker)
        return moves

    def boundaries_q_2_moves(self, r_start, r_stop, c_start, c_stop ,r_step, c_step, moves, checker):
        flag = False
        r = checker.pos_row
        c = checker.pos_col
        for row in range(r_start, r_stop, r_step):
            for col in range(c_start, c_stop, c_step):
                if abs(row - r) == abs(col - c):
                    if self.board[row][col] == 0:
                        moves.update({(row, col) : []})
                    if self.board[row][col]!= 0:
                        flag = True
                        break
            if flag:
                break


    def analyze_gray_2(self, checker, moves):
        r = checker.pos_row
        c = checker.pos_col
        c_start = c - 1
        c_stop = c + 2
        r_start = r - 1
        r_stop = r + 2
        if c == 0:
            c_start = c
        if c == 7:
            c_stop = c + 1
        if r == 7:
            r_stop = r + 1
        if r == 0:
            r_start = r
        for row in range(r_start, r_stop, 1):
            for col in range(c_start, c_stop, 1):
                if self.get_checker(row, col) == 0 and (row + col)%2!= 0 and row > r:
                    moves.update({(row, col) : []})
        if checker.is_q:
            self.boundaries_q_2(checker, moves)
        return moves


    def evaluate(self):
        # self.all_counter()
        # print("cnt : ",self.gray_left, self.black_left, self.gray_q, self.black_q)
        return self.gray_left - self.black_left + (self.gray_q * 0.5 - self.black_q * 0.5)

    def all_counter(self):
        black_counter = 0
        gray_counter = 0
        black_q_cnt = 0
        gray_q_cnt = 0
        for row in range(MAX_ROW+1):
            for col in range(MAX_COL+1):
                if self.board[row][col]!= 0:
                    if self.get_checker(row, col).color == BLACK and self.get_checker(row, col).is_q == False:
                        black_counter += 1
                    if self.get_checker(row, col).color == GRAY and self.get_checker(row, col).is_q == False:
                        gray_counter += 1
                    if self.get_checker(row, col).color == BLACK and self.get_checker(row, col).is_q == True:
                        black_q_cnt+= 1
                    if self.get_checker(row, col).color == GRAY and self.get_checker(row, col).is_q == True:
                        gray_q_cnt += 1
        self.black_left = black_counter
        self.gray_left = gray_counter
        self.black_q = black_q_cnt
        self.gray_q = gray_q_cnt

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
