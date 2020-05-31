# -*- coding: utf-8 -*-
import re
import csv
import requests
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import RequestException
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_one_page(city, keyword):
    '''
    获取网页html内容并返回
    '''
    paras = {
        'jl': city,  # 搜索城市
        'kw': keyword,  # 搜索关键词
        'kt': 3
        # 'isadv': 0,  # 是否打开更详细搜索选项
        # 'isfilter': 1,  # 是否对结果过滤
        # 'p': page,  # 页数
        # 're': region  # region的缩写，地区，2005代表海淀
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Host': 'sou.zhaopin.com',
        'Referer': 'https://www.zhaopin.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',

    }

    # url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' + urlencode(paras)
    url = 'https://sou.zhaopin.com/?jl=530&re=2006&kw=Python&kt=3' 
    try:
        # 获取网页内容，返回html数据
        response = requests.get(url)
        # print(response.encoding)  # 查看网页返回的字符集类型
        # print(response.apparent_encoding)  # 自动判断字符集类型
        # response.encoding = response.apparent_encoding
        # htmlA = response.text.encode('iso-8859-1').decode('gbk')
        # print(htmlA)
        # print(response.text)
        # 通过状态码判断是否获取成功
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        return None


def parse_one_page(html):
    '''
    解析HTML代码，提取有用信息并返回
    '''
    print(html)
    # print(html)
    # 正则表达式进行解析
    pattern = re.compile(
        '<span title="(.*?)" class="contentpile__content__wrapper__item__info__box__jobname__title">.*?</span>.*?'  # 匹配职位信息
        '<a href="(.*?)" title="(.*?)" target="_blank" class="contentpile__content__wrapper__item__info__box__cname__title company_title">.*?</a>.*?'  # 匹配公司网址和公司名称
        '<p class="contentpile__content__wrapper__item__info__box__job__saray">(.*?)</p>', re.S)  # 匹配月薪

    # 匹配所有符合条件的内容
    items = re.findall(pattern, html)


    for item in items:
        print("-----------" + item[0])
        job_name = item[0]
        job_name = job_name.replace('<b>', '')
        job_name = job_name.replace('</b>', '')
        yield {
            'job': item[0],
            'website': item[1],
            'company': item[2],
            'salary': item[3]
        }


def write_csv_file(path, headers, rows):
    '''
    将表头和行写入csv文件
    '''
    # 加入encoding防止中文写入报错
    # newline参数防止每写入一行都多一个空行
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)


def write_csv_headers(path, headers):
    '''
    写入表头
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def write_csv_rows(path, headers, rows):
    '''
    写入行
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)


def main(city, keyword):
    '''
    主函数
    '''
    filename = 'zl_' + city + '_' + keyword + '.csv'
    headers = ['job', 'website', 'company', 'salary']
    write_csv_headers(filename, headers)
    for i in tqdm(range(10)):
        '''
        获取该页中所有职位信息，写入csv文件
        '''
        jobs = []
        html = get_one_page(city, keyword)
        items = parse_one_page(html)
        for item in items:
            jobs.append(item)
        write_csv_rows(filename, headers, jobs)


if __name__ == '__main__':
    main('北京', 'Python')