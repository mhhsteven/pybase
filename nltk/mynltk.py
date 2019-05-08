'''
Created on 2018年08月21日 09:15:56

@author: mhh
'''

# import nltk

# nltk.download()

from bs4 import BeautifulSoup
from pylab import mpl
import urllib.request
import nltk
import jieba, math
import jieba.analyse

response = urllib.request.urlopen('http://www.zhihu.com')
html = response.read()
soup = BeautifulSoup(html, "html5lib")
text = soup.get_text(strip=True)
# tokens = [t for t in text.split()]
# freq = nltk.FreqDist(tokens)
# for key, val in freq.items():
#     print(str(key) + ':' + str(val))
# freq.plot(20, cumulative=False)

jieba.analyse.set_stop_words('D:\\Python\\tingyongci_zh.txt')
fenci = jieba.analyse.extract_tags(text, topK=100, withWeight=True)
for v, n in fenci:
    #权重是小数，为了凑整，乘了一万
    print(v + '\t' + str(int(n * 10000)))
#fenci = jieba.cut(text, cut_all=False)
#list = list(fenci)
#print('全模式分词：{%d}' % len(list(str_quan1)))
#print('='.join(list))

#freq = nltk.FreqDist(list)
#mpl.rcParams['font.sans-serif'] = ['SimHei']
#freq.plot(20, cumulative=False)
