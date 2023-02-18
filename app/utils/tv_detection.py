import cv2
# # Note: window displayed using cv2.imshow, TODO: change this
# from utils.settings_access import SettingsAccess

# # TODO: consider other modes like snow
MODE = "wobble"

class TVDetection():
    def __init__(self, image, settings_access) -> None:
        self.img = image
        self.top_left = None
        self.bottom_right = None
        self.settings_access = settings_access
    
    def update_mode_settings(self, settings, new_data):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")

        for i in range(len(settings)):
            mode_settings_json[MODE][settings[i]] = new_data[i]
        
        self.settings_access.write_settings("mode_settings.json", mode_settings_json)
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

        self.update_mode_settings(settings, new_values)
        # return center_x, center_y

    def detect_tv(self):
        cv2.namedWindow("Detect TV")
        cv2.setMouseCallback("Detect TV", self.on_mouse)
        while True:
            cv2.imshow("Detect TV", self.img)
            key = cv2.waitKey(1)
            if key == ord("q") and self.top_left is not None:
                break
            elif key == ord("q") and self.top_left is None:
                print("Please select your primary monitor before exiting!")
                pass
        cv2.destroyAllWindows()
        for i in range (1,5):
            cv2.waitKey(1)

        self.calc_center()
        return self.img



# import sys
# from PyQt6 import QtGui, QtCore
# from utils.settings_access import SettingsAccess

# from PyQt6 import QtWidgets

# # TODO: consider other modes like snow
# MODE = "wobble"

# class TVDetection(QtWidgets.QMainWindow):
#     def __init__(self, image, settings_access, parent=None):
#         super().__init__(parent)
#         self.img = image
#         self.top_left = None
#         self.bottom_right = None
#         self.settings_access = settings_access

#         self.setWindowTitle("Detect TV")
#         self.label = QtWidgets.QLabel(self)
#         height, width = image.shape[:2]
#         bytes_per_line = image.strides[0]
#         qImg = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
#         self.label.setPixmap(QtGui.QPixmap(qImg))

#         self.mouse_pressed = False

#     def update_mode_settings(self, settings, new_data):
#         mode_settings_json = self.settings_access.read_settings("mode_settings.json")

#         for i in range(len(settings)):
#             mode_settings_json[MODE][settings[i]] = new_data[i]

#         self.settings_access.write_settings("mode_settings.json", mode_settings_json)

#     def mousePressEvent(self, event):
#         self.top_left = (event.x(), event.y())
#         self.mouse_pressed = True

#     def mouseReleaseEvent(self, event):
#         self.bottom_right = (event.x(), event.y())
#         self.mouse_pressed = False
#         self.update()

#     def paintEvent(self, event):
#         qp = QtGui.QPainter()
#         qp.begin(self)
#         if self.mouse_pressed:
#             qp.setPen(QtGui.QPen(QtCore.Qt.green, 2))
#             qp.drawRect(QtCore.QRect(self.top_left[0], self.top_left[1],
#                                      self.bottom_right[0] - self.top_left[0],
#                                      self.bottom_right[1] - self.top_left[1]))
#         qp.end()

#     def calc_center(self):
#         center_x = int((self.top_left[0] + self.bottom_right[0]) / 2)
#         center_y = int((self.top_left[1] + self.bottom_right[1]) / 2)
#         # TODO: handle exceptions

#         settings = ["tv_top_left", "tv_bottom_right", "tv_center_x", "tv_center_y"]
#         new_values = [self.top_left, self.bottom_right, center_x, center_y]

#         self.update_mode_settings(settings, new_values)

#     def detect_tv(self):
#         self.show()

# # if __name__ == '__main__':
# #     app = QtGui.QApplication(sys.argv)
# #     tv_detection = TVDetection(QtGui.QImage("image.jpg"), SettingsAccess())
# #     tv_detection.detect_tv()
# #     sys.exit(app.exec_())
