from .mode import Mode
import time
from utils.weather_detection import weatherdetection
from .snow import Snow
from .rain import Rain


neural_network_dir = "C:/Users/user/Documents/weather_integration1/IllumiroomGroup33COMP0016-ImagineCupRelease/app/utils/ml_models"

class Weather(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture=None
        ):
        self.settings = settings_access
        self.background_img = background_img
        self.display_capture = display_capture
        self.audio_capture = audio_capture
        self.screenshot = self.display_capture.capture_frame()
        self.detector = weatherdetection(neural_network_dir)

        #Create the mode objects from the mode factory
       
        self.snow = Snow( self.settings, self.display_capture,  self.background_img,  self.audio_capture)
        self.rain = Rain( self.settings, self.display_capture,  self.background_img,  self.audio_capture)


    def trigger(self):
        # currenttime = time.time()
        # while time.time() < currenttime + 1:
        #     pass
        weather = self.detector.predict_weather(self.screenshot)
        if weather == "snow":
            snow_effect = self.snow.trigger()
            return snow_effect
        elif weather == "rain":
            rain_effect = self.rain.trigger()
            return rain_effect


