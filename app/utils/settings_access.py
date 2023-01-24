import json


class SettingsAccess:
    def __init__(self):
        #Get the path to the settings app up to the app folder
        self.path = __file__[:__file__.index("app") + len("app")]+"/settings/"


    def read_settings(self, settings_name):

        settings_path = self.path + settings_name
        with open(settings_path,'r') as read_file:
            return json.load(read_file)


    def write_settings(self, settings_name, new_json_data):
    
        settings_path = self.path + settings_name
        with open(settings_path,'w') as write_file:
            json.dump(new_json_data, write_file)