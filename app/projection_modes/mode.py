from abc import ABC, abstractmethod


class Mode(ABC):
    @abstractmethod
    def trigger(self):
        pass
