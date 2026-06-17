from src.figure import Figure


class Square(Figure):
    def __init__(self, side_a: int | float):
        if side_a <= 0:
            raise ValueError(f'Sides must be above zero, current is side_a={side_a}')

        self.side_a = side_a

    @property
    def perimeter(self):
        return (self.side_a + self.side_a) * 2

    @property
    def area(self):
        return self.side_a * self.side_a
