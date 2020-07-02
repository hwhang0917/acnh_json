from webscrapper import get_songs
from chalice import Chalice

app = Chalice(app_name='lambda-songScrapper')

@app.route("/")
def get_hello():
    return get_songs()