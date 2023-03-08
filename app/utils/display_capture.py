from mss import mss
import numpy as np
from cv2 import resize, INTER_AREA


class DisplayCapture:

    def __init__(self, settings_access):
        self.sct = mss()
        self.settings_access = settings_access
        self.selected_displays = settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = self.selected_displays["primary_display"]
        self.projector_bounding_box = self.selected_displays["projector_display"]
        self.projector_resize_scale_factor = self.projector_bounding_box['width']/self.primary_bounding_box['width']
        self.primary_resize_scale_factor = self.projector_bounding_box['width']/self.primary_bounding_box['width']

        """
        self.capture_card_settings = settings_access.read_general_settings("capture_card")
        self.use_capture_card = self.capture_card_settings["use_capture_card"]
        self.capture_card_num = self.capture_card_settings["capture_card_num"]
        if self.use_capture_card:
            self.capture_card = cv2.VideoCapture(self.capture_card_num,cv2.CAP_DSHOW)
            self.capture_card.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.capture_card.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        """

        

    #Capture a frame from the primary display, remove the alpha channel
    def capture_frame(self):
        frame = np.array(self.sct.grab(self.primary_bounding_box))[:,:,:3]
    
        return frame

    #Captures a frame from a specified bounding box
    def capture_frame_with_bounding_box(self, bounding_box):
        frame = np.array(self.sct.grab(bounding_box))[:,:,:3]

        return frame


    def get_projector_bounding_box(self):
        return self.projector_bounding_box
    
    def get_primary_bounding_box(self):
        return self.primary_bounding_box
    

    def frame_projector_resize(self, frame):
        #Check if frame needs to be resized
        if (self.monitor_resize_scale_factor) > 1.05 or (self.monitor_resize_scale_factor) < 0.95 :
            frame = self.resize_image_fit_projector(frame)
        return frame
    
    

    def resize_image_fit_projector(self,frame):
        #Resize an image from the primary display to fit the projector display,
        #use monitor resize scale factor which is projector width / primary width
        height = frame.shape[0]
        width = frame.shape[1]

        width = int(width * self.monitor_resize_scale_factor)
        height = int(height * self.monitor_resize_scale_factor)
        dim = (width, height)
        # resize image
        return resize(frame, dim, interpolation = INTER_AREA)
    

    def resize_image_fit_projector_each_frame(self,frame):
        #Resizes the image to fit on the projector, but based on the frame's height/width rather than the 
        #Primary display's - Useful for resizing images.
        height = frame.shape[0]
        width = frame.shape[1]
        scale_factor_w = self.projector_bounding_box["width"]/width
        scale_factor_h = self.projector_bounding_box["height"]/height
        #print("factors",scale_factor_w, ",",scale_factor_h)
        width = int(width * scale_factor_w)
        height = int(height * scale_factor_h)
        dim = (width, height)
        # resize image
        return resize(frame, dim, interpolation = INTER_AREA)
    


    def frame_primary_resize(self, frame):
        #Resize a frame to fit on the primary display, based on the frame's size
        height, width = frame.shape[:2]
        self.primary_resize_scale_factor = self.primary_bounding_box['width']/width 
        if (self.primary_resize_scale_factor) > 1.05 or (self.primary_resize_scale_factor) < 0.95 :
            frame = self.resize_image_fit_primary(frame)
        return frame

    def resize_image_fit_primary(self,frame):
        #Resize a frame to fit on the primary display, based on the frame's size
        height = frame.shape[0]
        width = frame.shape[1]

        width = int(width * self.primary_resize_scale_factor)
        height = int(height * self.primary_resize_scale_factor)
        dim = (width, height)
        # resize image
        return resize(frame, dim, interpolation = INTER_AREA)