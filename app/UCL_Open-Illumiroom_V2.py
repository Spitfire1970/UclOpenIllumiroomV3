"""
UCL_Open-Illumiroom_V2.py

This file contains the main function and supporting functions to run the UCL Open-Illumiroom V2 System.
When compiled, the program will be compiled as UCL_Open-Illumiroom_V2.exe and this file will act as the primary entry point of the program.

This script may be run during development to run the main loop of the app, the display capture system, or to run the calibration system.
To run the:
- main loop of the app, run the following command: python UCL_Open-Illumiroom_V2.py run
- display selection, run the following command: python UCL_Open-Illumiroom_V2.py display
- the calibration, run the following command: python UCL_Open-Illumiroom_V2.py calibration

The following global variables are defined:
- app_root_path: str - the root path of the project in user's file system

The following functions are defined:
- main(): void - the main function that runs the UCL Open-Illumiroom V2 system
- run_display_selection(settings_access): void - displays the menu that allows the user to select their primary display/TV and their projector
- run_calibration(calibration): void - runs the calibration system to calibrate the projector for the user's background area
- main_loop(settings_access, mode_factory, fps): void - the main loop of the app that displays the frames from the projection modes on the projector

"""

import sys

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
    """
    Entry point of the program.
    """

    #Instantiate required objects to be passed to main loop or display setup/calibration 
    settings_access = SettingsAccess(app_root_path)

    room_image_obj = RoomImage(settings_access)
    room_image = room_image_obj.read_room_image(resize=False)

    display_capture = DisplayCapture(settings_access)
    
    fps = FPS()

    #If no arguments passed, or argument is run, run the main loop
    if len(sys.argv) == 1 or sys.argv[1] == "run":
        print("run main loop")
        audio_capture = AudioCapture(settings_access)
        mode_factory = ModesFactory(room_image, display_capture, audio_capture, settings_access)
        main_loop(settings_access,  mode_factory, fps)

    #Argument is display - run display selection
    elif sys.argv[1] == "display":
        run_display_selection(settings_access)

    #Argument is calibration - run calibration
    elif sys.argv[1] == "calibration":
        calibration = Calibration(settings_access, display_capture)
        run_calibration(calibration)

    else:
        raise ValueError("Error: Incorrect Arguments")

def run_display_selection(settings_access):
    """
    Displays the settings menu for selecting between your primary display/TV and projector.
    Opens a TKinter window.
    """

    display_selection = DisplaySelection(settings_access)
    display_selection.select_tv_projector()


def run_calibration(calibration):
    """
    Runs the calibration system to calibrate the projector to the TV.
    """
    calibration.setup_system()


def main_loop(settings_access, mode_factory, fps):
        """
        The main loop of the program. While the user has not pressed ESC, get frames from the 
        mode object and display them on the projector.
        """
        
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
    
    
