from projection_modes.mode import Mode
from utils.settings_access import SettingsAccess

from cv2 import blur

class Blur(Mode):

    def __init__(
        self, 
        settings_access, 
        display_capture, 
        background_img=None, 
        audio_capture=None
    ):
        self.blur_amount = self.get_blur_amount_from_settings()
        self.blur_tuple = (self.blur_amount, self.blur_amount)

        self.display_capture = display_capture
   

    def apply_mode_to_frame(self,frame):

        return blur(frame, self.blur_tuple ,0)

    def trigger(self):
        #Once triggered, screen record a frame, apply the blurring, then return the frame
        #frame = self.display_capture.capture_frame_no_resize()
        frames = [None]
        frame= self.display_capture.capture_frame_projector_resize()
        frames[0] = self.apply_mode_to_frame(frame)
        return frames

    def get_blur_amount_from_settings(self):
        settings_access = SettingsAccess()
        mode_settings_json = settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["blur_amount"]
