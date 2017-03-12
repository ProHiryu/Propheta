# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3
import re
import urllib.request
from bs4 import BeautifulSoup
import datetime

# games_order = dict()
# games_order['IEM_Oakland_2016'] = 311
# games_order['NEST_2016'] = 298
# games_order['KeSPA_2016'] = 303
# games_order['S_2016'] = 177
# games_order['LPL_Regional_Qualifier_2016'] = 250
# games_order['Demacia_2016'] = 230
# games_order['LMS_Summer_2016'] = 221
# games_order['LCS_NA_Summer_2016'] = 217
# games_order['LCS_EU_Summer_2016'] = 216
# games_order['LPL_Summer_2016'] = 218
# games_order['LCK_Summer_2016'] = 215
# games_order['MSI_2016'] = 178
# games_order['IEM_Katowice_2016'] = 176
# games_order['LMS_Spring_2016'] = 173
# games_order['LCS_NA_Spring_2016'] = 169
# games_order['LCS_EU_Spring_2016'] = 170
# games_order['LPL_Spring_2016'] = 165
# games_order['LCK_Spring_2016'] = 172
# games_order['IEM_Cologne_2015'] = 164
# games_order['NEST_2015'] = 154
# games_order['Demacia_2015'] = 158
# games_order['IEM_San_Jose_2015'] = 152
# games_order['KeSPA_2015'] = 157
# games_order['S_2015'] = 136

new_urls = []
base_url = 'http://www.wanplus.com/lol/event?t=3&page='

conn = sqlite3.connect('lol.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Games ;

CREATE TABLE Games (
id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
duration TEXT,
series   TEXT,
team1    TEXT,
team2    TEXT,
result1  INTEGER,
result2  INTEGER,
bo       INTEGER
);
''')

for i in range(8):
    url = base_url + str(i + 1)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.findAll('div', class_='text_t')
    for link in links:
        # print (link.find('a').get('href'))

        # num = re.findall('[0-9]+',link.find('a').get('href'))
        new_urls.append('http://www.wanplus.com' + link.find('a').get('href'))

print (new_urls)

for url in new_urls:
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='caption-outer')
    duration = soup.find('div', class_='caption-outer').find('span').text
    str = title.contents[1].text
    if str[0] == ' ':
        str = str[1:]
    # print (str)
    bo = 0
    games = soup.findAll('div', class_='match-team')
    for game in games:
        team = game.findAll('span', class_='team-name')
        result = game.find('em', class_='team-vs').findAll('i')
        team_name = [i.text for i in team]
        game_result = [int(i.text) for i in result]
        if len(game_result) > 0:
            if max(game_result) == 1:
                if sum(game_result) == 1:
                    bo = 1
                elif sum(game_result) == 2:
                    bo = 2
            elif max(game_result) == 2:
                bo = 3
            elif max(game_result) == 3:
                bo = 5
            cur.execute('''INSERT OR IGNORE INTO Games (series, duration, team1, team2, result1,
                           result2, bo) VALUES ( ?, ?, ?, ?, ?, ?, ? )''', ( str, duration, team_name[0], team_name[1],
                                                                             game_result[0], game_result[1], bo))
            print (bo)


conn.commit()
