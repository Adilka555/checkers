from board import Board
import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GRAY = (192, 192, 192)

class Game:
    def __init__(self, win):
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def update(self):
        self.board.all_counter()
        # print("all_counter", self.board.black_left, self.board.gray_left, self)
        self.board.draw_all(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col):

        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        checker = self.board.get_checker(row, col)
        if checker!= 0 and checker.color == self.turn:
            self.selected = checker
            self.valid_moves = self.board.get_valid_moves(checker)
            # print("self.valid_moves", self.valid_moves)
            return True

        return False

    def _move(self, row, col):
        checker = self.board.get_checker(row, col)
        if self.selected and checker == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                for cords in skipped:
                    self.board.remove_checker(cords[0],cords[1])
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = GRAY
        else:
            self.turn = BLACK

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * 100 + 100//2, row * 100 + 100//2), 15)


    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
