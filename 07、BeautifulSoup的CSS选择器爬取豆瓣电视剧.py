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


def solve_html(html):
    soup = BeautifulSoup(html, 'lxml')
    names = soup.select('.title [target=_blank]')
    scores = soup.select('.rating .rating_nums')
    msgs = soup.select('.abstract')
    with open('豆瓣电视剧.txt', 'a', encoding='utf_8') as f:
        for name, score, msg in zip(names, scores, msgs):
            name = ' ' * 10 + '剧名：' + str(name.get_text().strip() + '\n')
            score = ' ' * 10 + '评分：' + str(score.get_text().strip('\n'))
            msg = str(msg.get_text())
            f.write('\n'.join([name, score, msg]))
            f.write('\n' + '>' * 30 + '<' * 30 + '\n')


def main(num):
    url = 'https://www.douban.com/doulist/3038463/?start={}&sort=seq&sub_type='.format(num)
    html = get_page(url)
    return solve_html(html)


if __name__ == '__main__':
    num = 25
    for i in tqdm.tqdm(range(5)):
        main(num)
        time.sleep(1)


