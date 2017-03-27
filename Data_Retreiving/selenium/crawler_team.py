# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3

driver = webdriver.Chrome()
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

for i in range(1):
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

driver.quit()
