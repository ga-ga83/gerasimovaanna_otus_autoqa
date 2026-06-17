from src.rectangle import Rectangle
import pytest


class TestRectangle():

    @pytest.mark.parametrize(
        ('side_a', 'side_b', 'area'),
        [(3, 5, 15), (3.23, 2.12, 6.8476)],
        ids=['integer', 'float'],
    )
    def test_rectangle_area(self, side_a, side_b, area):
        r = Rectangle(side_a, side_b)
        assert r.area == area, (
            f'Area of rectangle witch sides {r.side_a} and {r.side_b} must be 20, actual is = {r.area}'
        )

    @pytest.mark.parametrize(
        ('side_a', 'side_b', 'perimeter'),
        [pytest.param(3, 5, 16, id='integer'), pytest.param(3.23, 2.12, 10.7, id='float')],
    )
    def test_rectangle_perimeter(self, side_a, side_b, perimeter):
        r = Rectangle(side_a, side_b)
        assert r.perimeter == perimeter, (
            f'Perimeter of rectangle witch sides {r.side_a} and {r.side_b} must be {perimeter}, actual is = {r.perimeter}'
        )

    @pytest.mark.parametrize(
        ('side_a', 'side_b'),
        [pytest.param(0, 1, id='integer'), pytest.param(0.23, -2.1, id='float')],
    )
    def test_rectangle_negative_valid_parametr(self, side_a, side_b):
        with pytest.raises(ValueError):
            Rectangle(side_a, side_b)
