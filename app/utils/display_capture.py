from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import resize ,INTER_AREA
import cv2


class DisplayCapture:

    def __init__(self, settings_access):
        self.sct = mss()
        self.settings_access = settings_access
        self.selected_displays = settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = self.selected_displays["primary_display"]
        self.projector_bounding_box = self.selected_displays["projector_display"]

        """
        self.capture_card_settings = settings_access.read_general_settings("capture_card")
        self.use_capture_card = self.capture_card_settings["use_capture_card"]
        self.capture_card_num = self.capture_card_settings["capture_card_num"]
        if self.use_capture_card:
            self.capture_card = cv2.VideoCapture(self.capture_card_num,cv2.CAP_DSHOW)
            self.capture_card.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.capture_card.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        """

        

    #Use no resize if the image captured will not be directly displayed
    def capture_frame(self):
        # if self.use_capture_card:
        #     result, frame = self.capture_card.read()
        # else:
        #     
        frame = np.array(self.sct.grab(self.primary_bounding_box))[:,:,:3]
    
        return frame

    #Use no resize if the image captured will not be directly displayed
    def capture_frame_with_bounding_box(self, bounding_box):
        frame = np.array(self.sct.grab(bounding_box))[:,:,:3]

        return frame


    def get_projector_bounding_box(self):
        return self.projector_bounding_box
    
    def get_primary_bounding_box(self):
        return self.primary_bounding_box