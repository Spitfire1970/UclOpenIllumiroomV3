from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import imshow, namedWindow, setWindowProperty, waitKey, resize, destroyAllWindows, WINDOW_NORMAL, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN, INTER_AREA
import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage,QScreen, QScreen
from PyQt6.QtCore import Qt

import time


class DisplayOutput(QtWidgets.QMainWindow):
    def __init__(self, settings_access):
        # Create PyQt app, only ever needs to be defined once
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.settings_access = settings_access
        self.full_screen = self.settings_access.read_general_settings("full_screen")
        self.selected_displays = self.settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = self.selected_displays["primary_display"]
        self.projector_bounding_box = self.selected_displays["projector_display"]

        self.selected_mode = self.settings_access.read_general_settings("selected_mode")
        
        self.format_string = settings_access.read_mode_settings(self.selected_mode, "qImg_format")
        self.qImg_format = eval(self.format_string)

        self.icon_path = settings_access.get_assets_path()+'/logo/UCL-ICON-LOGO.ico'

        #Key binding to exit the app - set to Key_Escape
        self.exit_key_binding = Qt.Key.Key_Escape.value

        #Set up the PyQT window
        self.label = QtWidgets.QLabel(self)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)
        self.setWindowTitle("UCL Open-Illumiroom V2")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        self.monitor_resize_scale_factor = self.projector_bounding_box['width']/self.primary_bounding_box['width']


        #Move the PyQT window to the position of the projector display, as defined by windows and returned by MSS
        self.move(self.projector_bounding_box['left'], self.projector_bounding_box['top'])
        if self.full_screen:
            self.showFullScreen()
        else:
            self.show()
        print("-------------------------------------------------------------")
        print("Window Opened, press Escape in the illumiroom window to exit")
        print("If you have an issue with the image fitting, please ensure that your projector is at 100% scaling")
        
        self.stopped = False
        return 

    def display_frame(self, frame):

        #Display the supplied frame on the projecot, resizing if necessary
        frame = self.frame_projector_resize(frame)
        height, width = frame.shape[:2]
        bytes_per_line = frame.strides[0]

        #PyQT processing for display
        qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, self.qImg_format).rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap(qImg))
        self.app.processEvents()
    
    #Define key press events
    def keyPressEvent(self, event):

        #Exit binding
        if event.key() == self.exit_key_binding:
            self.stopped = True
            self.close()




    def frame_projector_resize(self, frame):
        #Check if the resolution of the primary monitor and TV differ (ratio not 1), if do not 
        #resizing not required
        if (self.monitor_resize_scale_factor) > 1.05 or (self.monitor_resize_scale_factor) < 0.95 :
            frame = self.resize_image_fit_projector(frame)
        return frame

    def resize_image_fit_projector(self,frame):
        #If the projector and the tv have different resolutions, quite possible if a 4k tv is being used 
        # The image from the tv needs to be resized to fit onto the projector, otherwise full size image will be shown

        #Function copied across from display capture.
        height = frame.shape[0]
        width = frame.shape[1]

        width = int(width * self.monitor_resize_scale_factor)
        height = int(height * self.monitor_resize_scale_factor)
        dim = (width, height)
        # resize image
        return resize(frame, dim, interpolation = INTER_AREA)
