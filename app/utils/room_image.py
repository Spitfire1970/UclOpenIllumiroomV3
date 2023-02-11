from .settings_access import SettingsAccess
from .display_capture import DisplayCapture

from .display_output import DisplayOutput

from .tv_detection import TVDetection

import os

from mss import mss
import cv2

import numpy as np
from cv2 import resize ,INTER_AREA
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSlot


import sys

class RoomImage:

    def __init__(
        self,
        settings_access,
        display_capture=None,
        ):
        self.settings_access = settings_access
        self.display_capture = display_capture
        
        self.image_path = None
        self.image_name = None
        self.app = None
        # self.app = QtWidgets.QApplication(sys.argv)

        # general_settings_json = settings_access.read_settings("general_settings.json")
        # selected_displays = general_settings_json["selected_displays"]

        selected_displays = settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = selected_displays["primary_display"]
        self.projector_bounding_box = selected_displays["projector_display"]


    def take_picture(self):
        app = QApplication(sys.argv)
        take_pic_window = DisplayOutput(self.primary_bounding_box, self.projector_bounding_box)
        # timer = QtCore.QTimer()
        # timer.timeout.connect(lambda: take_pic_window.label.setStyleSheet("background-color: rgb(74,78,84)"))
        # timer.start(50)
        take_pic_window.label.setStyleSheet("background-color: rgb(74,78,84)")
        
        while not take_pic_window.stopped:
            # take_pic_window.label.setStyleSheet("background-color: rgb(74,78,84)")
            app.processEvents()



    def upload_picture(self):
        app = QApplication(sys.argv)
        upload_pic_window = DisplayOutput(self.primary_bounding_box, self.projector_bounding_box, full_screen=False)


        @pyqtSlot()
        def open_dialog():
            self.image_path = QFileDialog.getOpenFileName(
                parent=upload_pic_window,
                caption="Select an image",
                directory="${HOME}",
                filter="Images (*.jpeg *.png *.jpg)",
            )[0]
            if len(self.image_path) != 0:
                btn.setText("Uploaded!")
                btn.setEnabled(False)
            # upload_pic_window.close()
            # sys.exit(app.exec())


        btn = QPushButton('Upload image of projected area')
        # btn.setText("Open file dialog")
        upload_pic_window.setCentralWidget(btn)
        btn.clicked.connect(open_dialog)

        while self.image_path is None or not upload_pic_window.stopped:
            app.processEvents()
        # sys.exit(app.exec())
        # upload_pic_window.close()


    def save_picture(self):
        self.upload_picture()
        # print(len(self.image_path))
        # self.image_name = self.image_path
        self.image_name = os.path.basename(self.image_path) #+ ".jpeg"

        img = cv2.imread(self.image_path)
        self.image_path = self.settings_access.room_img_path + self.image_name
        cv2.imwrite(self.image_path, img)

        # settings_JSON = self.settings_access.read_settings("general_settings.json")
        # self.settings_access.write_settings("general_settings.json", settings_JSON)


    def process_image(self, image_path):
        # Add black boundary filled box to the detected monitor
        image_without_TV = cv2.imread(image_path)
        start = self.settings_access.read_mode_settings("wobble", "tv_top_left")
        end = self.settings_access.read_mode_settings("wobble", "tv_bottom_right")
        cv2.rectangle(image_without_TV, (start[0], start[1]), (end[0], end[1]), (0, 0, 0), -1)
        # Save image of black boundary box replacing TV
        # cv2.imwrite("TV_box.jpeg", self.img)
        return image_without_TV

    def detect_primary_display(self):
        image_name = 'room_img1.jpg'
        image_path = self.settings_access.room_img_path + image_name
        image = cv2.imread(image_path)
        # image = self.read_room_image(resize=False)
        tv_detection = TVDetection(image, self.settings_access)
        image_without_TV = tv_detection.detect_tv()
        
        # Save image
        image_without_TV = self.process_image(image_path)
        # image_name = self.settings_access.read_settings("general_settings.json")["background_image_path"]
        # img_path = self.settings_access.get_image_path(image_name)
        # image_name = self.image_name
        # Resize image:
        # self.display_capture.frame_projector_resize(image_without_TV)
        # print(self.image_name, self.image_path)
        image_without_TV_path = self.settings_access.room_img_path + 'room_img1_noTV.jpg'
        cv2.imwrite(image_without_TV_path, image_without_TV)

        # Write image name to general settings JSON file
        settings_JSON = self.settings_access.read_settings("general_settings.json")
        settings_JSON["background_image_path"] = 'room_img1_noTV.jpg'
        self.settings_access.write_settings("general_settings.json", settings_JSON)


    #Read the room image, automatically resize to fit projector
    def read_room_image(self, resize=False):
        #Get the path of the image, prepend room_image, then get the fu
        image_name = self.settings_access.read_settings("general_settings.json")["background_image_path"]
        img_path = self.settings_access.get_image_path(image_name)
        img = cv2.imread(img_path)
        if resize:
            img = self.display_capture.frame_projector_resize(img)
        # cv2.imshow("img", img)
        return img


if __name__ == '__main__':
    settings = SettingsAccess()
    display = DisplayCapture()
    room = RoomImage(settings, display)

    room.take_picture()