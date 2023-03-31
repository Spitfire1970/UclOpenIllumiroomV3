import os

from cv2 import (
    resize, INTER_AREA, FileStorage, 
    FILE_STORAGE_READ, remap, INTER_LINEAR
)
import sys
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt


class DisplayOutput(QtWidgets.QMainWindow):
    """
    DisplayOutput is a class used for displaying and resizing frames for use with the projector and main display
    """
    def __init__(self, settings_access):
        # Create PySide app, only ever needs to be defined once
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.settings_access = settings_access
        self.full_screen = self.settings_access.read_general_settings("full_screen")
        self.use_calibration = self.settings_access.read_general_settings("use_calibration")
        self.calibration_map1 = None
        self.calibration_map2 = None
        if self.use_calibration:
            fs = FileStorage(os.path.join(settings_access.assets_path,
                                          "calibration/grey_code_photos/grey_code/map.ext"), FILE_STORAGE_READ)
            self.calibration_map1 = fs.getNode("map1").mat()
            self.calibration_map2 = fs.getNode("map2").mat()
            fs.release()
        if self.calibration_map1 is None or self.calibration_map2 is None:
            self.use_calibration = False
        self.selected_displays = self.settings_access.read_general_settings("selected_displays")
        self.primary_bounding_box = self.selected_displays["primary_display"]
        self.projector_bounding_box = self.selected_displays["projector_display"]

        self.selected_mode = self.settings_access.read_general_settings("selected_mode")

        self.format_string = settings_access.read_mode_settings(self.selected_mode, "qImg_format")
        self.qImg_format = eval(self.format_string)

        self.icon_path = settings_access.get_assets_path() + '/logo/UCL-ICON-LOGO.ico'

        # Key binding to exit the app - set to Key_Escape
        self.exit_key_binding = Qt.Key.Key_Escape

        # Set up the PySide window
        self.label = QtWidgets.QLabel(self)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)
        self.setWindowTitle("UCL Open-Illumiroom V2")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        self.monitor_resize_scale_factor = self.projector_bounding_box['width'] / self.primary_bounding_box['width']

        # Move the PySide window to the position of the projector display, as defined by windows and returned by MSS
        self.move(self.projector_bounding_box['left'], self.projector_bounding_box['top'])
        if self.full_screen:
            self.showFullScreen()
        else:
            self.show()
        print("-------------------------------------------------------------")
        print("Window Opened, press Escape in the illumiroom window to exit")
        print("If you have an issue with the image fitting, please ensure that your projector is at 100% scaling")

        self.stopped = False
        return

    def display_frame(self, frame):
        """
        Display image on the projector, resizing to fit
        :param frame: Frame to display
        """
        frame = self.frame_projector_resize(frame)
        if self.use_calibration:
            frame = remap(frame, self.calibration_map1, self.calibration_map2, INTER_LINEAR)
        height, width = frame.shape[:2]
        bytes_per_line = frame.strides[0]

        # PySide processing for display
        qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, self.qImg_format).rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap(qImg))
        self.app.processEvents()

    # Define key press events
    def keyPressEvent(self, event):

        # Exit binding
        if event.key() == self.exit_key_binding:
            self.stopped = True
            self.close()

    def frame_projector_resize(self, frame):
        """
        Resize the frame to projector size
        :param frame: Frame to be resized
        :return: Resized frame, or unchanged frame if resizing isn't needed
        """
        height, width = frame.shape[:2]
        resize_factor = self.projector_bounding_box['width'] / width
        if resize_factor > 1.05 or resize_factor < 0.95:
            return resize(frame, (self.projector_bounding_box['width'], int(height * resize_factor)), interpolation=INTER_AREA)
        return frame
