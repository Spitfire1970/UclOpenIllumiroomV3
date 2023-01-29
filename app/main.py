# 1) User runs main
# 2) Menu is opened for the user, can update settings eg: their primary and 
# projector displays and other settings

import sys
import time
import numpy as np
import cv2
from PyQt6 import QtWidgets, QtGui

from utils.main_menu import MainMenu
from utils.settings_access import SettingsAccess

from utils.display_output import DisplayOutput
from utils.display_capture import DisplayCapture
from utils.audio_capture import AudioCapture
from utils.tv_detection import TVDetection

from utils.fps import FPS

from projection_modes.modes_factory import ModesFactory


img_path = (__file__[:__file__.index("app") 
            + len("app")]+"/assets/room_image/TV_box.jpeg")
BACKGROUND_IMG = cv2.imread(img_path)

print("image = ", BACKGROUND_IMG)


def main():

    menu = MainMenu()

    #Get the current general settings
    settings_access = SettingsAccess()
    general_settings_json = settings_access.read_settings("general_settings.json")

    # Display settings menu

    mode, displays = menu.main_select_options()
    if mode is not None: 
        selected_mode = mode
    else:
        #Display currently selected modes, if there are none then get user to select
        selected_mode = general_settings_json["selected_mode"]

    if displays is not None:
        selected_displays = displays
    else:
        selected_displays = general_settings_json["selected_displays"]

    print(f"Your selected mode: {selected_mode}")

    print(f"Your selected displays: {selected_displays}")

    # Create instance of projection modes factory

    # Create instance of display output, display capture
    primary_bounding_box = selected_displays["primary_display"]
    projector_bounding_box = selected_displays["projector_display"]

    display_capture = DisplayCapture(primary_bounding_box, projector_bounding_box)
    audio_capture = AudioCapture()
    # display_output = DisplayOutput()
    # # tv_detection = TVDetection()

    #Create instance of FPS
    fps = FPS()

    #Create the mode objects from the mode factory
    mode_factory = ModesFactory(BACKGROUND_IMG, display_capture, audio_capture, settings_access)
    mode_object = mode_factory.get_mode(selected_mode)


    # Create PyQt app
    app = QtWidgets.QApplication(sys.argv)
    main_window = DisplayOutput()
    main_window.showFullScreen()
    # main_window.show()

    # Main loop for app
    while not main_window.stopped:
        frames = mode_object.trigger()

        if frames is not None or len(frames) != 0:
            for frame in frames:
                height, width = frame.shape[:2]
                bytes_per_line = frame.strides[0]
                format_string = settings_access.read_mode_settings(selected_mode, "qImg_format")
                qImg_format = eval(format_string)
                qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, qImg_format).rgbSwapped()
                main_window.label.setPixmap(QtGui.QPixmap(qImg))
                # main_window.setFixedSize(width, height)
                app.processEvents()
                time.sleep(0.1)
    sys.exit(app.exec())


    # #Main loop of application
    # display_output = DisplayOutput()
    # stopped = False
    # while not(stopped):
    #     #fps.print_fps()
    #     #Modes control whether they need screen or audio capture
    #     frames = mode_object.trigger()
    #     #potentially add the depth mapping here
    #     stopped = display_output.display_frame(frames)
    # # # run display output unless exit command received eg: 'q' pressed when on 
    # # # projector window

    # # print("Thank you for using UCL Open Illumiroom V2, Have a great day!")
    # # Clean up and exit.
    
    # exit()

if __name__ == '__main__':
    main()
    
