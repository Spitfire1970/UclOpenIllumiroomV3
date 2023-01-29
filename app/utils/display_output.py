from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import imshow, namedWindow, setWindowProperty, waitKey, destroyAllWindows, WINDOW_NORMAL, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN
import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import time


class DisplayOutput(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.ui = QMainWindow()
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        
        self.stopped = False

    def closeEvent(self, event):
        self.stopped = True
        event.accept()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape or event.text() == QtCore.Qt.Key_Q:
            self.close()


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