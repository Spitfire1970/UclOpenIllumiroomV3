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
from utils.display_selection import DisplaySelection

from utils.display_output import DisplayOutput
from utils.display_capture import DisplayCapture
from utils.audio_capture import AudioCapture
from utils.room_image import RoomImage
from utils.calibration.calibration import Calibration

from utils.fps import FPS

from projection_modes.modes_factory import ModesFactory

app_root_path = __file__[:__file__.index("UCL_Open-Illumiroom_V2.py")]


def main():
    print("main")
    #Get the current general settings and display the menu
    settings_access = SettingsAccess(app_root_path)
    room_image_obj = RoomImage(settings_access)
    general_settings_json = settings_access.read_settings("general_settings.json")
    primary_bounding_box = general_settings_json["selected_displays"]["primary_display"]
    projector_bounding_box = general_settings_json["selected_displays"]["projector_display"]
    display_capture = DisplayCapture(primary_bounding_box, projector_bounding_box)
    calibration = Calibration(settings_access, display_capture)

    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))

    if len(sys.argv) == 1 or sys.argv[1] == "run":
        main_loop(settings_access)

    elif sys.argv[1] == "display":
        run_display_capture(settings_access)

    elif sys.argv[1] == "background_capture":
        run_background_capture(room_image_obj)

    elif sys.argv[1] == "select_tv":
        run_select_tv(room_image_obj)
    
    elif sys.argv[1] == "calibration":
        run_calibration(calibration)

    else:
        raise ValueError("Error: Incorrect Arguments")

def run_display_capture(settings_access):


    # Display settings menu
    display_selection = DisplaySelection(settings_access)
    display_selection.select_tv_projector()

def run_background_capture(room_image_obj):
    print("Step 1: Use Microsoft Lens to take a picture of the projected area. Press ESC to exit"
                  + "the projection. \nStep 2: Select the 4 corners of the projected grey image on Lens "
                  + "as accurately as you can. \nStep 3: Save the image to 'app\\assets\\room_image'."
                  + "with the name 'room_img.jpg'. \nIn our next build, we'll introduce "
                  + "an upload feature!")
    room_image_obj.take_picture()


def run_select_tv(room_image_obj):
    # print("Step 1: Upload the picture of the projected area.")
    # self.room_image_obj.save_picture()
    print("Detect where the TV/ primary monitor is on the image "
        + "by dragging your cursor to create a rectangle around it. "
        + "Press 'q' when the green rectangle covers the whole TV.")
    room_image_obj.detect_primary_display()


def run_calibration(calibration):
    # print("Step 1: Upload the picture of the projected area.")
    # self.room_image_obj.save_picture()
    print("start")
    frames=calibration.capture()
    print(frames)



def main_loop(settings_access):

        # Create PyQt app, only ever needs to be defined once
        app = QtWidgets.QApplication(sys.argv)
        #menu = MainMenu(settings_access)
        general_settings_json = settings_access.read_settings("general_settings.json")

        # Display settings menu

        #mode, displays, exit_requested = menu.main_select_options()
        mode = None
        displays = None


        if mode is not None: 
            selected_mode = mode
        else:
            #Display currently selected modes, if there are none then get user to select
            selected_mode = general_settings_json["selected_mode"]

        if displays is not None:
            selected_displays = displays
        else:
            selected_displays = general_settings_json["selected_displays"]

        #print(f"Your selected mode: {selected_mode}")

        #print(f"Your selected displays: {selected_displays}")

        # Create instance of projection modes factory

        # Create instance of display output, display capture
        primary_bounding_box = selected_displays["primary_display"]
        projector_bounding_box = selected_displays["projector_display"]

        display_capture = DisplayCapture(primary_bounding_box, projector_bounding_box)
        audio_capture = AudioCapture(settings_access)
        room_image_obj = RoomImage(settings_access,display_capture)
        room_image = room_image_obj.read_room_image(resize=False)

        #Create instance of FPS
        fps = FPS()
        show_fps = settings_access.read_general_settings("show_fps")

        #Create the mode objects from the mode factory
        mode_factory = ModesFactory(room_image, display_capture, audio_capture, settings_access)
        mode_object = mode_factory.get_mode(selected_mode)

        format_string = settings_access.read_mode_settings(selected_mode, "qImg_format")
        trigger_frequency = settings_access.read_mode_settings(selected_mode, "trigger_frequency")
        qImg_format = eval(format_string)



        main_window = DisplayOutput(primary_bounding_box, projector_bounding_box)

        frame_counter = 0
        # Main loop for app
        while not main_window.stopped:
    
            frames = mode_object.trigger()

            if frames is not None or len(frames) != 0:
        
                for frame in frames:
                    #Resize frame to fit projector if requires resizing
                    #frame = display_capture.frame_projector_resize(frame)
                    if show_fps:
                        fps.add_fps_to_image(frame, fps.get_fps())
                    #Frame display
                    
     
                    print(frame.shape)
              
                    height, width = frame.shape[:2]
                    bytes_per_line = frame.strides[0]

                    print("height",bytes_per_line)
                    qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, qImg_format).rgbSwapped()
                    main_window.label.setPixmap(QtGui.QPixmap(qImg))
                    app.processEvents()
                    #fps.print_fps()
                    #time.sleep(5)
            frame_counter+=1
        


if __name__ == '__main__':
    main()
    
    
