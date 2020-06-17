import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from vidscrapper import get_youtube_links

NAMU_URL = "https://namu.wiki/w/%EB%8F%99%EB%AC%BC%EC%9D%98%20%EC%88%B2%20%EC%8B%9C%EB%A6%AC%EC%A6%88/%EB%85%B8%EB%9E%98%20%EB%AA%A9%EB%A1%9D"

def isAnchor(title):
    if "<a" in title:
        return True
    else:
        return False

def get_songs():
    songs = []

    # Get Soup
    print("[scrapper.py] Scraping from Namu.wiki ...")
    results = requests.get(NAMU_URL)
    soup = BeautifulSoup(results.text, "html.parser")

    tables = soup.find_all("table", {"class": "wiki-table"})
    song_table = tables[5]

    song_trs = song_table.find_all("tr")
    
    # Scrape songs from table
    for song_tr in song_trs[1:96]:
        song = {
            "id": "_" + str(uuid4()).split("-")[0],
            "kor_title": "",
            "eng_title": "",
            "thumbnail": "",
            "youtube": []
        }

        song_title_td = song_tr.find_all("td")[1]
        song["thumbnail"] = str(song_tr.find("img")["src"])
        title_div = song_title_td.find("div", {"class": "wiki-paragraph"})
        if isAnchor(str(title_div.contents[0])):
            song["kor_title"] = str(title_div.contents[0].text)
        else:
            song["kor_title"] = str(title_div.contents[0])
        print(song["kor_title"])
        song["eng_title"] = str(title_div.find_all(
            "span", {"class": "wiki-size"})[-1].get_text(strip=True))
        song["youtube"] = get_youtube_links(song["eng_title"])
        
        songs.append(song)

    return songs