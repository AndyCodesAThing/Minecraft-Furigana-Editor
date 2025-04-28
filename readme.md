This is a learning Tools I am making to assist in learning japanese

Minecarft stores its language files in ".minecraft/assets/indexes/" you will have files that look like "##.json" such as "24.json"
- there is no way of telling what version these are ment for, so I just tries to get the latest version
- These files are downloaded when the game needs them. once they have been downloaded, they stay there.

# Feature Ideas
1. shearch and edit individual items
    - I will use the TK Tree view for this. 
    - It will let you slect if you always want kanji with or without furigana for that item.
    - the changes will be saved to a specific file so they can be aplied every time you randomise
2. highlighted words that you are having difficulty with 
    - this can be acomplished using minecraft's Formatting codes
    - https://minecraft.wiki/w/Formatting_codes 

# How I make the exe
I use PyInstaller 

to make the exe use this comand
    pyinstaller --onefile --add-data "assets;assets" src/main.py