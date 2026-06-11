from figure import Figure


class Rectangle(Figure):
    """класс прямоугольника"""

    def __init__(self, side_a: int | float, side_b: int | float):
        if side_a <= 0 or side_b <= 0:
            raise ValueError(f'Sides must be above sero, current is side_a={side_a} and side_b={side_b}')

        self.side_a = side_a
        self.side_b = side_b

    @property
    def get_perimeter(self):
        return (self.side_a + self.side_b) * 2

    @property
    def get_area(self):
        return self.side_a * self.side_b
