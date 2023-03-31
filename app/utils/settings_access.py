import json


class SettingsAccess:
    """
    SettingsAccess class allows for easy read and write access into
    the config saved in general_settings.json and mode_settings.json files
    """
    def __init__(self, app_root_path):

        self.app_root_path = app_root_path
        self.assets_path = app_root_path + "assets\\"
        self.settings_path = app_root_path + "settings\\"
        self.room_img_path = self.assets_path + "room_image\\"
        self.utils_path = app_root_path + "utils\\"
        self.ml_models_path = app_root_path + "assets\\ml_models\\"

    def read_settings(self, settings_name):
        """
        Read setting file name as json
        :param settings_name: Name of settings file to be read
        :return: Json object containing settings
        """
        path = self.settings_path + settings_name
        with open(path, 'r') as read_file:
            return json.load(read_file)

    def write_settings(self, settings_name, new_json_data):
        """
        Write settings to specified file
        :param settings_name: Name of the file to write settings to
        :param new_json_data: Data to write into that file
        """
        path = self.settings_path + settings_name
        with open(path, 'w') as write_file:
            json.dump(new_json_data, write_file)

    def read_general_settings(self, setting):
        """
        Read a setting from general settings
        :param setting: Setting name
        :return: Value for specified setting
        """
        general_settings_json = self.read_settings("general_settings.json")
        return general_settings_json[setting]

    def read_mode_settings(self, mode, settings):
        """
        Read a settings from specific mode
        :param mode: Mode to read from
        :param settings: Settings name(s)
        :return: Setting value under specified mode and setting name
        """
        mode_settings_json = self.read_settings("mode_settings.json")
        if isinstance(settings, str):
            return mode_settings_json[mode][settings]
        else:
            # Nested JSON object
            return mode_settings_json[mode][settings[0]][settings[1]]

    def read_mode_settings_object(self, mode, settings):
        """
        Read an object from mode settings
        :param mode: mode to read from
        :param settings: name of the object
        :return: Object under specified settings name
        """
        mode_settings_json = self.read_settings("mode_settings.json")
        return mode_settings_json[mode][settings]

    def get_image_path(self, image_path):
        """
        Get a path for saving the room image
        :param image_path: internal image path
        :return: full image path
        """
        img_path = self.room_img_path + image_path
        return img_path

    def get_assets_path(self):
        return self.assets_path

    def get_ml_model_path(self):
        return self.ml_models_path
