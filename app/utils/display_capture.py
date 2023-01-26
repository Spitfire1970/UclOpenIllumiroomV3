from .settings_access import SettingsAccess
from mss import mss


import numpy as np
from cv2 import resize ,INTER_AREA


class DisplayCapture:

    def __init__(self, primary_bounding_box, projector_bounding_box):
        self.sct = mss()
        self.primary_bounding_box = primary_bounding_box
        self.projector_bounding_box = projector_bounding_box

        self.monitor_resize_scale_factor = self.projector_bounding_box['width']/self.primary_bounding_box['width']

    #Use no resize if the image captured will not be directly displayed
    def capture_frame_no_resize(self):
        frame = np.array(self.sct.grab(self.primary_bounding_box))
        return frame

    def capture_frame_projector_resize(self):
        frame = np.array(self.sct.grab(self.primary_bounding_box))
        #Check if the resolution of the primary monitor and TV differ (ratio not 1)
        if (self.monitor_resize_scale_factor) > 1.05 or (self.monitor_resize_scale_factor) < 0.95 :
            frame = self.resize_image_fit_projector(frame)

        return frame

    def resize_image_fit_projector(self,frame):
        #If the projector and the tv have different resolutions, quite possible if a 4k tv is being used 
        # The image from the tv needs to be resized to fit onto the projector, otherwise full size image will be shown
        height, width, channels = frame.shape
        width = int(width * self.monitor_resize_scale_factor)
        height = int(height * self.monitor_resize_scale_factor)
        dim = (width, height)
        # resize image
        return resize(frame, dim, interpolation = INTER_AREA)