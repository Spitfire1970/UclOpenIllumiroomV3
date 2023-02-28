from projection_modes.mode import Mode
from utils.settings_access import SettingsAccess

from cv2 import blur, rectangle

class Blur(Mode):

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
        self.projector_bounding_box = display_capture.get_projector_bounding_box()
        self.rect_color = self.get_blur_edge_rect_from_settings()
        height_factor = 128
        width_factor = 196
        self.top_rect_coords = [0,0,int(self.projector_bounding_box['width']),int(self.projector_bounding_box['height']/height_factor)]
        self.bottom_rect_coords = [0,int(self.projector_bounding_box['height']*(height_factor-1)/height_factor),int(self.projector_bounding_box['width']),int(self.projector_bounding_box['height'])]
        self.left_rect_coords = [0,0,int(self.projector_bounding_box['width']/width_factor),int(self.projector_bounding_box['height'])]
        self.right_rect_coords = [int(self.projector_bounding_box['width']*(width_factor-1)/width_factor),0,int(self.projector_bounding_box['width']),int(self.projector_bounding_box['height'])]
        

    def add_rectangles_to_frame(self, frame):
        #Top rectangle
        rectangle(frame, (self.top_rect_coords[0], self.top_rect_coords[1]), (self.top_rect_coords[2], self.top_rect_coords[3]), self.rect_color, -1)
        rectangle(frame, (self.bottom_rect_coords[0], self.bottom_rect_coords[1]), (self.bottom_rect_coords[2], self.bottom_rect_coords[3]), self.rect_color, -1)
        rectangle(frame, (self.left_rect_coords[0], self.left_rect_coords[1]), (self.left_rect_coords[2], self.left_rect_coords[3]), self.rect_color, -1)
        rectangle(frame, (self.right_rect_coords[0], self.right_rect_coords[1]), (self.right_rect_coords[2], self.right_rect_coords[3]), self.rect_color, -1)
        #frame = blur(frame, self.blur_tuple ,0)
        return frame

    def apply_mode_to_frame(self,frame):
        #Add rectangles at edges:
        #frame = self.add_rectangles_to_frame(frame)
        return blur(frame, self.blur_tuple ,0)

    def trigger(self):
        #Once triggered, screen record a frame, apply the blurring, then return the frame
        
        frames = [None]
        #frame= self.display_capture.capture_frame_projector_resize()
        frame = self.display_capture.capture_frame()
        frames[0] = self.apply_mode_to_frame(frame)
        return frames

    def get_blur_amount_from_settings(self):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["blur_amount"]

    def get_blur_edge_rect_from_settings(self):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")
        return mode_settings_json["blur"]["edge_rect_colour"]
