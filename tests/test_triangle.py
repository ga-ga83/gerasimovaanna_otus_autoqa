from src.circle import Circle
from src.triangle import Triangle
import pytest


class TestTriangle():

    @pytest.mark.parametrize(
        ('side_a', 'side_b', 'side_c', 'perimeter'),
        [(5, 15, 14, 34), (3.23, 3.73, 1.86, 8.82)],
        ids=['integer', 'float'],
    )
    def test_triangle_perimeter(self, side_a, side_b, side_c, perimeter):
        t = Triangle(side_a, side_b, side_c)
        assert t.perimeter == perimeter, (
            f'Area of triangle witch sides {t.side_a}, {t.side_b} and {t.side_c} must be {perimeter}, actual is = {t.perimeter}'
        )

    @pytest.mark.parametrize(
        ('side_a', 'side_b', 'side_c', 'area'),
        [(3, 4, 5, 6.0), (13.02, 12.2, 15.34, 76.66046346429171)],
        ids=['integer', 'float'],
    )
    def test_triangle_area(self, side_a, side_b, side_c, area):

        t = Triangle(side_a, side_b, side_c)
        assert t.area == area, (f'Area of triangle witch sides {t.side_a}, {t.side_b} and {t.side_c} must be {area}, actual is = {t.area}'
        )

    @pytest.mark.parametrize(
        ('side_a', 'side_b', 'side_c'),
        [(3, 4, 0), (13.02, -12.2, 15.34)],
        ids=['integer', 'float'],
    )
    def test_triangle_negative(self, side_a, side_b, side_c):
        with pytest.raises(ValueError):
            Triangle(side_a, side_b, side_c)
