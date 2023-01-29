from projection_modes.modes_factory import ModesFactory
from .display_selection import DisplaySelection
from .settings_access import SettingsAccess

from time import sleep

class MainMenu:
   def __init__(self):
      mode_factory = ModesFactory(None, None, None, None)
      self.settings_access = SettingsAccess()
      self.available_modes = mode_factory.get_available_modes()
      self.modes = None
      self.displays = None


   def main_select_options(self):
      ready_to_run = False
      print("Welcome to UCL Open-Illumiroom V2")
      
      while(not(ready_to_run)):
         print("Please enter the number of the option you wish to select")
         print("1) Run Illumiroom")
         print("2) Select your projector and TV displays")
         print("3) Chose your required mode(s)")
         print("4) View Mode Settings")
         
         user_selection = input(">")
         if user_selection == "1" or user_selection == "run":
            return self.modes, self.displays

         elif user_selection == "2":
            display_selector = DisplaySelection()
            self.displays = display_selector.select_tv_projector()

         elif user_selection == "3":
            self.modes = self.select_modes()

         elif user_selection == "4":
            self.select_mode_settings()
            #print("Changing mode settings requires the Ilumiroom System to restart, please rerun Illumiroom")
            #exit()

         else:
            print("Invalid input, please try again!")

         #Include a sleep to give feeling of menu movement
         sleep(0.5)

   
   def check_mode_valid(self,available_modes, mode):
      return mode in available_modes
   

   def select_modes(self):
      print("The modes currently available are:")
   
      #Create a mode factory and get the available modes, ModesFactory is definitive list
      # No display or audio capture are passed in - None

      mode_selection_in_progress = True #Becomes false when valid modes have been entered

      while(mode_selection_in_progress):
         for index, mode in enumerate(self.available_modes):
            print(f"{mode}")

         print("Please select a mode that you wish to use")
         print("Please only enter one mode name, any more will not be accepted")
         print("eg: wobble")

         mode_selection = input()
         mode = mode_selection.strip()

         print("Mode selected: ")
         print(f"{mode}")

         if self.check_mode_valid(self.available_modes,mode):
            mode_selection_in_progress = False #All modes valid, can continue
         else:
            print("Invalid mode entered, please try again!")


      #Write the selected mode to the general settings json
      general_settings_json = self.settings_access.read_settings("general_settings.json")
      general_settings_json['selected_mode'] = mode
      self.settings_access.write_settings("general_settings.json", general_settings_json)

      return mode

   def select_mode_settings(self):
      mode_selection_in_progress = True #Becomes false when valid modes have been entered
      
      while(mode_selection_in_progress):
         for index, mode in enumerate(self.available_modes):
            print(f"{mode}")
         print("------")
         print("Please select the mode whose settings you would like to view")
         print("Either enter the mode name eg: wobble. Only enter 1 mode")

         modes_selected=[input().strip()]
         if self.check_mode_valid(self.available_modes,modes_selected):
            mode_selection_in_progress = False #All modes valid, can continue
         else:
            print("Invalid mode entered, please try again!")

      self.get_settings_for_mode(modes_selected[0])

   def get_settings_for_mode(self,mode):
      mode_settings_json = self.settings_access.read_settings("mode_settings.json")
      #settings begining with a . cannot be changed by the user
      specific_mode_settings = mode_settings_json[mode]
      #for now only shows settings, must be changed in json file since not that important
      for key, setting in enumerate(specific_mode_settings):
         if setting[0]!=".":
            print(f"{key}) {setting}: {specific_mode_settings[setting]}")

      print("------")