from projection_modes.modes_factory import ModesFactory
from .settings_access import SettingsAccess


class MainMenu:

   def print_available_modes(self):
      print("Select Your Mode:")
      print("1: Blur")
      print("2: Wobble")

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
            print(f"{index}) {mode}")

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