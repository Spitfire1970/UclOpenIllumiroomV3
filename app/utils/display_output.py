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
    def __init__(self, primary_bounding_box, projector_bounding_box, full_screen=True):
        super().__init__()
        # self.ui = QMainWindow()

        
        self.primary_bounding_box = primary_bounding_box
        self.projector_bounding_box = projector_bounding_box

        self.exit_key_binding = Qt.Key.Key_Escape.value
              
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        self.setWindowTitle("UCL Open-Illumiroom V2")


        # #Move to the mss coordinates of the projector 
        # projector_left = int(projector_bounding_box['left'] )
        # projector_top = projector_bounding_box['top']

        self.move(projector_bounding_box['left'], projector_bounding_box['top'])
        if full_screen:
            self.showFullScreen()
        else:
            self.show()
        print("-------------------------------------------------------------")
        print("Window Opened, press Escape in the illumiroom window to exit")
        print("If you have an issue with the image fitting, please ensure that your projector is at 100% scaling")
        
        self.stopped = False
        return 

    
    def keyPressEvent(self, event):
        if event.key() == self.exit_key_binding:
            # print("Thank you for using UCL-Open Illumiroom V2")
            # print("Have a great day!")
            self.stopped = True
            self.close()

