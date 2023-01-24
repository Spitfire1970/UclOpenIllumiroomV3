# 1) User runs main
# 2) Menu is opened for the user, can update settings eg: their primary and 
# projector displays and other settings


import numpy as np
import cv2

from utils.main_menu import MainMenu
from utils.settings_access import SettingsAccess

BACKGROUND_IMAGE = "assets/room_image/TV_box.jpeg"

if __name__ == '__main__':

    menu = MainMenu()

    #Get the current general settings
    settings_access = SettingsAccess()
    general_settings_json = settings_access.read_settings("general_settings.json")
    #Display currently selected modes, if there are none then get user to select

    selected_modes = general_settings_json["selected_modes"]
    if selected_modes is None or selected_modes == []:
        selected_modes = menu.select_modes()

    print(f"Your selected mode(s): {selected_modes}")
    # Display settings menu
    

    # Create instance of projection modes factory

    # Create instance of display output

    # run display output unless exit command received eg: 'q' pressed when on 
    # projector window

    # Clean up and exit.
    pass
