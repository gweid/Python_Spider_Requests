# 爬取豆瓣电影250
import time
import requests
from pyquery import PyQuery
from tqdm import tqdm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/66.0.3359.139 Safari/537.36'}
n = 25
for i in tqdm(range(10)):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i * n)
    html = requests.get(url, headers=headers).text
    doc = PyQuery(html)
    results = doc('.grid_view li')
    for result in results.items():
        index = 'TOP' + result.find('em').text()
        name = '电影名：' + result.find('.title').text()
        msg = '电影信息：' + result.find('p').text()
        score = '评分：' + result.find('.rating_num').text()
        with open('豆瓣电影TOP250.txt', 'a', encoding='utf-8') as f:
            f.write('\n'.join([index, name, msg, score]))
            f.write('\n' * 2 + '*' * 90 + '\n' * 2)
            time.sleep(0.1)
