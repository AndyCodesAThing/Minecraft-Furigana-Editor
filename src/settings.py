import os

from utills import write_json_fromat, read_json_format

SettingsFileLocation = "./settings.json"

class SettingsHandler():
    def __init__(self):

        self.settings_opened = False

        # settings that don't change
        self._source_pack_PNG = "./assets/pack.png"

        # settings that do change
        self.RP_folder_name = "Furigana Scrambler"
        self.minecraft_folder_path = None
        self.furigana_rp_path = None
        self.RP_output_path = None

        if os.path.exists(SettingsFileLocation):
            self.settings_opened = True
            self.get_settings()

    def get_settings(self):
        # open settings
        setting_dict = read_json_format(SettingsFileLocation)

        self.RP_folder_name = setting_dict["RP_folder_name"]
        self.minecraft_folder_path = setting_dict["minecraft_folder_path"]
        self.furigana_rp_path = setting_dict["furigana_rp_path"]
        self.RP_output_path = setting_dict["minecraft_RP_folder_path"]
        

        # set settings as opened
        self.settings_opened = True

    def save_settings(self):
        settings_dict = {
            "RP_folder_name": self.RP_folder_name,
            "minecraft_folder_path": self.minecraft_folder_path,
            "furigana_rp_path": self.furigana_rp_path,
            "minecraft_RP_folder_path": self.RP_output_path,
        }
        write_json_fromat(settings_dict, SettingsFileLocation)
