import pygame
from board import Board
from logic import Game
from checks import checker
from minimax import minimax

GRAY = (192, 192, 192)
BLACK = (0,0,0)

pygame.init()

gameScreen = pygame.display.set_mode((400,300))

size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Checkers")
gameScreen.fill((0,0,255))
pygame.display.flip()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // 100
    col = x // 100
    # print("row col", row, col)
    # pygame.draw.circle(screen, (0,255,0), (x, y), 100, 100)
    return row, col

def main():
    runGame = True
    clock = pygame.time.Clock()
    game = Game(screen)
    while runGame:
        clock.tick(15)

        if game.turn == GRAY:
            value, new_board = minimax(game.get_board(), 4, GRAY, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            runGame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: runGame = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                # pygame.draw.circle(game.win, (0,255,0), (200, 100), 50, 10)
                # print("row, col", row, col)



        game.update()
    pygame.quit()

main()
