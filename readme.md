This is a learning Tools I am making to assist in learning Japanese

This program will take Minecraft's default Japanese Translation and mix it with a furigana resource pack that you provide.
I use this one - https://modrinth.com/resourcepack/furigana/versions
it should work with any furigana Resource pack.
You are able to adjust the percentage of kanji without furigana.

# Usage
when running for the first time just follow the messages you see. if you need to, you can change the paths later in the settings tab.
After that, just enter a Number into the field and click run.

once you are in minecraft, if you have it save into the resource pack folder. then all you have to do is 
1. activate the resource pack
2. set your language to 日本語 Furigana Scrambler

then that should be it.

once you have all that setup, you are now able randomise the Furigana while Minecraft is running
just follow these steps
1. hit the run button
2. in Minecraft press "F3 + T" to reload the Resource Pack

# some info about the minecraft language files
Minecarft stores its language files in ".minecraft/assets/objects/". the index file tells you what file it is. the indexes are stored in ".minecraft/assets/indexes/" you will have files that look like "##.json" such as "24.json"
- there is no way of telling what version these are meant for, so the program just tries to get the latest version
- These files are downloaded when the game needs them. once they have been downloaded, they stay there.

# Feature Ideas
1. search and edit individual items
    - I will use the TK Tree view for this. 
    - It will let you select if you always want kanji with or without furigana for that item.
    - the changes will be saved to a specific file so they can be applied every time you randomise
2. highlighted words that you are having difficulty with 
    - this can be accomplished using minecraft's Formatting codes
    - https://minecraft.wiki/w/Formatting_codes 

# How I make the exe
I use PyInstaller 

to make the exe use this command
    python -m PyInstaller --onefile --add-data "assets;assets" src/main.py


