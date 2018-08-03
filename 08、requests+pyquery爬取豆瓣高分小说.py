import time

import tqdm
import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq


def get_page(url):
    ua = UserAgent().chrome
    headers = {'User-Agent': ua}
    data = requests.get(url, headers=headers)
    if data.status_code == 200:
        return data.text
    return None


def solve_html(html):
    doc = pq(html)
    names = doc('.title [target=_blank]').items()
    scores = doc('.rating .rating_nums').items()
    msgs = doc('.abstract').items()
    comments = doc('.comment').items()
    with open('豆瓣高分小说.txt', 'a', encoding='utf_8') as f:
        for name, score, msg, comment in zip(names, scores, msgs, comments):
            name = '书名：' + str(name.text())
            # print(name)
            msg = str(msg.text())
            score = '评分：' + str(score.text())
            comment = str(comment.text())
            f.write('\n'.join([name, msg, score, comment]))
            f.write('\n' * 2 + '*' * 80 + '\n' * 2)


def main(num):
    url = 'https://www.douban.com/doulist/37533097/?start={}&sort=seq&sub_type='.format(num)
    html = get_page(url)
    return solve_html(html)


if __name__ == '__main__':
    num = 25
    for i in tqdm.tqdm(range(5)):
        main(num * i)
        time.sleep(1)
