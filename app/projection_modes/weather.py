from .mode import Mode
import time
from utils.weather_detection import weatherdetection
from utils.display_capture import DisplayCapture
from .snow import Snow
from .rain import Rain

neural_network_dir = "C:/Users/user/Documents/weather_integration1/IllumiroomGroup33COMP0016-ImagineCupRelease/app/utils/ml_models"

class Weather(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img=None,
            audio_capture=None
        ):
        self.settings = settings_access
        self.background_img = background_img
        self.display_capture = display_capture
        self.screenshot = DisplayCapture(display_capture, self.projector_bounding_box).capture_frame()
        self.detector = weatherdetection(neural_network_dir)
        self.projector_bounding_box = DisplayCapture.get_projector_bounding_box()



    def trigger(self):
        currenttime = time.time()
        while time.time() < currenttime + 2:
            pass
        weather = self.detector.predict_weather(self.screenshot)
        if weather == "snow":
            snow_effect = Snow(self.settings, self.screenshot).trigger()
            return snow_effect
        elif weather == "rain":
            rain_effect = Rain(self.settings, self.screenshot).trigger()
            return rain_effect


