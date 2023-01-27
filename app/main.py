# 1) User runs main
# 2) Menu is opened for the user, can update settings eg: their primary and 
# projector displays and other settings


import numpy as np
import cv2

from utils.main_menu import MainMenu
from utils.settings_access import SettingsAccess

from utils.display_output import DisplayOutput
from utils.display_capture import DisplayCapture
from utils.audio_capture import AudioCapture

from utils.fps import FPS

from projection_modes.modes_factory import ModesFactory

BACKGROUND_IMAGE = "assets/room_image/TV_box.jpeg"


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
    display_output = DisplayOutput()

    #Create instance of FPS
    fps = FPS()

    #Create the mode objects from the mode factory
    mode_factory = ModesFactory(display_capture,audio_capture)
    mode_object = mode_factory.get_mode(selected_mode)
    

    #Main loop of application
    stopped = False
    while not(stopped):

        #fps.print_fps()

        #Modes control whether they need screen or audio capture
        #Calling trigger on the mode object causes it to activate itself and run as required,
        #trigger always returns a frame or None
        frames = mode_object.trigger()
        
        #potentially add the depth mapping here

        stopped = display_output.display_frame(frames)

    # run display output unless exit command received eg: 'q' pressed when on 
    # projector window

    print("Thank you for using UCL Open Illumiroom V2, Have a great day!")
    # Clean up and exit.
    exit()

if __name__ == '__main__':
    main()
    
