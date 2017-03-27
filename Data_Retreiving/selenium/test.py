import bs4 as bs
import urllib.request

url = 'http://lishi.tianqi.com/shantou/201101.html'

source = urllib.request.urlopen(url)

soup = bs.BeautifulSoup(source,'html.parser')

uls = soup.find_all('ul')

for ul in uls:
    lis = ul.find_all('li')
    if len(lis[0].text) == 10:
        for li in lis:
            print(li.text)
