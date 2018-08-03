# 爬取猫眼电影Top100
import re
import requests
import json
import time
import tqdm


# 第一步：获取网页源码
def get_one_page(url):
    # proxies = {'http': 'http://112.111.217.188:38093',
    #            'https': 'https://112.111.217.188:38093'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/66.0.3359.139 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    # return None


# 提取信息
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
        '.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    results = pattern.findall(html)
    for result in results:
        yield {'排名': result[0],
               '海报': result[1],
               '电影名': result[2],
               '主演': result[3].strip()[3:],
               '上演时间': result[4].strip()[5:],
               '评分': result[5].strip() + result[6].strip()
               }
        # print(result)


# 存储信息
def write_to_file(msg):
    with open('猫眼电影Top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(msg, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for msg in parse_one_page(html):
        write_to_file(msg)


if __name__ == '__main__':
    # tqdm 是进度条函数
    for i in tqdm.tqdm(range(10)):
        main(i * 10)
        time.sleep(1)
