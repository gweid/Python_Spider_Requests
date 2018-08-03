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
        return data.text
    return None


# 解释网页获取信息并存储
def solve_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for items in soup.find_all('dl', class_='board-wrapper'):
        for item in items.find_all('dd'):
            # 获取电影排名
            ranks = item.find_all('i')[0]
            # 获取电影名
            names = item.find_all('p', class_='name')
            # 获取主演
            stars = item.find_all('p', class_='star')
            # 获取上映是时间
            releasetimes = item.find_all('p', class_='releasetime')
            # 获取评分
            scores_1 = item.find_all('i', class_='integer')
            scores_2 = item.find_all('i', class_='fraction')
            # 存储信息
            with open('猫眼影Top100.txt', 'a', encoding='utf_8') as f:
                for rank, name, star, releasetime, score_1, score_2 in zip(ranks, names, stars, releasetimes, scores_1,
                                                                           scores_2):
                    rank = 'Top：' + str(rank)
                    name = '电影名：' + str(name.get_text())
                    star = str(star.get_text().strip())
                    releasetime = str(releasetime.get_text())
                    score = '评分：' + str(score_1.get_text()) + str(score_2.get_text())
                    f.write('\n'.join([rank, name, star, releasetime, score]))
                    f.write('\n' + '>' * 30 + '<' * 30 + '\n')


def main(num):
    url = 'https://maoyan.com/board/4?offset=' + str(num)
    html = get_page(url)
    return solve_html(html)


# 获取全部
if __name__ == '__main__':
    num = 10
    # 通过tqdm加进度条
    for i in tqdm.tqdm(range(10)):
        main(num)
        time.sleep(1)
