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
