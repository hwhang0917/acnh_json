import json
from uuid import uuid4

songJsonLink = "./src/api/acnh_songs.json"

# Open file as Read mode
with open(songJsonLink, "r", encoding="UTF-8") as file:
    songs = json.load(file)
    
    # Save unique ID in songs
    for song in songs:
        ID = {"id": "_" + str(uuid4()).split("-")[0]}
        song.update(ID)
    file.close()
    
# Open file as Write mode
with open(songJsonLink, "w", encoding="UTF-8") as file:
    file.write(json.dumps(songs, ensure_ascii=False))
    file.close()