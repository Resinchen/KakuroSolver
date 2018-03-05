from copy import deepcopy
from enum import Enum

import sys

from ValueBlock import ValueBlock
from SumBlock import SumBlock


class Axis(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Solverer:
    """Класс, решающий головоломку"""

    def __init__(self, board):
        self.board = board
        self.cache_boards = [self.board]
        self.solved = False

    def remove_used_values(self, block):
        """Удаляет использованные значения у собратьев по вертикали и горизонтали

        :param block: блок, значение которого нужно удалить
        :type block: ValueBlock

        """
        parent_v = block.parent_vertical
        parent_h = block.parent_horizontal

        block.possible_values = [block.current_value]

        for child in parent_h.horizontal_child:
            if block.current_value in child.possible_values:
                child.possible_values.remove(block.current_value)

        for child in parent_v.vertical_child:
            if block.current_value in child.possible_values:
                child.possible_values.remove(block.current_value)

    @staticmethod
    def print_solve(boards, count, outfilename=None):
        """Печатает решение"""
        if count > len(boards):
            print('Количество решений меньше заданного')
            sys.exit(4)
        if outfilename is None:
            # for board in boards[:count]:
            for i in range(count):
                for row in boards[i]:
                    for block in row:
                        print(block, end=' ')
                    print()
                print()
        else:
            string = ''
            for board in boards[:count]:
                for row in board:
                    string += ' '.join([str(i) for i in row]) + '\n'
                string += '\n'

            with open(outfilename, 'w') as f:
                f.write(string)

    def simple_step_solve_game(self, board):
        """Совершает минимальный шаг для решения головоломки"""
        for x in range(len(board)):
            for y in range(len(board[0])):
                block = board[x][y]
                if isinstance(block, ValueBlock):
                    if len(block.possible_values) == 1:
                        block.current_value = block.possible_values[0]
                        self.remove_used_values(board[x][y])
                    self.board[x][y] = block

    def get_simple_solve_game(self, board):
        """Создает решение головоломки через простые сочетания"""
        while self.is_have_simple_blocks(board):
            self.simple_step_solve_game(board)

    @staticmethod
    def is_matrixx_fill(board):
        """Проверяет, заполнена ли головоломка"""
        for x in range(len(board)):
            for y in range(len(board[0])):
                if isinstance(board[x][y], ValueBlock):
                    bl = board[x][y]
                    if -1 == bl.current_value:
                        return False
        return True

    @staticmethod
    def is_have_simple_blocks(board):
        """Проверяет, есть ли в головоломке блоки с 1 возможным решением"""
        for x in range(len(board)):
            for y in range(len(board[0])):
                if isinstance(board[x][y], ValueBlock):
                    bl = board[x][y]
                    if len(bl.possible_values) == 1:
                        return True
        return False

    @staticmethod
    def is_have_alone_empty_block(block, axis):
        """Проверяет, есть ли один пустой блок в линии"""
        if axis == 1:
            parrent_block = block.parent_horizontal
            child_list = parrent_block.horizontal_child
        elif axis == 2:
            parrent_block = block.parent_vertical
            child_list = parrent_block.vertical_child
        else:
            child_list = []

        current_values = [x.current_value for x in child_list]
        return current_values.count(-1) == 1

    def get_sums_solve_game(self, board):
        """Создает решение головоломки через дополнение до суммы"""
        for x in range(len(board)):
            for y in range(len(board[0])):
                if isinstance(board[x][y], ValueBlock):
                    if self.is_have_alone_empty_block(board[x][y], Axis.HORIZONTAL.value):
                        self.addition_to_the_sum(board[x][y].parent_horizontal, Axis.HORIZONTAL.value)
        for x in range(len(board)):
            for y in range(len(board[0])):
                if isinstance(board[x][y], ValueBlock):
                    if self.is_have_alone_empty_block(board[x][y], Axis.VERTICAL.value):
                        self.addition_to_the_sum(board[x][y].parent_vertical, Axis.VERTICAL.value)

    def get_full_solve_game(self, board1):
        """Полное решение головоломки"""

        board = deepcopy(board1 if board1 is not None else self.cache_boards[-1])

        self.get_simple_solve_game(board)

        if self.is_matrixx_fill(board):
            self.cache_boards.append(board)
            return

        self.get_sums_solve_game(board)

        if self.is_matrixx_fill(board):
            self.cache_boards.append(board)
            return

        for x in range(len(board)):
            for y in range(len(board[0])):
                if isinstance(board[x][y], ValueBlock):
                    if board[x][y].current_value == -1:
                        bl = board[x][y]

                        for value in bl.possible_values:
                            copy_board = deepcopy(board)
                            copy_bl = copy_board[x][y]
                            copy_bl.current_value = value
                            self.remove_used_values(copy_bl)
                            self.get_full_solve_game(copy_board)
                            if self.solved:
                                return

        if len(self.cache_boards) > 300:
            cache_board = self.cache_boards[-1]
            cache = [cache_board]
            cache.extend([x for x in self.cache_boards if self.checker(x)])
            self.cache_boards = cache
            if len(self.cache_boards) > 1:
                self.solved = True

    def addition_to_the_sum(self, sum_block, axis):
        """Метод решения, путем дополнения до суммы"""

        if axis == 1:
            sum_value = sum_block.horizontal_int
            child_list = sum_block.horizontal_child
        elif axis == 2:
            sum_value = sum_block.vertical_int
            child_list = sum_block.vertical_child
        else:
            child_list = []
            sum_value = 0

        target_block = None

        for child in child_list:
            if child.current_value == -1:
                target_block = child

        result_value = 0

        for child in child_list:
            if child != target_block:
                result_value += child.current_value

        vals = sum_value - result_value

        if vals in target_block.possible_values:

            target_parrent_vertical_list_value = target_block.parent_vertical.vertical_list_value
            target_parrent_horizontal_list_value = target_block.parent_horizontal.horizontal_list_value

            if vals in target_parrent_horizontal_list_value and vals in target_parrent_vertical_list_value:
                target_block.current_value = vals
                self.remove_used_values(target_block)

    def checker(self, board):
        """Проверяет правильность решения головоломки"""

        current_sum = 0
        control_sum = 0
        contr = 0

        # Horizontal_check
        for x in range(len(board)):
            for y in range(len(board[0])):
                bl = board[x][y]
                if isinstance(bl, SumBlock):
                    control_sum = bl.horizontal_int
                    current_sum = 0
                    for child in range(bl.horizontal_count_child):
                        current_sum += board[x][y + 1 + child].current_value
                    if current_sum != control_sum:
                        contr += 1

            control_sum = 0
            current_sum = 0

        # Vertical_check
        for y1 in range(len(board[0])):
            for x1 in range(len(board)):
                bl = board[x1][y1]
                if isinstance(bl, SumBlock):
                    control_sum = bl.vertical_int
                    current_sum = 0
                    for child in range(bl.vertical_count_child):
                        current_sum += board[x1 + 1 + child][y1].current_value
                    if current_sum != control_sum:
                        contr += 1

            control_sum = 0
            current_sum = 0
        return contr == 0

    def returner(self):
        cac = []
        for b in self.cache_boards:
            if self.checker(b):
                if cac.count(b) == 0:
                    cac.append(b)

        return cac
