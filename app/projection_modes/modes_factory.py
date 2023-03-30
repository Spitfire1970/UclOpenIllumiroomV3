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

    """
    Factory class for creating instances of different projectionmode classes.

    This class allows the creation of instances of different mode classes
    based on a selected projection mode name. The available projection mode classes and their names
    are specified in the `mode_names` dictionary.

    Attributes:
        mode_names (dict): A dictionary that maps mode names to mode classes.
        settings (SettingAccess): An object that provides access to application settings.
        img (np.ndarray): A background image to use as the base image for the modes.
        display_capture (DisplayCapture): An object that provides access to display capture functions.
        audio_capture (AudioCapture): An object that provides access to audio capture functions.
        selected_mode (str): The name of the currently selected mode.

    Methods:
        get_mode(): Returns an instance of the currently selected mode, with all required arguments.
    """

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


    def get_mode(self):

        return self.mode_names[self.selected_mode](
                                                self.settings, 
                                                self.display_capture, 
                                                self.img,
                                                self.audio_capture
                                            )
