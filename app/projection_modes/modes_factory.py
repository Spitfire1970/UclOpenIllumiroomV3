from .cartoon import Cartoon
from .wobble import Wobble
from .blur import Blur
from .low_health import LowHealth
from .weather_snow import Snow
from .speed_lines import SpeedLines

class ModesFactory:

    def __init__(self, display_capture, audio_capture):
        self.mode_names = {
            "blur": Blur,
            "cartoon": Cartoon,
            "low_health": LowHealth,
            "wobble": Wobble,
            "snow": Snow,
            "speed_lines": SpeedLines,
        }
        self.display_capture = display_capture
        self.audio_capture = audio_capture

    def get_available_modes(self):
        return self.mode_names.keys()


    def get_modes(self, selected_modes):
        return_modes = []
        for mode in selected_modes:
            return_modes.append(self.mode_names[mode](self.display_capture, self.audio_capture))

        return return_modes
