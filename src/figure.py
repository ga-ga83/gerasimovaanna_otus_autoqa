from abc import ABC, abstractmethod


class Figure(ABC):
    """базовый класс"""

    @property
    @abstractmethod
    def get_perimeter(self):
        pass

    @property
    @abstractmethod
    def get_area(self):
        pass

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise ValueError(
                f"Argument figure must be Figure or child class, current {type(figure)}"
            )
        return self.get_area + figure.get_area
