import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

imgdbAPI = "https://api.imgbb.com/1/upload"
nook_base_url = "https://nookipedia.com"
API_KEY = os.getenv("IMGDB_APIKEY")

def save_img(url):
    '''
    Saves given image URL to imgdb and returns the stored URL
    '''    
    params = {"key": API_KEY, "image": url}
    results = requests.post(imgdbAPI, params=params)
    
    if (results.status_code >= 400):
        print(f"[imgscrapper.py] Error failed to upload thumbnail at imgdb!")
        print(results.json()["error"]["message"])
        return None
    else:
        return results.json()['data']['url']

def get_song_info(title):
    '''
    From given song title (str) get thumbnail URL
    '''
    info = {
        "music": {
            "aircheck": "",
            "live": ""
        }, 
        "thumbnail": ""
    }
    
    url = nook_base_url + "/wiki/" + title.replace(' ', '_')
    print(f"[infoscrapper.py] Scraping {title} information from nookipedia...")
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    table = soup.find("table", {"class": "infobox"})
    trs = table.find_all("tr")
    img_anchor = trs[5].find("a")
    
    # Get flac link
    info["music"]["aircheck"] = trs[7].find("audio")["src"]
    info["music"]["live"] = trs[9].find("audio")["src"]
    
    img_url = nook_base_url + img_anchor["href"]
    
    # Image wiki page
    img_results = requests.get(img_url)
    img_soup = BeautifulSoup(img_results.text, "html.parser")
    img_div = img_soup.find("div", {"class": "fullImageLink"})
    img_anchor = img_div.find("a")
    
    full_img_url = img_anchor["href"]
    print(f"[infoscrapper.py] Uploading {title} to imgdb...")
    
    info["thumbnail"] = save_img(full_img_url)
    
    return info