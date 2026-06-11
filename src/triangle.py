from figure import Figure


class Triangle(Figure):
    """класс треугольника"""

    def __init__(self, side_a: int | float, side_b: int | float, side_c: int | float):
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError(
                f"Sides must be above sero, current is side_a={side_a} and side_b={side_b} and side_c={side_c}"
            )

        if not (
            (side_a + side_b > side_c)
            and (side_a + side_c > side_b)
            and (side_c + side_b > side_a)
        ):
            raise ValueError(f"A triangle with given sides does not exist")

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    @property
    def get_area(self):
        pp = self.get_perimeter() / 2
        return (
            pp * (pp - self.side_a) * (pp - self.side_b) * (pp - self.side_c)
        ) ** 0.5

    @property
    def get_perimeter(self):
        return self.side_a + self.side_b + self.side_c
