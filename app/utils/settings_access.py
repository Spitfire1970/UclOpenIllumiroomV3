import json


class SettingsAccess:
    def __init__(self, app_root_path):
        #Get the path to the settings app up to the app folder
        #self.path = __file__[:__file__.index("app") + len("app")]+"/settings/"
        self.app_root_path = app_root_path
        self.assets_path = app_root_path+"assets\\"
        self.settings_path = app_root_path+"settings\\"


    def read_settings(self, settings_name):

        path = self.settings_path + settings_name
        with open(path,'r') as read_file:
            return json.load(read_file)

    def read_general_settings(self, setting):

        path = self.settings_path +"general_settings.json"
        with open(path,'r') as read_file:
            return json.load(read_file)[setting]


    def write_settings(self, settings_name, new_json_data):
    
        path = self.settings_path + settings_name
        with open(path,'w') as write_file:
            json.dump(new_json_data, write_file)


    def read_mode_settings(self, mode, settings):
        mode_settings_json = self.read_settings("mode_settings.json")
        if isinstance(settings, str):
            return mode_settings_json[mode][settings]
        else:
            # Nested JSON object
            return mode_settings_json[mode][settings[0]][settings[1]]

    def get_image_path(self, image_path):
        img_path = self.assets_path+image_path
        return img_path