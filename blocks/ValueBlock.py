class ValueBlock:
    """Класс ячейки для значений"""
    def __init__(self, value=-1):
        self.possible_values = []
        self.parent_vertical = None
        self.parent_horizontal = None
        self.current_value = value

    def set_parent_vertical(self, sum_block: type(SumBlock)):
        """Устанавливает вертикальный блок суммы"""
        self.parent_vertical = sum_block

    def set_parent_horizontal(self, sum_block: type(SumBlock)):
        """Устанавливает горизонтальный блок суммы"""
        self.parent_horizontal = sum_block

    def set_possible_values(self):
        """Устанавливает возможные значения для ячейки"""
        self.possible_values = list(set(self.parent_vertical.vertical_list_value) &
                                    set(self.parent_horizontal.horizontal_list_value))

    def __str__(self):
        return '  {}  '.format(self.current_value) if self.current_value != -1 else'  {}  '.format(self.possible_values)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.current_value == other.current_value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
