# import cv2
# Note: window displayed using cv2.imshow, TODO: change this
from utils.settings_access import SettingsAccess

# TODO: consider other modes like snow
MODE = "wobble"

class TVDetection():
    def __init__(self, image) -> None:
        self.img = image
        self.top_left = None
        self.bottom_right = None
    
    def update_mode_settings(self, mode, settings, new_data):
        settings_access = SettingsAccess()
        mode_settings_json = settings_access.read_settings("mode_settings.json")

        for i in range(len(settings)):
            mode_settings_json[mode][settings[i]] = new_data[i]
        
        settings_access.write_settings(self, "mode_settings.json", mode_settings_json)
        # return mode_settings_json[mode][setting]


    def on_mouse(self, event, x, y, flags, params):
        # Allow user to create a boundary box for the TV
        if event == cv2.EVENT_LBUTTONDOWN:
            self.top_left = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.bottom_right = (x, y)
            cv2.rectangle(self.img, self.top_left, self.bottom_right, (0, 255, 0), 2)
            cv2.imshow("Detect TV", self.img)

    def calc_center(self):
        # Calculate the center of the TV
        center_x = int((self.top_left[0] + self.bottom_right[0]) / 2)
        center_y = int((self.top_left[1] + self.bottom_right[1]) / 2)
        # TODO: handle exceptions

        settings = ["tv_top_left", "tv_bottom_right", "tv_center_x", "tv_center_y"]
        new_values = [self.top_left, self.bottom_right, center_x, center_y]

        self.update_mode_settings(MODE, settings, new_values)
        # return center_x, center_y

    def detect_tv(self):
        cv2.namedWindow("Detect TV")
        cv2.setMouseCallback("Detect TV", self.on_mouse)
        while True:
            cv2.imshow("Detect TV", self.img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        self.calc_center()
