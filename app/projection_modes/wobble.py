from .mode import Mode
from utils.audio_capture import AudioCapture
from utils.settings_access import SettingsAccess

import numpy as np
import cv2

# TODO: refactor generate_frames method
# - single responsibility principle!!

class Wobble(Mode):
    """
    The `Wobble` projection mode displays a wobble effect applied to the background image when triggered by media audio.

    Key Attributes:
        img (numpy.ndarray): The background image to which the wobble effect is applied.
        settings (SettingsAccess): The object that provides access to the mode settings.
        wobble_settings (dict): The wobble mode settings.
        num_frames (int): The number of frames in the wobble animation.
        amplitude (float): The initial amplitude of the wobble effect.
        frequency (float): The initial frequency of the wobble effect.
        output_img (numpy.ndarray): The output image after applying the wobble effect.
        x (numpy.ndarray): The x-coordinate meshgrid of the background image.
        y (numpy.ndarray): The y-coordinate meshgrid of the background image.
        original_x (numpy.ndarray): A copy of the x-coordinate meshgrid of the background image.
        original_y (numpy.ndarray): A copy of the y-coordinate meshgrid of the background image.
        fractal_amplitude (float): The amplitude of the fractal noise applied to the wobble effect.
        tv_data (dict): The TV data settings used to exclude pixels inside the TV rectangle.
        tv_tl_coords (tuple): The top-left coordinates of the TV rectangle.
        tv_br_coords (tuple): The bottom-right coordinates of the TV rectangle.
        tv_center_x (int): The x-coordinate of the center of the TV rectangle.
        tv_center_y (int): The y-coordinate of the center of the TV rectangle.
        audio_capture (AudioCapture): The object that provides audio capture functionality.
        frames (list): The list of frames in the wobble animation.

    Methods:
        generate_frames(): Generates the frames for the wobble animation.
        trigger(): Triggers the wobble animation mode.
    """

    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture
        ):
        self.img = background_img
        self.settings = settings_access

        self.wobble_settings = self.settings.read_mode_settings("wobble", "data")
        self.num_frames = self.wobble_settings["num_frames"]
        self.amplitude = self.wobble_settings["initial_amplitude"]
        self.frequency = self.wobble_settings["initial_frequency"]

        self.output_img = np.zeros_like(self.img)
        height, width = self.img.shape[:2]
        self.x, self.y = np.meshgrid(np.arange(width), np.arange(height))
        self.original_x, self.original_y = self.x.copy(), self.y.copy()
        self.fractal_amplitude = self.wobble_settings["fractal_amplitude"]

        self.tv_data = self.settings.read_mode_settings("wobble", "tv_data")
        self.tv_tl_coords = self.tv_data["tv_top_left"]
        self.tv_br_coords = self.tv_data["tv_bottom_right"]
        self.tv_center_x = self.tv_data["tv_center_x"]
        self.tv_center_y = self.tv_data["tv_center_y"]
        # self.threshold = self.settings.read_mode_settings("wobble", "sound_threshold")

        self.audio_capture = audio_capture
        # self.audio_capture.set_threshold(self.threshold)

        self.frames = None
        self.generate_frames()


    def generate_frames(self):
        """
        Generates a list of image frames by applying a wobbling effect to the background image.
        
        The wobbling effect is created by manipulating the pixel positions of the original image, 
        using a sinuosoidal wave equation. The amplitude and frequency of the sine wave is adjusted based on 
        the frame number to create a wobbling effect that increases and then decreases over time. 
        The resulting frames are stored in a list.
        
        Returns:
            None
        """
        print("Generating wobble frames")
        self.frames = []
        for i in range(self.num_frames):
            amplitude = self.amplitude * (i/self.num_frames)
            frequency = self.frequency * (i/self.num_frames)
            # Interpolation factor
            factor = 1 - i / (self.num_frames - 1)

            # Create a mask to exclude pixels inside the TV rectangle
            mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            cv2.rectangle(mask, self.tv_tl_coords, self.tv_br_coords, (255, 255, 255), -1)

            # Calculate distance from the center of the effect
            distance = np.sqrt((self.x - self.tv_center_x) ** 2 + (self.y - self.tv_center_y) ** 2)
            distance[mask == 255] = 0
            fractal_noise = np.random.normal(0, self.fractal_amplitude, distance.shape)
            distance = distance + fractal_noise

            # Calculate the angle of the pixel
            angle = distance * frequency

            # Calculate the new x and y coordinates using the sine wave equation
            new_x = self.x + amplitude * np.sin(angle)
            new_y = self.y + amplitude * np.cos(angle)

            # Interpolate between new pixel pos and the original pos
            # (to bring animation to stop how it started)
            new_x = np.float32(self.original_x * (1 - factor) + new_x * factor)
            new_y = np.float32(self.original_y * (1 - factor) + new_y * factor)

            # Use remap with new coords and Lanczos Interpolation method
            # For future: can re-map onto a cartoon image
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        """
        Triggers the wobbling effect animation by returning a list of image frames.
        
        The function checks for the presence of a loud sound using an audio capture device. If a 
        loud sound is detected, the frames with the wobbling effect are returned. Otherwise, 
        the original image is returned.
        
        Returns:
            A list of image frames. Either wobble frames, or a list containing the original background image.
        """
        if self.audio_capture.detect_loud_sound():
        # if self.audio_capture.detect_explosive_sound():
            frames = self.frames
        else:
            frames = [self.img]
        return frames