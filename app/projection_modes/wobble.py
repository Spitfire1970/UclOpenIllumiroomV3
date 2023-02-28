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
            cv2.rectangle(mask, top_left_coords, bottom_right_coors, (255, 255, 255), -1)

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
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
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
        self.num_frames = self.settings.read_mode_settings("wobble", "num_frames")

        self.output_img = np.zeros_like(self.img)
        height, width = self.img.shape[:2]
        self.x, self.y = np.meshgrid(np.arange(width), np.arange(height))
        self.original_x, self.original_y = self.x.copy(), self.y.copy()
        self.fractal_amplitude = self.settings.read_mode_settings("wobble", "fractal_amplitude")

        self.threshold = self.settings.read_mode_settings("wobble", "sound_threshold")

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
            cv2.rectangle(mask, top_left_coords, bottom_right_coors, (255, 255, 255), -1)

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
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        # if self.audio_capture.detect_loud_sound():
        if self.audio_capture.detect_explosive_sound():
            # print("Loud sound")
            frames = self.frames
        else:
            # print("No loud sound")
            frames = [self.img]
        return frames
"""
