from .settings_access import SettingsAccess
from mss import mss
import cv2

import numpy as np
from cv2 import resize ,INTER_AREA


class RoomImage:

    def __init__(
        self,
        settings_access,
        display_capture,
        ):
       self.settings_access = settings_access
       self.display_capture = display_capture

    #
    def capture_room_image(self):
        #Capture an image of the room, then save in assets/room_image

        #can potentially either use one name and overwrite each time, or save as a new image

        #Update general settings JSON File with new path to image
        pass
    
    #Read the room image, automatically resize to fit projector
    def read_room_image(self, resize):
        #Get the path of the image, prepend room_image, then get the fu
        image_name = self.settings_access.read_settings("general_settings.json")["background_image_path"]
        img_path = self.settings_access.get_image_path(image_name)
        img = cv2.imread(img_path)
        if resize:
            img = self.display_capture.frame_projector_resize(img)
        #cv2.imshow("img", img)
        return img


