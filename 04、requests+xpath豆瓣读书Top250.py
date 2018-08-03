# 用requests+xpath爬取豆瓣图书

import tqdm
import time
import requests
from lxml import etree
from fake_useragent import UserAgent


# 获取网页源码
def get_page(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 分析html文本，并保存结果
def parse_page(html):
    '''从浏览器选中书名右键检查后copyXpath可以获得xpath，有些多余的需要手动删掉，参考
    https://zhuanlan.zhihu.com/p/32041132，要获取文本，需在copy的xpath后加上@title----
    这样获取xpath主要是避免手动写xpath会爬取到空行的问题'''
    res = etree.HTML(html)
    name = res.xpath('//*[@id="content"]/div/div[1]/div/table/tr/td[2]/div[1]/a/@title')
    msg = res.xpath('//p[@class="pl"]/text()')
    score = res.xpath('//div[@class="star clearfix"]//span[@class="rating_nums"]/text()')
    with open('豆瓣图书.txt', 'a', encoding='utf-8') as f:
        for (a, b, c) in zip(name, msg, score):
            f.write('\n'.join([a, b, c]))
            f.write('\n' + '=' * 60 + '\n')


def main(start):
    url = 'https://book.douban.com/top250?start=' + str(start)
    html = get_page(url)
    results = parse_page(html)
    return results


if __name__ == '__main__':
    start = 25
    for i in tqdm.tqdm(range(10)):
        main(start * i)
        time.sleep(1)
