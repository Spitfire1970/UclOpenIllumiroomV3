


from projection_modes.mode import Mode
from utils.settings_access import SettingsAccess
from utils.display_capture import DisplayCapture

from cv2 import blur

class Blur(Mode):
    
    def __init__(self, display_capture, audio_capture=None):
        self.blur_amount = self.get_blur_amount_from_settings()
        self.blur_tuple = (self.blur_amount, self.blur_amount)

        self.display_capture = display_capture
   

    def apply_mode_to_frame(self,frame):

        return blur(frame, self.blur_tuple ,0)

    def trigger(self):
        #Once triggered, screen record a frame, apply the blurring, then return the frame
        #frame = self.display_capture.capture_frame_no_resize()
        frame = self.display_capture.capture_frame_projector_resize()
        frame = self.apply_mode_to_frame(frame)
        return frame

    def get_blur_amount_from_settings(self):
        settings_access = SettingsAccess()
        mode_settings_json = settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["blur_amount"]
