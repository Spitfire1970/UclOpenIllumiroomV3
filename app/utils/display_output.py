from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import imshow, namedWindow, setWindowProperty, waitKey, destroyAllWindows, WINDOW_NORMAL, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN

class DisplayOutput:

    def __init__(self):
        pass


    def display_frame(self, frames):
        #Setup the display window
        namedWindow("UCL Open Illumiroom V2", WINDOW_NORMAL)
        setWindowProperty("UCL Open Illumiroom V2", WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
        for frame in frames:
            imshow('UCL Open Illumiroom V2', frame)
        if (waitKey(1) & 0xFF) == ord('q'):
            destroyAllWindows()
            return True
        return False