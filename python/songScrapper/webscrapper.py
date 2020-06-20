import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from vidscrapper import get_youtube_links

NAMU_URL = "https://namu.wiki/w/%EB%8F%99%EB%AC%BC%EC%9D%98%20%EC%88%B2%20%EC%8B%9C%EB%A6%AC%EC%A6%88/%EB%85%B8%EB%9E%98%20%EB%AA%A9%EB%A1%9D"

def isAnchor(content):
    '''
    Check if given content is an anchor
    '''
    if content.name == "a":
        return True
    else:
        return False
    
def isRawString(content):
    '''
    Check if given content is a raw string with no tag
    '''
    if content.name:
        return False
    else:
        return True

def isNotTitle(content):
    '''
    Check if given element is a not part of title
    '''
    # content is Raw string (title)
    if not content.name:
        return False
    else:
        # Content is anchor
        if content.name == "a":
            # Content is footnote
            if "#fn" in content["href"]:
                return True
            # Content is not footnote
            else:
                return False
        # Content is not anchor nor raw string but something else (i.e. <br>)
        else:
            return True

def get_kor_title(title_div):
    kor_title = ""
    
    # Get the first two contents of title div
    contents = title_div.contents[:2]
    # Find all anchors in first two contents
    anchors = title_div.find_all("a")
    
    # If Anchor exists among first two contents
    if anchors:
        # If Both contents are anchors
        if isAnchor(contents[0]) and isAnchor(contents[1]):
            '''
            Only case this occurs is when first is an anchor and second is footnote
            i.e.) [<a href="#">Anchor</a>, <a href="#fn">Footnote</a>]
            '''
            kor_title = contents[0].get_text()
        # Only one of them is an anchor
        else:
            # Second part of the contents is not part of title
            if isNotTitle(contents[1]):
                '''
                Sample Cases:
                i.e.) [RawText, <a href="#fn">Footnote</a>] or [<a href="#">Title</a>, <br>]
                '''
                # Convert either rawstinr or anchor to title
                if isAnchor(contents[0]):
                    kor_title = contents[0].get_text()
                else:
                    kor_title = str(contents[0])
            # No footnote
            else:
                # Convert anchor content to string
                for i, content in enumerate(contents):
                    if isAnchor(content):
                        contents[i] = content.get_text()
                    else:
                        contents[i] = str(content)
                
                kor_title = ''.join(contents)
    # There are no anchors, return raw string
    else:
        kor_title = str(contents[0])
        
    return kor_title

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
        
        # Korean Title Scraping
        song["kor_title"] = get_kor_title(title_div)
        song["eng_title"] = str(title_div.find_all(
            "span", {"class": "wiki-size"})[-1].get_text(strip=True))
        song["youtube"] = get_youtube_links(song["eng_title"])
        
        songs.append(song)

    return songs

get_songs()