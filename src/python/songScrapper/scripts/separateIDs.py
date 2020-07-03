import os
import json
from uuid import uuid4

apiBaseLink = "./src/api/songVids/"
originDir = "./src/api/acnh_songs.json"
newSongs = []

# Open file as Read mode
with open(originDir, "r", encoding="UTF-8") as file:
    songs = json.load(file)
    
    # Create new array of songs
    '''
    {
        "id": Unique ID,
        "title": Title,
        "youtube": []
    }
    '''
    for song in songs:
        newSong = {}
        newSong["id"] = song["id"]
        newSong["title"] = song["kor_title"]
        newSong["youtube"] = song["youtube"]
        newSongs.append(newSong)
    file.close()

for newSong in newSongs:
    newDir = apiBaseLink + newSong["id"] + ".json"
    # Open file as Write mode
    with open(newDir, "w", encoding="UTF-8") as file:
        file.write(json.dumps(newSong, ensure_ascii=False))
        file.close()