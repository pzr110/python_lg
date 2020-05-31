import requests
from bs4 import BeautifulSoup
import json
import time


def main():
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.7 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%8C%97%E4%BA%AC',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest'
    }

    positions = []
    for x in range(1, 6):
        data = {
            'first': 'true',
            'pn': x,
            'kd': 'python'
        }

        res = requests.post(
            "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false",
            headers=headers, data=data)
        json_result = res.json()
        print(json_result)
        page_positions = json_result['content']['positionResult']['result']
        positions.extend(page_positions)
        for position in positions:
            # 打印测试
            print("-" * 40)
            print(position)
        # 转化为Json字符串
        line = json.dumps(positions, ensure_ascii=False)
        # 保存
        with open('lagou.json', 'wb+') as fp:
            fp.write(line.encode('utf-8'))
        time.sleep(3)


if __name__ == '__main__':
    main()