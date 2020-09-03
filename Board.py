from SumBlock import SumBlock
from NoneBlock import NoneBlock
from ValueBlock import ValueBlock
from KakuroExceptions import *


class Board:
    """Класс представления головоломки"""

    def __init__(self, filename: str):
        self.board = []
        self.game_desk = []

        self.parser_kakuro(filename)

        self.width = len(self.board[0])
        self.height = len(self.board)

        self.convert_in_blocks()

        self.grab_links_for_block()

        self.process_possible_value()


    def parser_kakuro(self, filename: str):
        """Парсит файл с головоломкой"""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.board.append(line.replace('\n', '').split('  '))
                    self.game_desk.append(line.replace('\n', '').split('  '))
        except IOError:
            print("Не удалось открыть файл")
            raise FileIsOut()


    def convert_in_blocks(self):
        """Конвертирует текстовые комбинации в блоки"""
        try:
            for row in range(self.height):
                for col in range(self.width):
                    if self.board[row][col] == '(nnn)':
                        self.game_desk[row][col] = NoneBlock()
                    elif self.board[row][col] == '(...)':
                        self.game_desk[row][col] = ValueBlock()
                    else:
                        self.game_desk[row][col] = SumBlock(self.board[row][col])
        except ValueError:
            print('Не корректно задана головоломка')
            raise NotCorrectValuePuzzle()

    def process_possible_value(self):
        """Собирает комбинации суммы в SumBlock и обрабатывает возможные значения для ValueBlock"""
        for row in range(self.height):
            for col in range(self.width):
                if isinstance(self.game_desk[row][col], SumBlock):
                    self.game_desk[row][col].set_lists_value()

        for row in range(self.height):
            for col in range(self.width):
                if isinstance(self.game_desk[row][col], ValueBlock):
                    self.game_desk[row][col].set_possible_values()

    def grab_links_for_block(self):
        """Собирает ссылки на блоки принадлежащие SumBlock"""
        for row in range(self.height):
            for col in range(self.width):
                if isinstance(self.game_desk[row][col], SumBlock):
                    block = self.game_desk[row][col]
                    block.horizontal_count_child = 0
                elif isinstance(self.game_desk[row][col], ValueBlock):
                    if block is not None:
                        self.game_desk[row][col].set_parent_horizontal(block)
                        block.horizontal_child.append(self.game_desk[row][col])
                        block.horizontal_count_child += 1
                elif isinstance(self.game_desk[row][col], NoneBlock):
                    block = None
            block = None

        for i in range(self.width):
            for j in range(self.height):
                if isinstance(self.game_desk[j][i], SumBlock):
                    block = self.game_desk[j][i]
                    block.vertical_count_child = 0
                elif isinstance(self.game_desk[j][i], ValueBlock):
                    if block is not None:
                        self.game_desk[j][i].set_parent_vertical(block)
                        block.vertical_child.append(self.game_desk[j][i])
                        block.vertical_count_child += 1
            block = None
