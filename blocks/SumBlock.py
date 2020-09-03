import Combination


class SumBlock:
    """Класс для ячейки с суммами"""

    def __init__(self, text_block: str):
        self.vertical_int = int(text_block.split('/')[0].split('(')[1])
        self.horizontal_int = int(text_block.split('/')[1].split(')')[0])
        self.vertical_count_child = 0
        self.horizontal_count_child = 0
        self.horizontal_list_value = []
        self.vertical_list_value = []
        self.vertical_child = []
        self.horizontal_child = []

    def set_lists_value(self):
        """Устанавливает 'суммарные' значения в SumBlock"""
        self.horizontal_list_value = Combination.get_comb(self.horizontal_count_child, self.horizontal_int)
        self.vertical_list_value = Combination.get_comb(self.vertical_count_child, self.vertical_int)

    def __str__(self):
        return '({}/{})'.format(self.vertical_int, self.horizontal_int)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__str__() == other.__str__()
        else:
            return False
