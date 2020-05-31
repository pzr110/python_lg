from lxml import etree
import requests
import time
import csv
import random

# 要爬取的网站链接
url = "https://www.lagou.com/zhaopin/Python/?labelWords=label"
# url = "https://www.lagou.com/jobs/list_Python/p-city_0?px=default#filterBox"
# 设置信息头，模拟人为操作，可以避免一些反爬虫
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36'}

res = requests.get(url, headers=head).content.decode("utf-8")
re = etree.HTML(res)
# 获得该页面翻页地址链接
# s_url = re.xpath("//div[@class='pager_container']/a[position()>2 and position()<30]/@href")
s_url = ['https://www.lagou.com/zhaopin/Python/2/',
         'https://www.lagou.com/zhaopin/Python/3/',
         'https://www.lagou.com/zhaopin/Python/4/',
         'https://www.lagou.com/zhaopin/Python/5/',
         'https://www.lagou.com/zhaopin/Python/6/',
         'https://www.lagou.com/zhaopin/Python/7/',
         'https://www.lagou.com/zhaopin/Python/8/',
         'https://www.lagou.com/zhaopin/Python/9/',
         'https://www.lagou.com/zhaopin/Python/10/',
         'https://www.lagou.com/zhaopin/Python/11/',
         'https://www.lagou.com/zhaopin/Python/12/',
         'https://www.lagou.com/zhaopin/Python/13/',
         'https://www.lagou.com/zhaopin/Python/14/',
         'https://www.lagou.com/zhaopin/Python/15/',
         'https://www.lagou.com/zhaopin/Python/16/',
         'https://www.lagou.com/zhaopin/Python/17/',
         'https://www.lagou.com/zhaopin/Python/18/',
         'https://www.lagou.com/zhaopin/Python/19/',
         'https://www.lagou.com/zhaopin/Python/20/',
         'https://www.lagou.com/zhaopin/Python/21/',
         'https://www.lagou.com/zhaopin/Python/22/',
         'https://www.lagou.com/zhaopin/Python/23/',
         'https://www.lagou.com/zhaopin/Python/24/',
         'https://www.lagou.com/zhaopin/Python/25/'
         ]
print('s_url=', s_url)
# 依次循环page1，page2等等
for x in s_url:
    res = requests.get(x, headers=head).content.decode("utf-8")
    re = etree.HTML(res)
    print('x==', x)
    # 获取当前页面下的所有招聘信息链接
    list_url = re.xpath(
        "//div[@class='s_position_list ']/ul/li[position()>=0 and position()<15]/div/div[1]/div/a/@href")
    print('list_url=', list_url)
    # 依次循环每个招聘信息，将标题，内容，薪资获取到
    for y in list_url:
        r01 = requests.get(y, headers=head).content.decode("utf-8")
        html01 = etree.HTML(r01)
        print('ALL==========', html01)
        print('y==', y)

        title = html01.xpath("string(//h1[@class='name'])")
        print('title===', title.replace(' ', ''))
        content = html01.xpath("string(//div[@class='job-detail'])")
        print('content===', content.replace(' ', ''))
        salary = html01.xpath("string(//span[@class='salary'])")
        print('salary===', salary.replace(' ', ''))
        require = html01.xpath("string(//h3)")
        address = require.replace(' ', '').split('/')[1]
        print('address===', address)
        undergo = require.replace(' ', '').split('/')[2]
        print('undergo===', undergo)
        edu = require.replace(' ', '').split('/')[3]
        print('edu===', edu)
        # 设置休眠是防止网站识别自己，最好是random休眠
        time.sleep(random.randint(5, 10))
        # 保存爬虫信息内容
        headers = ['title', 'content', 'salary']
        rows = [title, salary, address, undergo, edu, content]

        with open("cn-blog.csv", "a+", encoding="utf-8") as file:
            f_csv = csv.writer(file)
            # f_csv.writerow(headers)
            f_csv.writerow(rows)

            # file.write(title + "\n")
            # file.write(content + "\n")
            # file.write(salary + "\n")
            # file.write("*" * 50 + "\n")
