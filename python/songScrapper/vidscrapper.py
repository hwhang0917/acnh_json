import requests
import json
import os
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

# API configuration
youtubeAPI = "https://www.googleapis.com/youtube/v3/search"
API_KEY = os.getenv("GOOGLE_APIKEY")
ytlink_template = "https://www.youtube.com/watch?v="

def get_youtube_links(title):
    if not "K.K." in title:
        title = title + " Animal Corssing"
        
    print(f"[vidscrapper.py] {{Query = {title}}} : Scraping from YouTube ...")
    links = []
    
    params = {"key": API_KEY, "part": "snippet", "q": title, "maxResults": "5", "type": "video"}
    results = requests.get(youtubeAPI, params=params)
    
    if (results.status_code == 403):
        return None
    
    videos = json.loads(results.text)["items"]
    
    for video in videos:
        youtube_video = {
            "title": "",
            "link": ""
        }
        
        youtube_video["title"] = video["snippet"]["title"]
        youtube_video["link"] = ytlink_template + video["id"]["videoId"]
        
        links.append(youtube_video)
      
    return links

# print(get_youtube_links("K.K. Idol"))