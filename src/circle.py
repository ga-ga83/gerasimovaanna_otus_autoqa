import math
from figure import Figure


class Circle(Figure):
    """класс круга"""

    def __init__(self, radius: int | float):
        if radius <= 0:
            raise ValueError(f'Radius circle must be above zero, current is radius={radius}')

        self.radius = radius

    @property
    def get_perimeter(self):
        return self.radius * 2 * math.pi

    @property
    def get_area(self):
        return math.pi * (self.radius ** 2)
