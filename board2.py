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
        self.black_q = 0
        self.gray_q = 0

    def create_bord(self):
        for row in range(8):
            nul = []
            for col in range(8):
                nul.append(0)
            self.board.append(nul)
        # for row in range(8):
        #     for col in range(8):
        #         if col%2 == (row + 1)%2:
        #             if row < 3:
        #                 self.board[row][col] = checker(row, col, GRAY)
        #             elif row > 4:
        #                 self.board[row][col] = checker(row, col, BLACK)
        #             else:
        #                 self.board[row][col] = 0
        #         else:
        #             self.board[row][col] = 0
        self.board[7][2] = checker(7 , 2, GRAY)
        self.board[7][2].make_king()
        self.board[5][4] = checker(5 , 4, BLACK)
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
            if row == 7 or row == 0:
                checker.make_king()
                if checker.color == GRAY:
                    self.gray_q += 1
                else:
                    self.black_q += 1

    def get_checker(self, row, col):
        return self.board[row][col]

    def put_checker(self, row, col, color):
        self.board[row][col] = checker(row, col, color)

    def remove_checker(self, row, col):
        self.board[row][col] = 0

    def get_valid_moves(self, checker):
        # print("row, col", checker.pos_row, checker.pos_col)
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
                        flag = False


        if  flag == True:
            self.analyze_black_2(checker, moves)
            return moves

        else:
            moves_for_checker = {}
            self.analyze_black_1(checker, moves_for_checker)
            res = moves.keys() & moves_for_checker.keys()
            dict3 = {}
            for i in res:
                dict3[i] = moves_for_checker[i]
            moves = dict3
            buffer = {}
            for m in moves.keys():
                buffer.update(self.recursive_check(m, checker.color, moves[m]))
            moves = buffer
            return moves

    def recursive_check(self, move, ch_color, key_value):
        self.put_checker(move[0], move[1], color = ch_color)
        new_moves = {}
        if self.analyze_black_1(self.get_checker(move[0], move[1]), new_moves):
            rec = {}
            for m in new_moves:
                key_value.extend(new_moves[m])
                rec.update(self.recursive_check(m, ch_color, key_value))
            result = rec
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
                        flag = False

        if flag == True:
            self.analyze_gray_2(checker, moves)
            return moves
        else:
            print("in else")
            moves_for_checker = {}
            self.analyze_gray_1(checker, moves_for_checker)
            res = moves.keys() & moves_for_checker.keys()
            dict3 = {}
            for i in res:
                dict3[i] = moves_for_checker[i]
            moves = dict3
            buffer = {}
            for m in moves.keys():
                buffer.update(self.recursive_check(m, checker.color, moves[m]))
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
        if checker.is_q:
            c_start = 0
            c_stop = MAX_COL
            r_start = MAX_ROW
            r_stop = 0
        for row in range(r_start, r_stop, -1):
            for col in range(c_start, c_stop, 1):
                if (row , col != r , c) and self.board[row][col]!= 0 and self.get_checker(row, col).color!= checker.color:
                    if (row + (row - r)) <= MAX_ROW and (col + (col - c)) <= MAX_COL:
                        if (row + (row - r)) >= 0 and (col + (col - c)) >= 0:
                            if self.board[row + (row - r)][col + (col - c)] == 0:
                                skipped_r_c = []
                                skipped = []
                                skipped_r_c.append(row)
                                skipped_r_c.append(col)
                                skipped.append(skipped_r_c)
                                moves.update({(row + (row - r), col + (col - c)) : skipped})
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
        for row in range(r_start, r_stop, -1):
            for col in range(c_start, c_stop, 1):
                if self.get_checker(row, col) == 0 and (row + col)%2 != 0 and r > row:
                    moves.update({(row, col) : []})
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
        print("is_q", checker.is_q)
        if checker.is_q:
            print("DAMKA")
            c_start = 0
            c_stop = MAX_COL
            r_start = 0
            r_stop = MAX_ROW
        for row in range(r_start, r_stop, 1):
            for col in range(c_start, c_stop, 1):
                if (row , col != r , c) and self.board[row][col]!= 0 and self.get_checker(row, col).color!= checker.color:
                    if (row + (row - r)) <= MAX_ROW and (col + (col - c)) <= MAX_COL:
                        print("IN IF")
                        if  (row + (row - r)) >= 0 and (col + (col - c)) >= 0:
                            if self.board[row + (row - r)][col + (col - c)] == 0:
                                print("ЭТИ УСЛОВИЯ")
                                skipped_r_c = []
                                skipped = []
                                skipped_r_c.append(row)
                                skipped_r_c.append(col)
                                skipped.append(skipped_r_c)
                                moves.update({(row + (row - r), col + (col - c)) : skipped})
        return moves


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

        return moves
