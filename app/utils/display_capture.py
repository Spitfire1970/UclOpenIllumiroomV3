from .settings_access import SettingsAccess
from mss import mss


import numpy as np
import cv2


class DisplayCapture:

    def __init__(self, display_bounding_box):
        self.sct = mss()
        self.display_bounding_box = display_bounding_box


    def capture_frame(self):
        frame = self.sct.grab(self.display_bounding_box)
        return frame