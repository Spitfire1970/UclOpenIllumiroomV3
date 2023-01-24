from abc import ABC, abstractmethod


class WeatherMode(ABC):
    @abstractmethod
    def trigger(self):
        pass

