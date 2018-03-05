from Board import Board
from Solverer import Solverer
from KakuroExceptions import *

import argparse


def parser_args():
    parser = argparse.ArgumentParser(description="Решает головоломку Какуро")
    parser.add_argument('inFilename', type=str, help='Имя входного файла с головоломкой')
    parser.add_argument('-o', '--outFilename', type=str, action='store', default=None,
                        help='Имя выходного файла с головоломкой')
    parser.add_argument('-N', '--countSolve', type=int, action='store', default=1,
                        help='Количество решений (по умолчанию 1)')

    return parser.parse_args()


def main():
    args = parser_args()
    filename = args.inFilename
    try:
        board = Board(filename)
        solver = Solverer(board.game_desk)
        solver.get_full_solve_game(solver.board)
        results = solver.returner()
        Solverer.print_solve(results, args.countSolve, args.outFilename)
    except NotCorrectValuePuzzle:
        pass
    except FileIsOut:
        pass


if __name__ == '__main__':
    main()
