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
        pass