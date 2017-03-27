from bs4 import BeautifulSoup as bs
import urllib.request
import sqlite3
import json
import requests
from pprint import pprint


url = 'http://api.best.gg/v1/standings/teams'

payload = {'acceptLanguage': 'zh-cn', 'authToken': '$2y$10$pNWqRyslkIFZ4IGLl6nC3uEwLcrAIcTTrrDczikbf5SRyaXJNE2HG',
           'year': '2017', 'competition': '140'}

r = requests.get(url, params=payload)

if r.status_code == 200:
    data = json.loads(r.text)

teams = data['content']['body']['teams']

for team in teams:
    print ('{} : {}'.format(team['name'],team['pp']))
