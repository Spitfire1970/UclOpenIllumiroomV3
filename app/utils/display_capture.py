from mss import mss
import numpy as np
from cv2 import resize, INTER_AREA


class DisplayCapture:
    """
    Display capture is a class used for capturing the screen content of a projector and primary display
    """

    def __init__(self, settings_access):
        self.sct = mss()
        self.settings_access = settings_access
        self.selected_displays = settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = self.selected_displays["primary_display"]
        self.projector_bounding_box = self.selected_displays["projector_display"]
        self.projector_resize_scale_factor = self.projector_bounding_box['width'] / self.primary_bounding_box['width']

        
        """
        A capture card can be used instead of the primary display, however the frame rate when tested was very low.
        Perhaps trying again with the elgato capture card would be better.

        self.capture_card_settings = settings_access.read_general_settings("capture_card")
        self.use_capture_card = self.capture_card_settings["use_capture_card"]
        self.capture_card_num = self.capture_card_settings["capture_card_num"]
        if self.use_capture_card:
            self.capture_card = cv2.VideoCapture(self.capture_card_num,cv2.CAP_DSHOW)
            self.capture_card.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.capture_card.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        """

    def capture_frame(self):
        """
        Capture frame from primary display, removing the alpha channel
        :return: Frame from primary display
        """
        frame = np.array(self.sct.grab(self.primary_bounding_box))[:, :, :3]
        return frame

    def capture_frame_with_bounding_box(self, bounding_box):
        """
        Capture a specified part of primary display
        :param bounding_box: Bounding box to capture
        :return: Specified part of primary display frame
        """
        frame = np.array(self.sct.grab(bounding_box))[:, :, :3]

        return frame

    def get_projector_bounding_box(self):
        return self.projector_bounding_box

    def get_primary_bounding_box(self):
        return self.primary_bounding_box

    def resize_image_fit_projector_each_frame(self, frame):
        """
        Resize frame to fully fit projector
        :param frame: Frame to be resized
        :return: Resized frame
        """
        return resize(frame, (self.projector_bounding_box["width"], self.projector_bounding_box["height"]), interpolation=INTER_AREA)

    def frame_projector_resize(self, frame):
        """
        Resize the frame to projector width
        :param frame: Frame to be resized
        :return: Resized frame, or unchanged frame if resizing isn't needed
        """
        height, width = frame.shape[:2]
        resize_factor = self.projector_bounding_box['width'] / width
        if resize_factor > 1.05 or resize_factor < 0.95:
            return resize(frame, (self.projector_bounding_box['width'], int(height * resize_factor)), interpolation=INTER_AREA)
        return frame

    def frame_primary_resize(self, frame):
        """
        Resize the frame to primary display width
        :param frame: Frame to be resized
        :return: Resized frame, or unchanged frame if resizing isn't needed
        """
        height, width = frame.shape[:2]
        resize_factor = self.primary_bounding_box['width'] / width
        if resize_factor > 1.05 or resize_factor < 0.95:
            return resize(frame, (self.primary_bounding_box['width'], int(height * resize_factor)), interpolation=INTER_AREA)
        return frame
