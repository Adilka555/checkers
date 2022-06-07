from copy import deepcopy
import pygame

BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
def minimax(position, depth, max_player, game ,alpha = float('-inf'), beta = float('inf')):
    if depth == 0 or position.winner()!= None:
        print("eval: ", position.evaluate())
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, GRAY, game):
            evaluation = minimax(move, depth-1, False, game ,alpha, beta)[0]
            # print("in if alpha , beta :", alpha, beta)
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, True, game ,alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_checker(piece.pos_row, piece.pos_col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            # print("new_b_ev",new_board.evaluate())
            moves.append(new_board)
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    # board.draw_all(game.win)
    # pygame.draw.circle(game.win, (0,255,0), (piece.pos_x, piece.pos_y), 50, 5)
    # game.draw_valid_moves(valid_moves.keys())
    # pygame.display.update()
    pygame.time.delay(0)
#
