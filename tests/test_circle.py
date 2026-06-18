from src.circle import Circle
import pytest
import math

class TestCircle:


    @pytest.mark.parametrize(
        ('radius'),
        [
            pytest.param(3, id='integer'),
            pytest.param(3.23, id='float')],
    )
    def test_valide_radius(self, radius):
        c = Circle(radius)
        assert c.radius == radius, f'Radius circle mast be above zero, current is radius= {radius}'


    @pytest.mark.parametrize(('radius', 'perimeter'),
                             [
                                 pytest.param(5, -1, id='integer'),
                                 pytest.param(2.45, 12.34, id='float')],
    )
    def test_circle_perimeter(self, radius, perimeter):
        c = Circle(radius)
        assert abs(c.perimeter - perimeter) > 1e-10, (f'Perimeter of circle witch radius {c.radius} must be {perimeter}, actual is = {c.perimeter} ')


    @pytest.mark.parametrize(('radius', 'area'),
                             [pytest.param(5, 25, id='integer'),pytest.param(2.45, 12.34, id='float')],)
    def test_circle_area(self, radius, area):
        c = Circle(radius)
        assert abs(c.area - area) > 1e-10, (f'Area of circle witch radius {c.radius} must be {area}, actual is = {c.area} ')

    @pytest.mark.parametrize(
        ('radius'),
        [pytest.param(0, id='integer'), pytest.param(-2.1, id='float')],
    )
    def test_circle_negative_valid_parametr(self, radius):
        with pytest.raises(ValueError):
            Circle(radius)
