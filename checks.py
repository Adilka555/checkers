import pygame
CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (44, 25))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class checker:
    def __init__(self, pos_row, pos_col, color):
        self.pos_row = pos_row
        self.pos_col = pos_col
        self.white_q = 0
        self.black_q = 0
        self.pos_x = 100 * pos_col + 50
        self.pos_y = 100 * pos_row + 50
        self.color = color
        self.is_q = False

    def draw(self, win):
        radius = 45
        # pygame.draw.circle(win, BLACK, (self.pos_x, self.pos_y), radius)
        pygame.draw.circle(win, self.color, (self.pos_x, self.pos_y), radius)


        if self.is_q:
            win.blit(CROWN, (self.pos_x - CROWN.get_width()//2, self.pos_y - CROWN.get_height()//2))


    def make_king(self):
        self.is_q = True


    def move(self, row, col):
        self.pos_x = 100 * col + 50
        self.pos_y = 100 * row + 50
