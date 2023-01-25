from .settings_access import SettingsAccess
from mss import mss


import numpy as np
import cv2

class DisplayOutput:

    def __init__(self):
        pass


    def display_frame(self, frame):
        cv2.imshow('UCL Open Illumiroom V2', np.array(frame))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            return True
        return False