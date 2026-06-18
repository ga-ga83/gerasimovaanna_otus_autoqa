from src.square import Square
import pytest

from tests.test_rectangle import TestRectangle


class TestSquare():

    @pytest.mark.parametrize(
        ('side_a', 'perimeter'),
        [pytest.param(5, 20, id='integer'), pytest.param(2.12, 8.48, id='float')],
    )
    def test_square_perimeter(self, side_a, perimeter):
        s = Square(side_a)
        assert s.perimeter == perimeter, (
            f'Perimeter of square witch side {s.side_a} must be {perimeter}, actual is = {s.perimeter}')

    @pytest.mark.parametrize(
        ('side_a', 'area'),
        [pytest.param(5, 25, id='integer'), pytest.param(2.1, 4.41, id='float')],
    )
    def test_square_area(self, side_a, area):
        s = Square(side_a)
        assert s.area == area, (
            f'Area of square witch sides {s.side_a} must be {area}, actual is = {s.area}'
        )

    @pytest.mark.parametrize(
        ('side_a'),
        [pytest.param(0, id='integer'), pytest.param(-2.1, id='float')],
    )
    def test_square_negative_valid_parametr(self, side_a):
        with pytest.raises(ValueError):
            Square(side_a)
