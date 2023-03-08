#The Main menu class has been deprecated, replaced with the MFC application

from projection_modes.modes_factory import ModesFactory
from .display_selection import DisplaySelection
from .room_image import RoomImage

from time import sleep


class MainMenu:
   def __init__(self, settings_access):
      mode_factory = ModesFactory(None, None, None, None)
      self.settings_access = settings_access
      self.available_modes = mode_factory.get_available_modes()
      self.modes = None
      self.displays = None
      self.room_image_obj = RoomImage(self.settings_access)


   def main_select_options(self):
      ready_to_run = False
      print("----------------------------------")
      print("Welcome to UCL Open-Illumiroom V2")
      
      while(not(ready_to_run)):
         print("\nPlease enter the number of the option you wish to select:")
         print("1) Run Illumiroom")
         print("2) Select your projector and TV displays")
         print("3) Take a picture of the projected area")
         print("4) Detect your TV in the picture")
         print("5) Choose your required mode")
         print("6) View mode Settings")
         print("7) Exit the system")

         user_selection = input(">")
         if user_selection == "1" or user_selection == "run":
            return self.modes, self.displays, False

         elif user_selection == "2":
            display_selector = DisplaySelection(self.settings_access)
            self.displays = display_selector.select_tv_projector()

         elif user_selection == "3":
            print("Step 1: Use Microsoft Lens to take a picture of the projected area. Press ESC to exit"
                  + "the projection. \nStep 2: Select the 4 corners of the projected grey image on Lens "
                  + "as accurately as you can. \nStep 3: Save the image to 'app\\assets\\room_image'."
                  + "with the name 'room_img.jpg'. \nIn our next build, we'll introduce "
                  + "an upload feature!")
            self.room_image_obj.take_picture()

         elif user_selection == "4":
            # print("Step 1: Upload the picture of the projected area.")
            # self.room_image_obj.save_picture()
            print("Detect where the TV/ primary monitor is on the image "
               + "by dragging your cursor to create a rectangle around it. "
               + "Press 'q' when the green rectangle covers the whole TV.")
            self.room_image_obj.detect_primary_display()

         elif user_selection == "5":
            self.modes = self.select_modes()

         elif user_selection == "6":
            self.select_mode_settings()
         #    #print("Changing mode settings requires the Ilumiroom System to restart, please rerun Illumiroom")
         #    #exit()
         elif user_selection == "7":
            print("Thank you for using UCL-Open Illumiroom V2")
            print("Have a great day!")    
            return self.modes, self.displays, True

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

         modes_selected=input().strip()
         # print("Mode selected IS: ", modes_selected)
         if self.check_mode_valid(self.available_modes,modes_selected):
            mode_selection_in_progress = False #All modes valid, can continue
         else:
            print("Invalid mode entered, please try again!")

      self.get_settings_for_mode(modes_selected)

   def get_settings_for_mode(self,mode):
      mode_settings_json = self.settings_access.read_settings("mode_settings.json")
      #settings begining with a . cannot be changed by the user
      specific_mode_settings = mode_settings_json[mode]
      #for now only shows settings, must be changed in json file since not that important
      for key, setting in enumerate(specific_mode_settings):
         if setting[0]!=".":
            print(f"{key}) {setting}: {specific_mode_settings[setting]}")

      print("------")