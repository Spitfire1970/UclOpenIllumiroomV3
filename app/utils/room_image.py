#Class mostly deprecated, need to be removed
from .settings_access import SettingsAccess
from .display_capture import DisplayCapture

from .tv_detection import TVDetection
import os

import numpy as np
from cv2 import (
    namedWindow, setWindowProperty, 
    moveWindow, imshow, waitKey, destroyAllWindows,
    imread, imwrite, resize, rectangle, WND_PROP_FULLSCREEN, 
    WINDOW_FULLSCREEN, INTER_AREA
)


class RoomImage:

    def __init__(
        self,
        settings_access,
        display_capture=None,
        ):
        self.settings_access = settings_access
        
        self.image_path = None
        self.image_name = None
        self.app = None
        # self.app = QtWidgets.QApplication(sys.argv)

        # general_settings_json = settings_access.read_settings("general_settings.json")
        # selected_displays = general_settings_json["selected_displays"]

        selected_displays = settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = selected_displays["primary_display"]
        self.projector_bounding_box = selected_displays["projector_display"]
        self.display_capture = DisplayCapture(settings_access)


    def take_picture(self):
        height = self.projector_bounding_box['height']
        width = self.projector_bounding_box['width']
        image = np.zeros((height, width, 3), np.uint8)
        
        rgb_color = (74,78,84)
        colour = tuple(reversed(rgb_color))
        image[:] = colour
        
        window_name = "Capture projected area"
        # cv2.namedWindow(window_name)
        namedWindow(window_name, WND_PROP_FULLSCREEN)
        setWindowProperty(window_name, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)

        moveWindow(
            window_name, 
            self.projector_bounding_box['left'], 
            self.projector_bounding_box['top']
        )

        while True:
            imshow(window_name, image)
            k = waitKey(1)
            if k==27:    # Esc key to stop
                break
        destroyAllWindows()


    def process_image(self, image_path):
        # Add black boundary filled box to the detected monitor
        image_without_TV = imread(image_path)
        start = self.settings_access.read_mode_settings("wobble", "tv_top_left")
        end = self.settings_access.read_mode_settings("wobble", "tv_bottom_right")
        rectangle(image_without_TV, (start[0], start[1]), (end[0], end[1]), (0, 0, 0), -1)
        return image_without_TV

    def detect_primary_display(self):
        image_name = 'room_img.jpg'
        image_path = self.settings_access.room_img_path + image_name
        if not os.path.exists(image_path):
            print("Invalid image name. Please save the picture of the projected area " 
            + "with the name: room_img.jpg")
            return

        image = imread(image_path)
        # Resize image to fit projector's size
        dim = (self.projector_bounding_box['width'], self.projector_bounding_box['height'])
        image = resize(image, dim, interpolation=INTER_AREA)
        imwrite(image_path, image)

        tv_detection = TVDetection(image, self.settings_access)
        image_without_TV = tv_detection.detect_tv()
        
        # Save image
        image_without_TV = self.process_image(image_path)

        image_without_TV_path = self.settings_access.room_img_path + 'room_img_noTV.jpg'
        imwrite(image_without_TV_path, image_without_TV)

        # Write image name to general settings JSON file
        settings_JSON = self.settings_access.read_settings("general_settings.json")
        settings_JSON["background_image_path"] = 'room_img_noTV.jpg'
        self.settings_access.write_settings("general_settings.json", settings_JSON)


    #Read the room image, automatically resize to fit projector
    def read_room_image(self, resize=False):
        #Get the path of the image, prepend room_image, then get the fu
        image_name = self.settings_access.read_settings("general_settings.json")["background_image_path"]
        img_path = self.settings_access.get_image_path(image_name)
        img = imread(img_path)
        if resize:
            img = self.display_capture.frame_projector_resize(img)
        # cv2.imshow("img", img)
        return img


if __name__ == '__main__':
    settings = SettingsAccess()
    display = DisplayCapture()
    room = RoomImage(settings, display)

    room.take_picture()