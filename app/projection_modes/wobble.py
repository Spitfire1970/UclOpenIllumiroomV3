from .mode import Mode
from utils.audio_capture import AudioCapture
from utils.settings_access import SettingsAccess

import numpy as np
import cv2


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
        self.initial_ampl  = self.wobble_settings["initial_amplitude"]
        self.initial_freq  = self.wobble_settings["initial_frequency"]

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

        self.audio_capture = audio_capture

        self.frames = None
        self.generate_frames()


    def create_TV_mask(self):
        """Create a mask to exclude pixels inside the TV 
        rectangle in the animation. Use the TV coordinates
        saved in the mode settings with an inward padding
        to give the appearance that the TV edges are shaking.

        Parameters:
        -----------
        None

        Returns:
        --------
        mask : numpy.ndarray
            A numpy array representing the mask for the TV.
        """
        mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        # Apply padding (in px)
        padding = 9
        new_tl_coords = [sum(i) for i in zip(self.tv_tl_coords, [padding, padding])]
        new_br_coords = [sum(i) for i in zip(self.tv_br_coords, [-abs(padding), -abs(padding)])]
        # Fill white rectangle for area inside the TV with padding
        cv2.rectangle(mask, new_tl_coords, new_br_coords, (255, 255, 255), -1)
        return mask


    def calc_center_distance(self, mask):
        """Calculate the distance from center of effect (the TV 
        centre) and the pixels. Set distance for pixels inside the 
        TV mask to 0, so that they are not included in the animation.

        Parameters:
        -----------
        mask : numpy.ndarray
            A binary mask with the same shape as the input image, where white
            pixels represent the area inside the TV rectangle that should be
            excluded.
        
        Returns:
        --------
        distance : numpy.ndarray
            Distance between the center of the effect and each pixel (with pixels
            in the TV mask set to 0).
        """
        distance = np.sqrt((self.x - self.tv_center_x) ** 2 + (self.y - self.tv_center_y) ** 2)
        distance[mask == 255] = 0
        fractal_noise = np.random.normal(0, self.fractal_amplitude, distance.shape)
        distance = distance + fractal_noise
        return distance


    def calc_pixels_coords(self, distance, frequency, amplitude, factor):
        """Calculate the new coordinates of each pixel based on the
        sinusoidal distortion.
        
        Parameters:
        -----------
        distance : numpy.ndarray
            Distance between the center of the effect and each pixel.
        frequency : float
            The intial frequency of the sine wave effect.
        amplitude : float
            The inital amplitude of the sine wave effect.
        factor : float
            The interpolation factor used to bring the animation 
            to stop how it started.

        Returns:
        --------
        new_x, new_y : tuple of numpy.ndarray
            The new x and y coordinates of each pixel.
        """
        angle = distance * frequency
        # Calculate new x and y coords using sine wave eqn
        new_x = self.x + amplitude * np.sin(angle)
        new_y = self.y + amplitude * np.cos(angle)

        # Interpolate between new pixel pos and initial positions
        new_x = np.float32(self.original_x * (1 - factor) + new_x * factor)
        new_y = np.float32(self.original_y * (1 - factor) + new_y * factor)
        return new_x, new_y


    def generate_frames(self):
        """Generates a list of image frames by applying a 
        sinusoidal wobble effect to the background image.
        
        The wobbling effect is created by manipulating the 
        pixel positions of the original image, using a sinuosoidal 
        wave equation. The amplitude and frequency of the sine wave 
        is adjusted based on the frame number to create a wobbling 
        effect that increases and then decreases over time to come
        to a stop. 
        
        The resulting frames for the animation are stored in a list.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        print("Generating wobble frames, awesomeness coming soon!")
        self.frames = []
        for i in range(self.num_frames):
            amplitude = self.initial_ampl * (i/self.num_frames)
            frequency = self.initial_freq * (i/self.num_frames)
            # Interpolation factor - used to bring
            # animation to stop how it started
            factor = 1 - i / (self.num_frames - 1)

            mask = self.create_TV_mask()
            distance = self.calc_center_distance(mask)

            new_x, new_y = self.calc_pixels_coords(
                                distance, frequency, amplitude, factor
                            )

            # Use remap with new coords and Lanczos Interpolation method
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        """
        Triggers the wobbling effect animation by returning 
        a list of image frames.
        
        The function checks for the presence of a loud sound 
        using an audio capture device. If a loud sound is detected, 
        the pre-generated frames for the wobbling effect are returned. 
        Otherwise, the original image is of the room is returned.
        
        Returns:
        --------
            A list of image frames. Either wobble frames, or
            a list containing the original background image.
        """
        if self.audio_capture.detect_loud_sound():
            frames = self.frames
        else:
            frames = [self.img]
        return frames
