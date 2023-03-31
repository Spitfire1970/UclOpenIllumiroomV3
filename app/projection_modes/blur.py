from projection_modes.mode import Mode
from utils.settings_access import SettingsAccess

from cv2 import blur, rectangle

class Blur(Mode):

    """
    The Blur mode blurs the content shown on the primary display/TV, and projects the blurred content onto the projector.

    Attributes:
        blur_amount: Blur amount to be applied to the frame, stored in settings
        blur_tuple: Blur amount combined twice into a tuple.
    Methods:
        apply_mode_to_frame(self, frame):
            Applies the blur to the frame.
        trigger(self):
            Gets a frame from the display capture, applies the blur, and returns the frame.

    """

    def __init__(
        self, 
        settings_access, 
        display_capture, 
        background_img=None, 
        audio_capture=None
    ):
        self.settings_access = settings_access
        self.blur_amount = self.get_blur_amount_from_settings()
        self.blur_tuple = (self.blur_amount, self.blur_amount)

        self.display_capture = display_capture
        
        

    def apply_mode_to_frame(self,frame):

        """
            Applies blurring to the given frame according to the blur tuple stored in the object attribute

            Prameters:
                frame : The frame to which the blurring is to be applied.

            Returns:
                 The frame after applying the blurring.
        """
        return blur(frame, self.blur_tuple ,0)

    def trigger(self):
        """
            Triggers the object to capture the current screen display, apply the blurring, and return the resulting frame.

            Returns:
                A list containing the single blurred frame.
        """
        frame = self.display_capture.capture_frame()
        frame = self.apply_mode_to_frame(frame)
        return [frame]

    def get_blur_amount_from_settings(self):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["blur_amount"]

    def get_blur_edge_rect_from_settings(self):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["edge_rect_colour"]
