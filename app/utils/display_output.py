from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import imshow, namedWindow, setWindowProperty, waitKey, destroyAllWindows, WINDOW_NORMAL, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN
import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage,QScreen, QScreen
from PyQt6.QtCore import Qt

import time


class DisplayOutput(QtWidgets.QMainWindow):
    def __init__(self, primary_bounding_box, projector_bounding_box):
        super().__init__()
        # self.ui = QMainWindow()
        self.primary_bounding_box = primary_bounding_box
        self.projector_bounding_box = projector_bounding_box

        self.exit_key_binding = Qt.Key.Key_Escape.value
        display_monitor = 1

        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
              
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)

        #Move to the mss coordinates of the projector 
        projector_left = projector_bounding_box['left']
        projector_top = projector_bounding_box['top']

        self.move(projector_left, projector_top)
        self.showFullScreen()

        print("Window Opened, press Escape in the illumiroom window to exit")
        
        self.stopped = False
        return 

    
    def keyPressEvent(self, event):
        if event.key() == self.exit_key_binding:
            print("Thank you for using UCL-Open Illumiroom V2")
            print("Have a great day!")
            self.close()
            exit()


# class DisplayOutput:

#     def __init__(self):
#         pass

#     def display_frame(self, frames):
#         #Setup the display window
#         namedWindow("UCL Open Illumiroom V2", WINDOW_NORMAL)
#         # setWindowProperty("UCL Open Illumiroom V2", WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
#         for frame in frames:
#             imshow('UCL Open Illumiroom V2', frame)
#         if (waitKey(1) & 0xFF) == ord('q'):
#             destroyAllWindows()
#             return True
#         return False