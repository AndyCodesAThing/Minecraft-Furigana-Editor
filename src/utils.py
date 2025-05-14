import json
import os
import sys
import zipfile
import random
import shutil

SourcePackPNG = "assets/pack.png"

RP_lang_folder = "assets/minecraft/lang/"

MixedLangFileName = "ja_jp_mixed_rubi"

# TODO This should get genterted with accurate values.
#   The format should take after the furigana RP format
PackMCMetaFileData = {
    "pack": {
        "description": "This is the result of the Furigana Scrambler, Furigana is randomly removed. Use the Rubi mod to display Furigana above the Kanji.",
        "pack_format": 34,
        "supported_formats": { "min_inclusive": 33, "max_inclusive": 38 }
    },
    "language": {
        MixedLangFileName: {
            "name": "日本語 Furigana Scrambler",
            "region": "§^日本(にほん)",
            "bidirectional": False
        }
    }
}


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# #### Make files ####
def write_json_format(data, file_path, encoding=None, ensure_ascii=True):
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data, file, indent=4, ensure_ascii=ensure_ascii)

def write_json_fromat_japanese(data, file_path):
    '''This ensures the Japanese text gets encoded properly'''
    write_json_format(data=data, file_path=file_path, encoding="utf-8", ensure_ascii=False)

def make_resource_pack(lang_data, minecraft_RP_path, pack_name):
    # get the paths
    RP_path = os.path.join(minecraft_RP_path, pack_name)
    lang_path = os.path.join(RP_path, RP_lang_folder)
    # get File paths
    pack_mc_meta_file = os.path.join(RP_path, "pack.mcmeta")
    pack_png_file = os.path.join(RP_path, "pack.png")
    lang_json_path = os.path.join(lang_path, f"{MixedLangFileName}.json")
    # ensure paths exist
    if not os.path.exists(RP_path) or not os.path.exists(lang_path):
        os.makedirs(lang_path)
        print(f"Folder '{RP_path}' created.")
    else:
        print(f"Folder '{RP_path}' already exists.")

    # add / update the files
    shutil.copyfile(src=resource_path(SourcePackPNG),dst=pack_png_file)

    write_json_fromat_japanese(data=PackMCMetaFileData, file_path=pack_mc_meta_file)

    write_json_fromat_japanese(data=lang_data, file_path=lang_json_path)

#### Read File ####

def read_json_format(path, encoding=None)->dict:
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)

#### Find Files ####

def get_index_path(minecraft_dir):
    return os.path.join(minecraft_dir, "assets", "indexes")

def get_index_list(indexes_dir):
    "Find JSON index file and order it from greatest number to smallest"
    # indexes_dir = os.path.join(minecraft_dir, "assets", "indexes")
    # get a list of valid index files from the index dir. this will only get files that have a number as an name. e.g. "17.json", "24.json"
    index_files = [file for file in os.listdir(indexes_dir) if file.endswith(".json") and os.path.splitext(file)[0].isdigit()]

    # For each filename, it strips the .json part (x[:-5]) and converts the remaining string to an integer.
    # It then sorts based on these integers.
    # reverse=True means it will sort in descending order (highest number first).
    index_files.sort(key=lambda file: int(os.path.splitext(file)[0]), reverse=True)

    if not index_files:
        print("No numbered index files found in:", indexes_dir)
        return None
    return index_files

def get_objects_dir(minecraft_dir):
    return os.path.join(minecraft_dir, "assets", "objects")

def get_hash_from_index(index_path, lang_key = "minecraft/lang/ja_jp.json"):
    index_data = read_json_format(index_path,encoding="utf-8")
    
    # Look for the Japanese language file
    if lang_key not in index_data["objects"]:
        print("Japanese language file not found in index.")
        return None
    return index_data["objects"][lang_key]["hash"]
    
def get_data_from_hash(objects_dir, hash_val):
    subfolder = hash_val[:2]
    filename = hash_val

    source_path = os.path.join(objects_dir, subfolder, filename)

    print(f"Loading lang file from: {source_path}")

    if not os.path.exists(source_path):
        print("Hash file not found:", source_path)
        return None

    lang_dict = read_json_format(path=source_path, encoding="utf-8")
    return lang_dict

def get_lang_from_minecraft_indexes(minecraft_dir):
    '''Finds and loads the Japanese lang file from the newest index'''

    indexes_dir = get_index_path(minecraft_dir)
    objects_dir = get_objects_dir(minecraft_dir)

    # Find JSON index file and order it from greatest number to smallest
    index_files = get_index_list(indexes_dir)
    if not index_files:
        return None

    # we will go thru the index files to try to get the translation
    # it should be the first one, but it might not always be.
    is_latest_translation = True
    for index_file in index_files:
        print(f"Checking translation from index file: {index_file}")

        index_path = os.path.join(indexes_dir, index_file)

        hash_val = get_hash_from_index(index_path)
        lang_dict = get_data_from_hash(objects_dir, hash_val)
        if lang_dict:
            return lang_dict, is_latest_translation
        is_latest_translation is False # this will resualt in a warning if it is False
    return False
    

def get_furigana_lang(furigana_rp_zip, target_file):
    with zipfile.ZipFile(furigana_rp_zip, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        print("Files in the archive:", file_list)

        if target_file in file_list:
            with zip_ref.open(target_file) as file:
                # Read and decode JSON content
                content = file.read().decode('utf-8')
                data = json.loads(content)
                return data
        else:
            print(f"'{target_file}' not found in archive.")
            return None

def mix_dicts(kanji, furigana, percentage_from_kanji):
    # Only consider keys that are in both dictionaries
    common_keys = list(kanji.keys() & furigana.keys())
    
    # Calculate how many keys to take from master
    num_from_master = max(1, int(len(common_keys) * percentage_from_kanji / 100))

    # Randomly select keys to take from master
    keys_from_master = set(random.sample(common_keys, num_from_master))

    # Build the mixed dictionary
    mixed = {}
    for key in common_keys:
        if key in keys_from_master:
            mixed[key] = kanji[key]
        else:
            mixed[key] = furigana[key]

    return mixed

def get_lang_file_list(furigana_rp_zip):
    target_folder = RP_lang_folder
    with zipfile.ZipFile(furigana_rp_zip,"r") as zip:
        file_list = zip.namelist()
        json_files = [f for f in file_list if f.startswith(target_folder) and f.endswith('.json')]
        return json_files
