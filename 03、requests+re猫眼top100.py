import re
import tqdm
import time
import requests


def get_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/66.0.3359.139 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?class="name".*?a.*?>(.*?)</a></p>.*?class="star">(.*?)'
                         '</p>.*?class="releasetime">(.*?)</p>.*?class="integer">(.*?)</i>.*?fraction.*?>(.*?)</i>'
                         '.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        index = 'Top' + item[0]
        name = item[1]
        star = item[2].strip()
        releasetime = item[3].strip()
        score = '评分：' + item[4].strip() + item[5].strip()
        delimiter = '=' * 50 + '\n'
        with open('猫眼Top100.txt', 'a', encoding='utf-8') as f:
            f.write('\n'.join([index, name, star, releasetime, score, delimiter]))


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    result = parse_one_page(html)
    return result


if __name__ == '__main__':
    for i in tqdm.tqdm(range(10)):
        main(i * 10)
        time.sleep(1)