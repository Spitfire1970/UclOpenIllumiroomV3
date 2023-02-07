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


    def read_mode_settings(self, mode, settings):
        mode_settings_json = self.read_settings("mode_settings.json")
        if isinstance(settings, str):
            return mode_settings_json[mode][settings]
        else:
            # Nested JSON object
            return mode_settings_json[mode][settings[0]][settings[1]]