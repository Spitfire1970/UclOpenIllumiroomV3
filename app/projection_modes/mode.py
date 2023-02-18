from abc import ABC, abstractmethod


class Mode(ABC):
    @abstractmethod
    def trigger(self):
        pass

    # @abstractmethod
    # def apply_mode_to_frame(self,frame):
    #     pass
