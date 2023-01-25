from .cartoon import Cartoon
from .wobble import Wobble
from .blur import Blur
from .low_health import LowHealth
from .weather_snow import Snow


class ModesFactory:

    def __init__(self):
        self.mode_names = {
            "blur": Blur,
            "cartoon": Cartoon,
            "low_health": LowHealth,
            "wobble": Wobble,
            "snow": Snow
        }

    def get_available_modes(self):
        return self.mode_names.keys()


    def get_modes(self, selected_modes):
        return_modes = []
        for mode in selected_modes:
            return_modes.append(self.mode_names[mode]())

        return return_modes
