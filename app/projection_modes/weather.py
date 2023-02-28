from .mode import Mode
import time
from utils.weather_detection import weatherdetection
from .snow import Snow
from .rain import Rain




class Weather(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture=None
        ):
        self.settings_access = settings_access
        self.neural_network_dir = self.settings_access.get_ml_model_path()
        self.background_img = background_img
        self.display_capture = display_capture
        self.audio_capture = audio_capture
        self.screenshot = self.display_capture.capture_frame()
        self.detector = weatherdetection(self.neural_network_dir)
        self.weather = self.detector.predict_weather(self.screenshot)
        self.timer = time.time()
        self.time_interval = 1

        #Create the mode objects from the mode factory
       
        self.snow = Snow( self.settings_access, self.display_capture,  self.background_img,  self.audio_capture)
        self.rain = Rain( self.settings_access, self.display_capture,  self.background_img,  self.audio_capture)


    def trigger(self):
        # if time.time() > self.timer + self.time_interval: 
        #     self.screenshot = self.display_capture.capture_frame()
        #     self.weather = self.detector.predict_weather(self.screenshot)
        #     self.timer = time.time()
        self.screenshot = self.display_capture.capture_frame()
        self.weather = self.detector.predict_weather(self.screenshot)
        if self.weather == "snow":
            snow_effect = self.snow.trigger()
            return snow_effect
        elif self.weather == "rain" or self.weather == "sandstorm":
            rain_effect = self.rain.trigger()
            return rain_effect
        else:
            return []


