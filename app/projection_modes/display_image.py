from .mode import Mode
import cv2


class DisplayImage(Mode):
    """
    The Display image mode projects a single image to the projection screen. 
    display_image is useful for simple demonstrations that do not require interaction

    Attributes:
        img_path: path to the image file
        img: The image file 
    Methods:
        trigger(self):
            Display the image that was loaded in.

    """
    
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture=None
        ):
        self.settings_access = settings_access
        self.img_path = self.settings_access.get_assets_path() +"display_image\\"+ self.settings_access.read_mode_settings("display_image","display_image_file")
        self.img = cv2.imread(self.img_path)

    def trigger(self):        
        """
        Triggers the display image mode and returns the captured frames.

        Returns:
            frames (list): A list of captured frames, which contains only display image
        """    
        frames = [self.img]
        return frames
