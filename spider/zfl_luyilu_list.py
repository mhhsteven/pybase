'''
Created on 2018年08月21日

@author: mhh
'''

from urllib import request
from bs4 import BeautifulSoup

response = request.urlopen('https://52zfls.com/luyilu/list_5_1.html')
html = response.read()
html_string = html.decode('gb18030')
#print(html_string)
soup = BeautifulSoup(html_string,"html5lib")
article_list = soup.find_all('article',attrs={'class':'excerpt excerpt-one'})
for article in article_list:
    print(article.find_all('a')[1].get('href'))