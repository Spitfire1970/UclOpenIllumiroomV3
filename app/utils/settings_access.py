import json


class SettingsAccess:
    def __init__(self, app_root_path):
        
        
        self.app_root_path = app_root_path
        self.assets_path = app_root_path+"assets\\"
        self.settings_path = app_root_path+"settings\\"
        self.room_img_path = self.assets_path+"room_image\\"
        self.utils_path = app_root_path+"utils\\"
        self.ml_models_path = app_root_path + "assets\\ml_models\\"


    def read_settings(self, settings_name):

        path = self.settings_path + settings_name
        with open(path,'r') as read_file:
            return json.load(read_file)


    def write_settings(self, settings_name, new_json_data):
    
        path = self.settings_path + settings_name
        with open(path,'w') as write_file:
            json.dump(new_json_data, write_file)


    def read_general_settings(self, setting):
        general_settings_json = self.read_settings("general_settings.json")
        return general_settings_json[setting]


    def read_mode_settings(self, mode, settings):
        mode_settings_json = self.read_settings("mode_settings.json")
        if isinstance(settings, str):
            return mode_settings_json[mode][settings]
        else:
             # Nested JSON object
            return mode_settings_json[mode][settings[0]][settings[1]]
        
    def read_mode_settings_object(self, mode, settings):
        mode_settings_json = self.read_settings("mode_settings.json")
        return mode_settings_json[mode][settings]


    def get_image_path(self, image_path):
        img_path = self.room_img_path + image_path
        return img_path


    def get_assets_path(self):
        return self.assets_path

    def get_ml_model_path(self):
        return self.ml_models_path