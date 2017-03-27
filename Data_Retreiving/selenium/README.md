---
title: Game Prediction System Part 1
date: 2016-11-24 18:06:07
tags:
- beautifulsoup
- machine learning
- sqlite
- python
- databases
---

# **Game Prediction System Part 1**

## **Data Retrieving**

### *Data Source and version control*
+ [Data Source](http://www.wanplus.com/lol "WAN PLUS")
+ [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html "BeautifulSoup4")
+ [Python35](https://www.python.org/downloads/ "python 3.5.2")
+ [selenium](http://www.seleniumhq.org/ "selenium 3.0.1")
+ [geckodriver](https://github.com/mozilla/geckodriver/releases/ "geckodriver-v0.11.1-arm7hf")
+ [DB browser](http://sqlitebrowser.org/ "DB browser")

---
#### crawler with PyQt and BS4

+ BeautifulSoup is just a Web page parser,cannot use for ajax or other dynamic pages,or it is very difficult to achieve it.There is a [video](https://www.youtube.com/results?search_query=dynamic+webpage+beautifulsoup "PyQt BS4") on youtube offers an solution. It simulates an browser client to get the dynamic pages,so you can just use BS4 to parse the ajax pages,just as follows:

+ Code:

<!-- more -->

```python
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import urllib.request
import bs4 as bs
# from BeautifulSoup import *

class Client(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()



url = 'http://www.wanplus.com/lol/playerstats'
clien_response = Client(url)
source = clien_response.mainFrame().toHtml()

soup = bs.BeautifulSoup(source, 'html.parser')
table = soup.find('table')

table_rows = table.find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print (row)

```

+ However this way cannot turn the page down to another page,so we can just get the first page of 144 pages.So,in this system,we will not use this way to get the players and teams data,selenium will be the best way to get it,as for bs4,in the games data retrieving, we will see it again
+ There are some attentions:
  - You'd best to choose PyQt4,this release is the most mature version
  - No matter PyQt4 or PyQt5,it is just compatible to the Python 3.4.2 or less. (~~a very big hole~~)
  - Once you have changed your python release,you'd better change your system environment variables to fit it
  - Everything with BeautifulSoup is the same as before or follow

---

#### crawler with selenium

+ Selenium it a library that can help you to simulate a browser behavior and get the ajax data that you can't get on the formal situation
+ First you need to get a selenium,and geckodriver as before i said
+ Then a DB browser is neccessary for you to visuilizate your database
+ Code:

```python
# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3

driver = webdriver.Firefox()
driver.get("http://www.wanplus.com/lol/teamstats")

conn = sqlite3.connect('lol.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Team;

CREATE TABLE Team (
    id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name         TEXT,
    kda          REAL,
    kill_avg     REAL,
    dead_avg     REAL,
    dpm          INTEGER,
    fb_rate      REAL,
    time_avg     TEXT,
    gold_avg     INTEGRE,
    cs_avg       REAL,
    dragon_avg   REAL,
    dragon_rate  REAL,
    baron_avg    REAL,
    baron_rate   REAL,
    wpm          REAL,
    exepm        REAL,
    tower_avg    REAL,
    extower_avg   REAL
);
''')

for i in range(16):
    table = driver.find_element_by_tag_name('table')
    table_rows = table.find_elements_by_tag_name('tr')
    for tr in table_rows:
        td = tr.find_elements_by_tag_name('td')
        row = [i.text for i in td]
        if len(row) == 0:
            continue
        cur.execute('''INSERT OR IGNORE INTO Team (name, kda, kill_avg, dead_avg, dpm, fb_rate,
                    time_avg, gold_avg, cs_avg) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                    ( row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9] ) )
        print(row)

    page_button = driver.find_element_by_xpath('html/body/div[2]/div[2]/div[1]/div[2]')
    page_button.click()
    time.sleep(1)

    table = driver.find_element_by_tag_name('table')
    table_rows = table.find_elements_by_tag_name('tr')
    for tr in table_rows:
        td = tr.find_elements_by_tag_name('td')
        row = [i.text for i in td]
        if len(row) == 0:
            continue
        cur.execute('''UPDATE Team SET dragon_avg = ?, dragon_rate = ?, baron_avg = ?, baron_rate = ?, wpm = ?, exepm = ?,
                    tower_avg = ?, extower_avg = ? WHERE id = ?''',( row[2], row[3], row[4], row[5], row[6], row[7],
                                                                      row[8], row[9], row[0] ))
        print(row)

    page_button = driver.find_element_by_xpath(".//*[@id='DataTables_Table_0_next']")
    page_button.click()
    time.sleep(1)

    page_button = driver.find_element_by_xpath('html/body/div[2]/div[2]/div[1]/div[1]')
    page_button.click()
    time.sleep(1)

conn.commit()
```

+ The code is very easy to understand,we create a sqlite3 db and put our data into it,that's it
+ And also there is some attentions:
  - Once you get a geckodriver,if you want to use ``driver = webdriver.Firefox()``,you need to add the geckodriver's path to the system environment variable **path**,press shift and click right,you can get the whole path.
  - The way to get players data is almost the same with teams
  - Name cloumn in table should not be unique because one player can be in many teams in different period
  - That's it
+ **Today that's all,in the next part we will try to get games data using bs4 and urllib,that will be much more easier,see you~**



---
title: Game Prediction System Part 2
date: 2016-11-25 19:14:32
tags:
- beautifulsoup
- machine learning
- sqlite
- python
- databases
---
# **Game Prediction System Part 2**

## **Data Retrieving**

### *Data Source and version control*
+ [Data Source](http://www.wanplus.com/lol "WAN PLUS")
+ [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html "BeautifulSoup4")
+ [Python35](https://www.python.org/downloads/ "python 3.5.2")
+ [selenium](http://www.seleniumhq.org/ "selenium 3.0.1")
+ [geckodriver](https://github.com/mozilla/geckodriver/releases/ "geckodriver-v0.11.1-arm7hf")
+ [DB browser](http://sqlitebrowser.org/ "DB browser")

---
#### crawler with Urllib and BS4
+ Something just be different with last part's website,the web page on [WAN PLUS](http://www.wanplus.com/lol/event?t=3&page=1 "WAN PLUS") has changed,this become a static webpage,so that we can just use bs4 to get what we want
+ First Step is to get the different game series's order. The order is very important,the urls http://www.wanplus.com/event/173.html have different order like 173 and so on,so we must find every series' order.At the first time i want to find all the orders myself,and i found that it is two much workload. So,i put it to the work to the bs4,as follows:

<!-- more -->
##### Code1:

```python
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
# ......
```
+ *these are some orders that i have found before..*

##### Code2
```python
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
```
+ *use sql to create the table*

```python
for i in range(8):
    url = base_url + str(i+1)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    links = soup.findAll('div',class_ = 'text_t')
    for link in links:
        print (link.find('a').get('href'))
        # num = re.findall('[0-9]+',link.find('a').get('href'))
        new_urls.append('http://www.wanplus.com' + link.find('a').get('href'))

print (new_urls)
```
+ *in this code segment,i use bs4 to find every order in the tag a's attribute href's text,at the first time i want to use REGEX to find the numbers,and then i found that the text is the url's portion,just use it*

##### Code3
```python
for url in new_urls:
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('div',class_ = 'caption-outer')
    duration = soup.find('div',class_ = 'caption-outer').find('span').text
    str = title.contents[1].text
    if str[0] == ' ':
        str = str[1:]
    print (str)
    bo = 0
    games = soup.findAll('div',class_ = 'match-team')
    for game in games:
        team = game.findAll('span',class_ = 'team-name')
        result = game.find('em',class_ = 'team-vs').findAll('i')
        team_name = [i.text for i in team]
        game_result = [int(i.text) for i in result]
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
                       result2, bo) VALUES ( ?, ?, ?, ?, ?, ?, ? )''',( str, duration, team_name[0], team_name[1],
                                                                    game_result[0], game_result[1], bo ))
        print (bo)


conn.commit()

```
+ *find 'match-team','team-name','team-vs',we can get the team information and game information includes duration and series name,so that we can put them into our database 'lol'*
+ There are also some tips and notes:
  - use class name in bs4 should be like this `title = soup.find('div',class_ = 'caption-outer')`,other usages you should read the [documentations](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html "BeautifulSoup4")
  - everything in db should not be unique except id
  - just use bs4 for you to find something you don't want to do ti hand by hand
  - don't forget to commit your database after everything has done
  - the way to classify number of BO is still a problem, hope i will resolve it later
+ That's all we get the game informations, in the next part we may be start our machine learning portion,very excited!
+ *See you*
