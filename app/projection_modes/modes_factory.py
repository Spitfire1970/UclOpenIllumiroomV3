from .cartoon import Cartoon
from .wobble import Wobble
from .blur import Blur
from .low_health import LowHealth
from .weather import Weather
from .rain import Rain
from .snow import Snow
from .speed_blur import SpeedBlur
from .display_image import DisplayImage

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
            "rain": Rain,
            "snow": Snow,
            "speed_blur": SpeedBlur,
            "display_image": DisplayImage,
        }
        self.settings = setting_access
        self.img = background_image
        self.display_capture = display_capture
        self.audio_capture = audio_capture
        self.selected_mode = setting_access.read_general_settings("selected_mode")
        #self.background_image = read_background_image()

    def get_available_modes(self):
        return self.mode_names.keys()

    def get_mode(self):

        return self.mode_names[self.selected_mode](
                                                self.settings, 
                                                self.display_capture, 
                                                self.img,
                                                self.audio_capture
                                            )
