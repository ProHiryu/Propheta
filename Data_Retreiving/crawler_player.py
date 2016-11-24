# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3

driver = webdriver.Firefox()
driver.get("http://www.wanplus.com/lol/playerstats")

conn = sqlite3.connect('lol.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Player;

CREATE TABLE Player (
    id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name           TEXT,
    team           TEXT,
    role           TEXT,
    show_times     INTEGER,
    kda            REAL,
    contribution   REAL,
    kill_avg       REAL,
    kill_most      INTEGER,
    dead_avg       REAL,
    dead_most      INTEGER,
    assist_avg     REAL,
    assist_most    INTEGER,
    gpm            INTEGER,
    cspm           REAL,
    dpm            INTEGER,
    damage         REAL,
    apm            INTEGER,
    afford         REAL,
    wpm            REAL,
    exwpm          REAL
);
''')

for i in range(144):
    table = driver.find_element_by_tag_name('table')
    table_rows = table.find_elements_by_tag_name('tr')
    for tr in table_rows:
        td = tr.find_elements_by_tag_name('td')
        row = [i.text for i in td]
        if len(row) == 0:
            continue
        cur.execute('''INSERT INTO Player (name, team, role, show_times, kda, contribution,
            kill_avg, kill_most, dead_avg, dead_most, assist_avg) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
            ( row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11] ) )
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
        cur.execute('''UPDATE Player SET assist_most = ?, gpm = ?, cspm = ?, dpm = ?, damage = ?, apm = ?,
            afford = ?, wpm = ?,  exwpm = ? WHERE id = ?''',( row[2], row[3], row[4], row[5], row[6], row[7],
                                                              row[8], row[9], row[10], row[0] ))
        print(row)

    page_button = driver.find_element_by_id('DataTables_Table_0_next')
    page_button.click()
    time.sleep(1)

    page_button = driver.find_element_by_xpath('html/body/div[2]/div[2]/div[1]/div[1]')
    page_button.click()
    time.sleep(1)

conn.commit()