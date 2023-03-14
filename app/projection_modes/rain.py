from .mode import Mode
from cv2 import cvtColor,COLOR_RGB2HLS, COLOR_HLS2RGB, line, addWeighted
import numpy as np
import random


class Rain(Mode):

    def __init__(
        self, 
        settings_access, 
        display_capture, 
        background_img=None, 
        audio_capture=None
    ):
        self.settings = settings_access
        self.img = background_img
        self.height, self.width = self.img.shape[:2]
        self.rain = np.zeros_like(background_img)
        self.raindrops = []
        self.rain_mode = self.settings.read_mode_settings("rain", "rain_mode")
        self.rain_mode_settings = self.settings.read_mode_settings("rain", self.rain_mode)
        
        self.rain_point = self.rain_mode_settings["rain_point"]
        self.rain_increment = self.rain_mode_settings["rain_point_increment"]
        self.num_raindrops = self.rain_mode_settings["num_raindrops"]
        self.speed_interval = self.rain_mode_settings["falling_speed_interval"]
        self.wind_interval = self.rain_mode_settings["noise_wind_interval"]

        self.possible_drop_lengths = self.settings.read_mode_settings("rain", "possible_drop_lengths")
        self.possible_drop_colours = self.settings.read_mode_settings("rain", "possible_drop_colours")

        self.falling_speed = random.randint(self.speed_interval[0], self.speed_interval[1])
        self.noise_wind = random.randint(self.wind_interval[0], self.wind_interval[1])


    def add_to_top(self, scale):

        if len(self.raindrops) == 0:
        # Add new raindrops to the top of the image
            for i in range(self.num_raindrops):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                r = random.randint(4, scale)
                self.raindrops.append([x, y, r])
        
    
    def create_falling_rain(self, max_scale, scale_factor):
        slant_extreme = 1
        slant = np.random.randint(-slant_extreme, slant_extreme)
        drop_width = 2
        # Move raindrops down by falling speed and wind
        for i in range(len(self.raindrops)):
            raindrop = self.raindrops[i]
            # Add randomness to y and x pos
            raindrop[1] += self.noise_wind + self.falling_speed
            # Add randomness to size of raindrop
            raindrop[2] += random.uniform(-abs(scale_factor), scale_factor)

            # Keep raindrops within the desired scale
            if raindrop[2] < 0:
                raindrop[2] = 0
            elif raindrop[2] > max_scale:
                raindrop[2] = max_scale

            line(
                self.rain,(raindrop[0], raindrop[1]), (raindrop[0]+slant, raindrop[1]+self.get_random_drop_length()), self.get_random_drop_color(), drop_width)

            # Keep raindrops within background image
            if raindrop[1] > self.height:
                raindrop[1] = 0
            if raindrop[0] > self.width:
                raindrop[0] = 0


    def add_rain_to_image(self):
        return addWeighted(self.img, 0.8, self.rain, 0.8, 0)

    def get_random_drop_color(self):
        return tuple(random.choice(self.possible_drop_colours))


    def get_random_drop_length(self):
        return random.choice(self.possible_drop_lengths)

    def trigger(self):
        # rain flake properties
        max_scale = 4
        scale_factor = 140   # how much scale will change as rain drops

        # Add new raindrops to the top of the image
        self.add_to_top(max_scale)

        while True:
            # Clear the rain image
            self.rain.fill(0)

            self.create_falling_rain(max_scale, scale_factor)
            
            img = self.add_rain_to_image()
            #img = self.add_settling_rain(img)
            self.rain_point += self.rain_increment

            return [img]