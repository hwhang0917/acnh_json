import json
from webscrapper import get_songs

# This code is live on Repl.it
# https://acnhsongscrapper--hwhang0917.repl.co/

songJsonLink = "./src/api/acnh_songs.json"

songs = get_songs()

print("[main.py] Writing as JSON file...")
with open(songJsonLink, "w", encoding="UTF-8") as file:
    file.write(json.dumps(songs, ensure_ascii=False))
    file.close()
