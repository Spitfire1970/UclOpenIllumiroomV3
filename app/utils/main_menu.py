from projection_modes.modes_factory import ModesFactory
from .display_selection import DisplaySelection
from .settings_access import SettingsAccess

from time import sleep

class MainMenu:
   def __init__(self):
      self.modes = None
      self.displays = None

   def main_select_options(self):
      ready_to_run = False
      print("Welcome to UCL Open-Illumiroom V2")
      
      while(not(ready_to_run)):
         print("Please enter the number of the option you wish to select")
         print("1) Select your projector and TV displays")
         print("2) Chose your required mode(s)")
         print("3) Run Illumiroom")
         user_selection = input(">")
         if user_selection == "3" or user_selection == "run":
            return self.modes, self.displays
         elif user_selection == "1":
            display_selector = DisplaySelection()
            self.displays = display_selector.select_tv_projector()
         elif user_selection == "2":
            self.modes = self.select_modes()
         else:
            print("Invalid input, please try again!")

         #Include a sleep to give feeling of menu movement
         sleep(0.75)

   
   def check_modes_valid(self,available_modes, modes):
      for mode in modes:
         if mode not in available_modes:
            return False
      return True
   

   def select_modes(self):
      print("The modes currently available are:")
   
      #Create a mode factory and get the available modes, ModesFactory is definitive list
      mode_factory = ModesFactory(None, None)
      available_modes = mode_factory.get_available_modes()
      mode_selection_in_progress = True #Becomes false when valid modes have been entered

      while(mode_selection_in_progress):
         for index, mode in enumerate(available_modes):
            print(f"{mode}")

         print("Please select a mode, or 2 modes that are compatible")
         print("Either enter the mode name eg: wobble, or for 2 modes seprate with a comma: blur,weather_snow")
         print("Any more than 2 modes are not supported and will be ignored!")

         modes_selection = input()
         modes = modes_selection.strip().replace(" ","").split(',')[:2]

         print("Mode(s) selected: ")
         for mode in modes:
            print(f"{mode}")

         if self.check_modes_valid(available_modes,modes):
            mode_selection_in_progress = False #All modes valid, can continue
         else:
            print("Invalid mode entered, please try again!")


      #Write the selected modes to the general settings json
      settings_access = SettingsAccess()
      general_settings_json = settings_access.read_settings("general_settings.json")
      general_settings_json['selected_modes'] = modes
      settings_access.write_settings("general_settings.json", general_settings_json)

      return modes