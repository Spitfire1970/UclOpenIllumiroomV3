from .mode import Mode
import numpy as np
import cv2
from pathlib import Path

class Cartoon(Mode):
    def __init__(
            self,
            settings_access: object,  # An object that provides access to the settings of the application.
            display_capture: object,  # A display capture object.
            background_img: np.ndarray,  # A numpy array representing the background image to be used.
            audio_capture: object = None  # An optional audio capture object.
        ):
        """
        Initialize a Cartoon object.

        settings_access (object): An object that provides access to the settings of the application.
        display_capture (object): A display capture object.
        background_img (numpy.ndarray): A numpy array representing the background image to be used.
        audio_capture (object): An optional audio capture object. Defaults to None.
        """
        self.settings_access = settings_access
        self.img = background_img

    def cartoonify(self):
        """
        Cartoonify the background image using edge detection and color filters.
        """
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        # Detect edges in image, create colour image
        edges = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                    cv2.THRESH_BINARY,11, 7
                )
        colour = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        colour[np.where((colour == [0,0,0]).all(axis = 2))] = [0, 0, 0]

        colour = cv2.bilateralFilter(colour, 9, 300, 300)

        # Merge original image with edge image
        self.img = cv2.addWeighted(self.img, 0.9, colour, 0.2, -40)


    def trigger(self):
        """
        Generate and return a cartoon view of the background image.

        Returns:
        list: A list containing the cartoon view of the background image.
        """
        # Save image
        # cartoon_img_name = (__file__[:__file__.index("app")
        #     + len("app")]+"/assets/generated/cartoon_view.jpeg")
        #All images are stored in the assets folder
        cartoon_img_name = self.settings_access.assets_path + "generated\cartoon_view.jpeg"
        cartoon_img = Path(cartoon_img_name)
        if cartoon_img.is_file():
            self.img = cv2.imread(cartoon_img_name)
        else: 
            self.cartoonify()
            cv2.imwrite(cartoon_img_name, self.img)

        frames = [self.img]
        return frames
