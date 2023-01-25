from .settings_access import SettingsAccess
from mss import mss


import numpy as np
import cv2

class DisplayOutput:

    def __init__(self):
        pass


    def display_frame(self, frame):
        #Setup the display window
        cv2.namedWindow("UCL Open Illumiroom V2", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("UCL Open Illumiroom V2", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('UCL Open Illumiroom V2', frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            return True
        return False