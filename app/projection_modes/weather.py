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
        self.settings_access = settings_access
        self.background_img = background_img
        self.display_capture = display_capture
        self.screenshot = self.display_capture.capture_frame()
        self.detector = weatherdetection(neural_network_dir)


    def trigger(self):
        currenttime = time.time()
        while time.time() < currenttime + 2:
            pass
        weather = self.detector.predict_weather(self.screenshot)
        if weather == "snow":
            return Snow
        elif weather == "rain":
            return Rain


