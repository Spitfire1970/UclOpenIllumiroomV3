from .mode import Mode
import cv2
import numpy as np
import random


class Snow(Mode):

    def __init__(
        self, 
        settings_access, 
        display_capture, 
        background_img=None, 
        audio_capture=None
    ):
        """
        Initializes the Snow mode object.

        Args:
            settings_access (object): An object that provides access to mode-specific settings.
            display_capture (object): The object that captures the display.
            background_img (numpy.ndarray, optional): The background image to add snow to. Defaults to None.
            audio_capture (object, optional): The object that captures audio. Defaults to None.
        """
        self.settings = settings_access
        self.img = background_img
        self.height, self.width = self.img.shape[:2]
        self.snow = np.zeros_like(background_img)
        self.snowflakes = []
        self.snow_amount = self.settings.read_mode_settings("snow", "snow_amount")

        self.snow_amount_settings = self.settings.read_mode_settings("snow", self.snow_amount)
        self.snow_point = self.snow_amount_settings["snow_point"]
        self.snow_increment = self.snow_amount_settings["snow_point_increment"]
        self.num_snowflakes = self.snow_amount_settings["num_snowflakes"]
        self.speed_interval = self.snow_amount_settings["falling_speed_interval"]
        self.wind_interval = self.snow_amount_settings["noise_wind_interval"]
        
        self.falling_speed = random.randint(self.speed_interval[0], self.speed_interval[1])
        self.noise_wind = random.randint(self.wind_interval[0], self.wind_interval[1])


    def add_settling_snow(self, image):
        """
        Adds settling snow to an image.

        Args:
            image (numpy.ndarray): The image to add settling snow to.

        Returns:
            numpy.ndarray: The image with settling snow added to it.
        """
        # Conversion to HLS
        image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS)
        image_HLS = np.array(image_HLS, dtype = np.float64)
        brightness_coefficient = 2.5

        # Scale pixel values up for channel 1 (Lightness)
        image_HLS[:,:,1][image_HLS[:,:,1]<self.snow_point] = (
            image_HLS[:,:,1][image_HLS[:,:,1]<self.snow_point]*brightness_coefficient
        )
        # Set all values above 255 to 255
        image_HLS[:,:,1][image_HLS[:,:,1]>255]  = 255 

        # Convert to RGB
        image_HLS = np.array(image_HLS, dtype = np.uint8)    
        image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB)
        # Change contrast, brightness
        # cv2.convertScaleAbs(image_RGB, alpha=1, beta=0)
 
        return image_RGB


    def add_to_top(self, radius):
        """
        Adds new snowflakes to the top of the image.

        Args:
            radius (int): The maximum radius of the snowflakes.
        """
        if len(self.snowflakes) == 0:
        # Add new snowflakes to the top of the image
            for i in range(self.num_snowflakes):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                r = random.randint(3, radius)
                self.snowflakes.append([x, y, r])

    def create_falling_snow(self, max_radius, radius_factor):
        """
        Move snowflakes down by falling speed and wind, and update their properties. 
        Keep snowflakes within the desired radius and the background image.
        
        Args:
            max_radius (int): The maximum radius of a snowflake.
            radius_factor (float): How much the radius of a snowflake will change as it falls.
        
        """
        # Move snowflakes down by falling speed and wind
        for i in range(len(self.snowflakes)):
            snowflake = self.snowflakes[i]
            # Add randomness to y and x pos
            snowflake[1] += random.randint(-1, 1) + self.noise_wind + self.falling_speed
            snowflake[0] += random.randint(-1, 1) + self.noise_wind
            # Add randomness to size of snowflake
            snowflake[2] += random.uniform(-abs(radius_factor), radius_factor)

            # Keep snowflakes within the desired radius
            if snowflake[2] < 0:
                snowflake[2] = 0
            elif snowflake[2] > max_radius:
                snowflake[2] = max_radius

            cv2.circle(
                self.snow, (snowflake[0], snowflake[1]), 
                int(snowflake[2]), (255, 255, 255), -1
            )

            # Keep snowflakes within background image
            if snowflake[1] > self.height:
                snowflake[1] = 0
            if snowflake[0] > self.width:
                snowflake[0] = 0


    def add_snow_to_image(self):
        return cv2.addWeighted(self.img, 0.8, self.snow, 0.3, 0)


    def trigger(self):
        # Snow flake properties
        max_radius = 5
        radius_factor = 3    # how much radius will change as snow falls

        # Add new snowflakes to the top of the image
        self.add_to_top(max_radius)

        while True:
            # Clear the snow image
            self.snow.fill(0)

            self.create_falling_snow(max_radius, radius_factor)
            
            overlay = self.add_snow_to_image()
            img = self.add_settling_snow(overlay)
            self.snow_point += self.snow_increment

            return [img]
