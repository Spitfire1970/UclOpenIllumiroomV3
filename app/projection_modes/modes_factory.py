from .cartoon import Cartoon
from .wobble import Wobble
from .blur import Blur
from .low_health import LowHealth
from .weather import Weather
from .snow import Snow
from .speed_lines import SpeedLines

class ModesFactory:

    def __init__(
        self, 
        background_image, 
        display_capture, 
        audio_capture, 
        setting_access
    ):
        self.mode_names = {
            "blur": Blur,
            "cartoon": Cartoon,
            "low_health": LowHealth,
            "wobble": Wobble,
            "weather": Weather,
            "snow": Snow,
            "speed_lines": SpeedLines,
        }
        self.settings = setting_access
        self.img = background_image
        self.display_capture = display_capture
        self.audio_capture = audio_capture
        #self.background_image = read_background_image()

    def get_available_modes(self):
        return self.mode_names.keys()

    def get_mode(self, selected_mode):
        return self.mode_names[selected_mode](
                                                self.settings, 
                                                self.display_capture, 
                                                self.img,
                                                self.audio_capture
                                            )
