# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 11:13
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : spider_dangdang.py
# @Software: PyCharm
import requests
from lxml import html
import urllib
book_list = []
def spider(isbn):
    """根据isbn爬取当当网图书信息 书名，价格，
    店铺，购买链接，然后进行价格排序
    """
    url = 'http://search.dangdang.com/?key={}&act=input'.format(urllib.parse.quote(isbn))

    print(url)
    # 使用requests进行http请求然后获取网页的源代码
    resp = requests.get(url)
    # print(resp.status_code)
    # print(resp)
    html_data = resp.text
    # print(html_data)

    # 使用xpath提取图书的信息
    selector = html.fromstring(html_data)
    ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
    #print(ul_list)
    #print('您好，售卖该书的店铺共有:',len(ul_list),'家')
    for li in ul_list:
        # 书名
        title = li.xpath('a/@title')[0]
        # print(title)

        # 购买链接
        link = li.xpath('a/@href')[0]
        # print(link)

        # 价格

        price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
        if(len(price)):
            price = price[0].replace('¥', '')
        # print(price)
        # 店铺
        store = li.xpath('p[@class="search_shangjia"]/a[1]/text()')
        # if len(store) == 0:
        #     store = '当当自营'
        # else:
        #     store = store[0]
        store = '当当自营' if len(store) == 0 else store[0]

        # print(store)
        # 存储形式[{},{},{}]
        book_list.append({
            "title": title,
            "link": link,
            "price": price,
            "store": store
        })

    # 按照价格进行排序 [{},{}]
    book_list.sort(key=lambda x : float(x['price']))

    for book in book_list:
        print(book)

    import pandas as pd
    df = pd.DataFrame(book_list)
    df.to_csv('book.csv')

    # 切片
    # for i in book_list[:10]
    # x ，y 轴
    #price_x = [float(i['price']) for i in book_list[:10]]
   # print(price_x)
   # store_y = [i['store'] for i in book_list[:10]]
   # print(store_y)

    # 绘制
    #from matplotlib import pyplot as plt
    #plt.rcParams["font.sans-serif"] = ['SimHei']
    #plt.rcParams['axes.unicode_minus'] = False
    #plt.barh(store_y,price_x )
    #plt.show()



isbn  = input('请输入图书的书号')
spider(isbn)
