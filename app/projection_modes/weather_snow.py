from .weather import WeatherMode


class Snow(WeatherMode):
    
    def trigger(self):
        print("trigger snow")
