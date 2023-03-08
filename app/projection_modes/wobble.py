"""
from .mode import Mode
from utils.audio_capture import AudioCapture
from utils.settings_access import SettingsAccess

import numpy as np
from cv2 import rectangle, remap, INTER_LANCZOS4

# TODO: refactor generate_frames method
# - single responsibility principle!!

class Wobble(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture
        ):
        self.img = background_img
        self.settings = settings_access
        self.num_frames = self.settings.read_mode_settings("wobble", "num_frames")

        self.output_img = np.zeros_like(self.img)
        height, width = self.img.shape[:2]
        self.x, self.y = np.meshgrid(np.arange(width), np.arange(height))
        self.original_x, self.original_y = self.x.copy(), self.y.copy()
        self.fractal_amplitude = self.settings.read_mode_settings("wobble", "fractal_amplitude")

        # self.threshold = self.settings.read_mode_settings("wobble", "sound_threshold")

        self.audio_capture = audio_capture
        # self.audio_capture.set_threshold(self.threshold)

        self.frames = None
        self.generate_frames()


    def generate_frames(self):
        print("Generating wobble frames, awesomeness coming soon!")
        self.frames = []
        for i in range(self.num_frames):
            amplitude = 30 * (i/self.num_frames)
            frequency = 0.10 * (i/self.num_frames)
            # Interpolation factor
            factor = 1 - i / self.num_frames

            # Create a mask to exclude pixels inside the TV rectangle
            top_left_coords = self.settings.read_mode_settings("wobble", "tv_top_left")
            bottom_right_coors = self.settings.read_mode_settings("wobble", "tv_bottom_right")
            mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            rectangle(mask, top_left_coords, bottom_right_coors, (255, 255, 255), -1)

            # Calculate distance from the center of the effect
            center_x = self.settings.read_mode_settings("wobble", "tv_center_x")
            center_y = self.settings.read_mode_settings("wobble", "tv_center_y")

            distance = np.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)
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
            output_img = remap(self.img, new_x, new_y, INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        if self.audio_capture.detect_loud_sound():
        # if self.audio_capture.detect_explosive_sound():
            frames = self.frames
        else:
            frames = [self.img]
        return frames
"""
from .mode import Mode
from utils.audio_capture import AudioCapture
from utils.settings_access import SettingsAccess

import numpy as np
import cv2

# TODO: refactor generate_frames method
# - single responsibility principle!!

class Wobble(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture
        ):
        self.img = background_img
        self.settings = settings_access
        
        # Generating wobble animation
        self.num_frames = self.settings.read_mode_settings("wobble", "num_frames")
        self.initial_ampl = self.settings.read_mode_settings("wobble", "initial_amplitude")
        self.initial_freq = self.settings.read_mode_settings("wobble", "initial_frequency")

        self.output_img = np.zeros_like(self.img)
        height, width = self.img.shape[:2]
        self.x, self.y = np.meshgrid(np.arange(width), np.arange(height))
        self.original_x, self.original_y = self.x.copy(), self.y.copy()
        self.fractal_amplitude = self.settings.read_mode_settings("wobble", "fractal_amplitude")

        # Sound analysis
        # analysis_type can be: loud_sound or explosive_sound. NOTE: Extend this in future.
        self.analysis_type = self.settings.read_mode_settings("wobble", "sound_analysis_type")
        self.threshold = self.settings.read_mode_settings("wobble", "sound_threshold")

        self.audio_capture = audio_capture
        self.audio_capture.set_threshold(self.threshold)

        # Frame generation
        self.frames = None
        self.generate_frames()

    def create_TV_mask(self):
        # Create a mask to exclude pixels inside the TV rectangle
        top_left_coords = self.settings.read_mode_settings("wobble", "tv_top_left")
        bottom_right_coors = self.settings.read_mode_settings("wobble", "tv_bottom_right")
        mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, top_left_coords, bottom_right_coors, (255, 255, 255), -1)

        return mask

    def calc_center_distance(self, mask):
        # Calculate distance from center of effect and the pixels
        center_x = self.settings.read_mode_settings("wobble", "tv_center_x")
        center_y = self.settings.read_mode_settings("wobble", "tv_center_y")

        distance = np.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)
        distance[mask == 255] = 0
        fractal_noise = np.random.normal(0, self.fractal_amplitude, distance.shape)
        distance = distance + fractal_noise
        return distance

    def calc_pixels_coords(self, distance, frequency, amplitude, factor):
        angle = distance * frequency
        # Calculate new x and y coords using sine wave eqn
        new_x = self.x + amplitude * np.sin(angle)
        new_y = self.y + amplitude * np.cos(angle)

        # Interpolate between new pixel pos and initial positions
        new_x = np.float32(self.original_x * (1 - factor) + new_x * factor)
        new_y = np.float32(self.original_y * (1 - factor) + new_y * factor)
        return new_x, new_y


    def generate_frames(self):
        print("Generating wobble frames, awesomeness coming soon!")
        self.frames = []
        for i in range(self.num_frames):
            amplitude = self.initial_ampl * (i/self.num_frames)
            frequency = self.initial_freq * (i/self.num_frames)
            # Interpolation factor - used to bring
            # animation to stop how it started
            factor = 1 - i / (self.num_frames - 2)

            mask = self.create_TV_mask()
            distance = self.calc_center_distance(mask)

            new_x, new_y = self.calc_pixels_coords(
                distance, frequency, amplitude, factor
            )

            # Use remap with new coords and Lanczos Interpolation method
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        do_trigger = False

        # NOTE: avoid if-else statements in future to 
        # make this more extendible for other types of 
        # audio analysis e.g. trigger when a sound effect
        # is present
        if self.analysis_type == "loud_sound":
            do_trigger = self.audio_capture.detect_loud_sound()
        elif self.analysis_type == "explosive_sound":
            do_trigger = self.audio_capture.detect_explosive_sound()

        if do_trigger:
            frames = self.frames
        else:
            frames = [self.img]
        return frames
