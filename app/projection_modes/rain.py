from .mode import Mode
import cv2
import numpy as np
import random


class Rain(Mode):
    """
    A class that represents the Rain mode, which adds a falling rain effect to a background image.
    """

    def __init__(
        self, 
        settings_access, 
        display_capture, 
        background_img=None, 
        audio_capture=None
    ):
        """
        Initializes a new instance of the Rain class.

        :param settings_access: An object that provides access to the settings for this mode.
        :param display_capture: A capture object that provides access to the display.
        :param background_img: The background image to which the rain effect will be added.
        :param audio_capture: A capture object that provides access to audio.
        """
        self.settings = settings_access
        self.img = background_img
        self.height, self.width = self.img.shape[:2]
        self.rain = np.zeros_like(background_img)
        self.raindrops = []
        self.rain_mode = self.settings.read_mode_settings("rain", "rain_mode")
        self.rain_point = self.settings.read_mode_settings("rain", [self.rain_mode, "rain_point"])
        self.possible_drop_lengths = self.settings.read_mode_settings("rain", "possible_drop_lengths")
        self.possible_drop_colours = self.settings.read_mode_settings("rain", "possible_drop_colours")

        self.rain_increment = self.settings.read_mode_settings("rain", [self.rain_mode, "rain_point_increment"])
        self.num_raindrops = self.settings.read_mode_settings("rain", [self.rain_mode, "num_raindrops"])
        self.speed_interval = self.settings.read_mode_settings("rain", [self.rain_mode, "falling_speed_interval"])
        self.wind_interval = self.settings.read_mode_settings("rain", [self.rain_mode, "noise_wind_interval"])

        self.falling_speed = random.randint(self.speed_interval[0], self.speed_interval[1])
        self.noise_wind = random.randint(self.wind_interval[0], self.wind_interval[1])
        

    def add_settling_rain(self, image):
        """
        Adds a settling rain effect to the given image.

        :param image: The image to which the settling rain effect will be added.
        :return: The image with the settling rain effect added.
        """
        # Conversion to HLS
        image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS)
        image_HLS = np.array(image_HLS, dtype = np.float64)
        brightness_coefficient = 0.7

        # Scale pixel values up for channel 1 (Lightness)
        image_HLS[:,:,1][image_HLS[:,:,1]<self.rain_point] = (image_HLS[:,:,1][image_HLS[:,:,1]<self.rain_point]*brightness_coefficient)
        # Set all values above 255 to 255
        image_HLS[:,:,1][image_HLS[:,:,1]>255]  = 255 

        # Convert to RGB
        image_HLS = np.array(image_HLS, dtype = np.uint8)    
        image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB)
        # Change contrast, brightness
        # cv2.convertScaleAbs(image_RGB, alpha=1, beta=0)
 
        return image_RGB


    def add_to_top(self, scale):
        """
        Adds new raindrops to the top of the image.

        :param scale: The maximum scale for the raindrops.
        """
        if len(self.raindrops) == 0:
        # Add new raindrops to the top of the image
            for i in range(self.num_raindrops):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                r = random.randint(4, scale)
                self.raindrops.append([x, y, r])
        
    
    def create_falling_rain(self, max_scale, scale_factor):
        """
        Generates falling raindrops in the `rain` image by modifying the positions, sizes and colors of existing raindrops.
        
        Args:
        - max_scale (int): The maximum size that a raindrop can have.
        - scale_factor (float): How much the size of raindrops can change as they fall.
        """
        slant_extreme = 1
        slant = np.random.randint(-slant_extreme, slant_extreme)
        #drop_length = 20
        drop_width = 2
        #drop_color = (255,120,0)
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

            cv2.line(
                self.rain,(raindrop[0], raindrop[1]), (raindrop[0]+slant, raindrop[1]+self.get_random_drop_length()), self.get_random_drop_color(), drop_width)

            # Keep raindrops within background image
            if raindrop[1] > self.height:
                raindrop[1] = 0
            if raindrop[0] > self.width:
                raindrop[0] = 0


    def add_rain_to_image(self):
        return cv2.addWeighted(self.img, 0.8, self.rain, 0.8, 0)

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
