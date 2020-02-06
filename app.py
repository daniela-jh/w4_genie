import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbgenie

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

musics = soup.select('table.list-wrap > tbody > tr')

rank = 1
for music in musics:

    title_tag = music.select_one('td.info > a.title')

    if title_tag is not None:
        title = title_tag.text
        title_strip = title.strip()
        artist = music.select_one('a.artist').text
        # print(rank, title_strip, artist)
        doc = {
            'rank': rank,
            'title': title_strip,
            'artist': artist
        }
        db.musics.insert_one(doc)
        rank += 1

