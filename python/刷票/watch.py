from bs4 import BeautifulSoup
import requests
from datetime import datetime
import random
import time
import pymysql


# cur.execute("SELECT * FROM news limit 30")


url = "http://cdjcvote.lz.net.cn/?sort=top"

headers = {
    "referer":'http://cdjcvote.lz.net.cn',
    "user-agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
}

def getList():
    # 打开数据库
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd="root", db='watch',charset='utf8')
    cur = conn.cursor()

    res = requests.get(url,headers).text
    soup = BeautifulSoup(res)
    ips = soup.find_all(attrs={"class":"col-md-4 listpro"})
    finddate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for item in ips:
        infos = item.find(attrs={"class":"col-md-8"}).find('a').text.split('\t')
        title = infos[2]
        school = infos[0]
        team = infos[1]
        urls = str(item.find(attrs={"class": "col-md-8"}).find('a')['href'])
        number = item.find(attrs={"class":"number"}).text
        vote = item.find('b').text
        # print(infos,number,vote,urls,finddate)
        # sql语句
        sql = "insert into team (title, school, team, url, vote, number_id, f_date) values ('%s','%s','%s','%s','%s','%s','%s')" %(title,school,team,urls,vote,number,finddate)
        # sql = "insert into team (title, school, team, url, vote, number_id, f_date) values (%s,%s,%s,%s,%s,%s,%s)"
        # sql = "select * from team"
        cur.execute(sql)
        # cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        # try:
        #     # 执行sql语句
        #     cur.execute(sql)
        #     # 提交到数据库执行
        #     conn.commit()
        # except:
        #     # Rollback in case there is any error
        #     conn.rollback()

    cur.close()
    conn.close()

if __name__ == '__main__':
    getList()
