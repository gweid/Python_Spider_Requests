import time

import tqdm
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# 获取单页网页源码
def get_page(url):
    ua = UserAgent().chrome
    headers = {'User-Agent': ua}
    data = requests.get(url, headers=headers)
    if data.status_code == 200:
        return data.content
    return None


# 分析、提取和存储信息
def solve_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for items in soup.find_all('ol'):
        for item in items.find_all('li'):
            # 获得排名
            ranks = item.find_all('em', class_='')
            # 获得电影名，因为网页html有两个<span class='title'>，所以取第一个
            names = item.find_all('span', class_='title')[0]
            # 获取电影导演、演员、地区等信息
            msgs = item.find_all('p', class_='')
            # 获取评分
            scores = item.find_all('span', attrs={'class': 'rating_num', 'property': 'v:average'})
            # 进行存储
            with open('豆瓣影Top250.txt', 'a', encoding='utf_8') as f:
                for rank, name, msg, score in zip(ranks, names, msgs, scores):
                    rank = str('>' * 50 + 'Top：' + rank.get_text() + '<' * 50)
                    name = str('电影名：' + name.strip())
                    msg = str('电影信息：' + msg.get_text().strip())
                    score = str('评分：' + score.get_text())
                    f.write('\n'.join([rank, name, msg, score]))
                    f.write('\n' * 2)


def main(num):
    url = 'https://movie.douban.com/top250?start=%s&filter='.format(num)
    html = get_page(url)
    return solve_html(html)


if __name__ == '__main__':
    # 获取全部的
    num = 25
    for i in tqdm.tqdm(range(10)):
        main(num * i)
        time.sleep(1)
