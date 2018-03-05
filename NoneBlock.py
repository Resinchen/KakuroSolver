class NoneBlock:
    """Класс пустой ячейки"""

    def __init__(self):
        pass

    def __str__(self):
        return 'Noned'

    def __eq__(self, other):
        return isinstance(other, self.__class__)
