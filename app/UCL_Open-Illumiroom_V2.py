# 1) User runs main
# 2) Menu is opened for the user, can update settings eg: their primary and 
# projector displays and other settings
import sys
import numpy as np
from PyQt6 import QtWidgets, QtGui

from utils.settings_access import SettingsAccess
from utils.display_selection import DisplaySelection

from utils.display_output import DisplayOutput
from utils.display_capture import DisplayCapture
from utils.audio_capture import AudioCapture
from utils.room_image import RoomImage
from utils.calibration.calibration import Calibration

from utils.fps import FPS

from projection_modes.modes_factory import ModesFactory

#Get the app root path of the project in user's file system
#Allows assets to be loaded in
app_root_path = __file__[:__file__.index("UCL_Open-Illumiroom_V2.py")]

def main():

    #Instantiate required objects to be passed to main loop or display setup/calibration 
    settings_access = SettingsAccess(app_root_path)

    room_image_obj = RoomImage(settings_access)
    room_image = room_image_obj.read_room_image(resize=False)

    display_capture = DisplayCapture(settings_access)
    
    fps = FPS()

    #If no arguments passed, or argument is run, run the main loop
    if len(sys.argv) == 1 or sys.argv[1] == "run":
        audio_capture = AudioCapture(settings_access)
        mode_factory = ModesFactory(room_image, display_capture, audio_capture, settings_access)
        main_loop(settings_access,  mode_factory, fps)

    elif sys.argv[1] == "display":
        run_display_capture(settings_access)

    elif sys.argv[1] == "background_capture":
        run_background_capture(room_image_obj)

    elif sys.argv[1] == "select_tv":
        run_select_tv(room_image_obj)
    
    elif sys.argv[1] == "calibration":
        calibration = Calibration(settings_access, display_capture)
        run_calibration(calibration)

    else:
        raise ValueError("Error: Incorrect Arguments")

def run_display_capture(settings_access):


    # Display the settings menu
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
    #Run the calibration system, calibrating the projector to the TV.
    calibration.capture()




def main_loop(settings_access, mode_factory, fps):
        
        display_output = DisplayOutput(settings_access)

        mode_object = mode_factory.get_mode()
        show_fps = settings_access.read_general_settings("show_fps")


        # Main loop for app, while user has not pressed ESC
        while not display_output.stopped:
            
            #Trigger the mode object to get the frames to display
            frames = mode_object.trigger()

            #Display frames if some are returned
            if frames is not None or len(frames) != 0:
        
                for frame in frames:
                    #Add the FPS counter to images if required
                    if show_fps:
                        fps.add_fps_to_image(frame, fps.get_fps())

                    #Display the frame on the projector
                    display_output.display_frame(frame)
                   
        


if __name__ == '__main__':
    main()
    
    
