import tkinter as tk
from tkinter import ttk, filedialog as tfd, messagebox as tmb, simpledialog as tsd
import os

from settings import SettingsHandler
from utills import *


class SettingsTab(ttk.Frame, SettingsHandler):
    def __init__(self, master, root, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        SettingsHandler.__init__(self)
        
        self.root_window = root

        # ttk.Label(master=self, text="test").pack(pady=20)

        center_frame = ttk.Frame(master=self)
        center_frame.pack(pady=5, padx=5)

        row = 0
        # Name the Resource pack
        rp_name_label = ttk.Label(master=center_frame,text="Resource pack Name: ")
        rp_name_label.grid(row=row, column=0, sticky="e")
        
        self.rp_folder_name_label = ttk.Label(master=center_frame, text=self.RP_folder_name)
        self.rp_folder_name_label.grid(row=row, column=1,)

        rp_name_button = ttk.Button(master=center_frame, text="Change Name", command=self.set_rp_folder_name)
        rp_name_button.grid(row=row, column=2)

        row += 1

        # Minecraft folder path
        minecraft_folder_label = ttk.Label(master=center_frame,text="Minecraft Path: ")
        minecraft_folder_label.grid(row=row, column=0, sticky="e")
        
        self.minecraft_folder_path_label = ttk.Label(master=center_frame, text=self.minecraft_folder_path)
        self.minecraft_folder_path_label.grid(row=row, column=1,)

        Minecraft_path_button = ttk.Button(master=center_frame, text="Change Path", command=self.set_path_minecraft)
        Minecraft_path_button.grid(row=row, column=2)

        row += 1
        # Furigana Resource pack path
        furigana_rp_label = ttk.Label(master=center_frame,text="Furigana Resource Pack Path: ")
        furigana_rp_label.grid(row=row, column=0, sticky="e")
        
        self.furigana_rp_path_label = ttk.Label(master=center_frame, text=self.furigana_rp_path)
        self.furigana_rp_path_label.grid(row=row, column=1,)

        furigana_rp_button = ttk.Button(master=center_frame, text="Change Path", command=self.set_path_RP_zip)
        furigana_rp_button.grid(row=row, column=2)

        row += 1

        # Resource pack output path
        RP_output_label = ttk.Label(master=center_frame,text="Furigana Resource Pack Path: ")
        RP_output_label.grid(row=row, column=0, sticky="e")
        
        self.RP_output_path_label = ttk.Label(master=center_frame, text=self.RP_output_path)
        self.RP_output_path_label.grid(row=row, column=1,)

        RP_output_button = ttk.Button(master=center_frame, text="Change Path", command=self.set_path_RP_output)
        RP_output_button.grid(row=row, column=2)

        row += 1


        # Save settings
        save_settings_button = ttk.Button(master=self, text="Save Settings", command=self.save_settings)
        save_settings_button.pack()

        if self.settings_opened is False:
            print(f"settings file: {self.settings_opened}")
            self.after(0, self.first_time_setup)
            # self.first_time_setup()

    def first_time_setup(self):
        answer = tmb.askokcancel("First time setup", 
"""The settings file was not found

Runing first time settup

If this is your first time running this.
The language file does not come with the game and must be downloaded by the game.
Please make sure you have run the Latest UN-MODDED version of Minecraft and have used the japanese language option once.""")
        if not answer:
            self.root_window.destroy()
            return
        # self.set_rp_folder_name()
        self.set_path_minecraft()
        self.set_path_RP_zip()
        self.set_path_RP_output()

        self.save_settings()
        self.settings_opened = True

    def set_path_minecraft(self):
        # ask how the path should be found
        answer = tmb.askyesnocancel("Set Minecraft Path", 
"""The Minecraft folder must be set in order to grab the Japanese translation.

The language file does not come with the game and must be downloaded by the game.
Please make sure you have run the Latest UN-MODDED version of Minecraft and have used the japanese language option once.

Would you like me to try to use the default minecraft path?
Press 'No' to set the path yourself.""")
        if answer is None:
            # if canceled, return
            return
        elif answer is True:
            # If yes, find the pathe in appdata
            path = os.path.join(os.getenv('APPDATA'), ".minecraft")
        else:
            # If no, have the user slect the path
            path = tfd.askdirectory()
            # TODO ad a check to see if the path the user gives is valid
        
        if not os.path.exists(path=path):
            # check if the path exist and show an error if it does not.
            tmb.showerror("Error", "The minecraft path can't be found.")
            # let the user slect a diffrent way
            self.set_path_minecraft()
        else:
            self.minecraft_folder_path = path
            self.minecraft_folder_path_label.config(text=self.minecraft_folder_path)

    def set_path_RP_output(self):
        # ask how the path should be found
        answer = tmb.askyesnocancel("Set the ouput location", "Would you like to export to the Minecraft Resource Pack folder?\nThis setting is where the mixed resource pack gets saved\n\nSelect 'No' to set a diffrent path")
        if answer is None:
            # if canceled, return
            return
        elif answer is True:
            # If yes, find the pathe in appdata
            path = os.path.join(os.getenv('APPDATA'), ".minecraft/resourcepacks")
        else:
            # If no, have the user slect the path
            path = tfd.askdirectory()
        
        if not os.path.exists(path=path):
            # check if the path exist and show an error if it does not.
            tmb.showerror("Error", "The path can't be found.")
            # let the user slect a diffrent way
            self.set_path_RP_output()
        else:
            self.RP_output_path = path
            self.RP_output_path_label.config(text=self.RP_output_path)

    def set_path_RP_zip(self):
        # ask for the zip file
        path = tfd.askopenfilename(
            initialdir=os.path.join(self.minecraft_folder_path, "resourcepacks"),
            title="Please slect a Resource Pack ZIP file.",
            filetypes=(("ZIP files", "*.zip"), ("All files", "*.*"))
            )
        
        if not os.path.exists(path=path):
            tmb.showerror("Error", "No path was slected.")
        else:
            self.furigana_rp_path = path
            self.furigana_rp_path_label.config(text=self.furigana_rp_path)

    def set_rp_folder_name(self):
        name = tsd.askstring(
            "Input", 
            "What do you want the resource pack to be called in minecraft?",
            parent=self.root_window,
            initialvalue=self.RP_folder_name
            )
        print(name)
        print(type(name))
        if type(name) is None:
            return
        elif len(name) == 0:
            return
        elif str.isspace(name):
            return
        else:
            self.RP_folder_name = name
            self.rp_folder_name_label.config(text=self.RP_folder_name)
            

class ScramblerTab(ttk.Frame):
    def __init__(self, master, root, settings:SettingsHandler, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.root_window = root
        self.settings = settings

        frame = ttk.Frame(master=self)
        frame.pack()

        number_percentage_label = ttk.Label(master=frame, text="Percentage of No furigana:")
        number_percentage_label.pack(side="left")

        # Register the validation command
        # TODO How do I only alow numbers to be entered in the box?
        self.percentage_entry = ttk.Entry(master=frame)
        self.percentage_entry.pack(side="left")

        run_the_program_button = ttk.Button(master=self, text="RUN", command=self.run_it)
        run_the_program_button.pack()

        run_the_program_button = ttk.Button(master=self, text="Load", command=self.load_packs)
        run_the_program_button.pack()


    def get_packs(self):
        pass
    
    def get_default_translation(self):
        index_results = get_lang_from_minecraft_indexes(minecraft_dir=self.settings.minecraft_folder_path)
        if not index_results:
            tmb.showerror(title="Translation Not found",
                          message='''Can not find the Japanese Translation
The language file does not come with the game and must be downloaded by the game.
Please make sure you have ran the Latest UN-MODDED version of Minecraft and have used the japanese language option once.''')
            return
        kanji_lang_dict, latest_translation = index_results
        if not latest_translation:
            tmb.showwarning(title="Latest Translation not found",
message='''Can not find the latest translation file.
An older one has been found, some ingame items may be in english.

The language file does not come with the game and must be downloaded by the game.
Please make sure you have ran the Latest UN-MODDED version of Minecraft and have used the japanese language option once.''')
        return kanji_lang_dict

    def get_percentage(self):
        entry = self.percentage_entry.get()
        try:
            percentage = float(entry)
        except ValueError:
            tmb.showerror(title="Not a Valid Number",
                          message=f'''You Entered: "{entry}"
that is not a valid number.

Please enter a valid number''')
            return
        else: 
            if percentage > 100:
                percentage = 100
            elif percentage < 0:
                percentage = 0    
            
            print(f"percentage = {percentage}")
            return percentage

    def get_furigana(self):
        lang_file_list = get_lang_file_list(furigana_rp_zip=self.settings.furigana_rp_path)
        if len(lang_file_list) > 1:
            print(len(lang_file_list))
            # TODO let the user decide wich one they want to use
            tmb.showwarning(title="Multiple Language files found",
                            message=f'''Multiple Language files were found in the Resource Pack
{lang_file_list}
loading the first one: {lang_file_list[0]}
                            '''
                            )    


        furigana_lang_dict = get_furigana_lang(furigana_rp_zip=self.settings.furigana_rp_path, target_file=lang_file_list[0])
        if not furigana_lang_dict:
            tmb.showerror(title="Translation Not found",
                          message="Can't open the furigana language file")
            return
        return furigana_lang_dict

    def run_it(self):
        # get the inputed percent
        percent = self.get_percentage()
        if not isinstance(percent, (int, float)):
            return
        
        # get the default Translation
        kanji_lang_dict = self.get_default_translation()
        if type(kanji_lang_dict) is not dict:
            return
        
        # get furigana translation
        furigana_lang_dict = self.get_furigana()
        if type(furigana_lang_dict) is not dict:
            return 
        

        # Mix the data
        mixed_lang_dict = mix_dicts(
            kanji=kanji_lang_dict, 
            furigana= furigana_lang_dict, 
            precentage_from_kanji=percent)

        make_resource_pack(
            lang_data=mixed_lang_dict,
            minecraft_RP_path=self.settings.RP_output_path,
            pack_name=self.settings.RP_folder_name
            )
        tmb.showinfo("Completed", message="The resource pack has been made.\n\nIf Minecraft is running, You can press F3 + T to reload the pack.")

    def load_packs(self):
        pass

class MainWindow(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        # Some setup for the window name and size
        self.title("Furigana Scrambler")
        self.geometry("800x600")
        self.minsize(300, 200)

        # setup the tabs
        tabs = ttk.Notebook(self)
        tabs.pack(expand=True, fill='both')

        tab_settings = SettingsTab(master=tabs, root=self)
        
        tab_scrambler = ScramblerTab(master=tabs, root=self, settings=tab_settings)
        tabs.add(tab_scrambler, text="Scrambler")

        tabs.add(tab_settings, text="Settings")

        pass

if __name__ == "__main__":
    MainWindow().mainloop()
  
    
    