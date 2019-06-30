from bs4 import BeautifulSoup
import requests
import random
import time
url = "https://www.xicidaili.com/wt/"

USER_AGENTS = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"]

headers = {
    "cookie":'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTg4NDQwMDk3YjgyMTFjMjYyNmUxOTk2MTUwMmE0ZmEwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMU80dmZobUcyaXpBNitYQzZSM2MyVmhVY2JVWFJHK2Vsem03d291Uk1JaTg9BjsARg%3D%3D--88f297870c32556fb90c431ee0a7b8b7d1e61f0a; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1559368218; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1559368247',
    "referer":'https://www.xicidaili.com/api',
    "user-agent":random.choice(USER_AGENTS),
    "accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
}

# 投票请求头
header_vote = {
    "user-agent":random.choice(USER_AGENTS),
    "origin":'http://cdjcvote.lz.net.cn'
}
# 投票地址
vote_url = "http://cdjcvote.lz.net.cn/home/index/vp/"

# 投票id
vote_id = 236

# 1000次爬取ip代理网站数据
for i in range(1,100):
    print(url+str(i))
    res = requests.get(url=url+str(i),headers=headers).text
    soup = BeautifulSoup(res)
    # IP表的每一行
    ips = soup.find(id='ip_list').find_all('tr')
    ip_list = []

    # 遍历每一行的td，拿到ip和端口号
    for item in ips:
        tds = item.find_all('td')
        if len(tds) > 3:
            ip_list.append(tds[1].text+':'+tds[2].text)

    # 打开文件存储可用ip
    f = open('ip2.txt','a+')
    # 遍历每一次的ip_list
    for i in range(len(ip_list)):
        try:
            proxy = {
                'http':ip_list[i]
            }
            vote = requests.post(url=vote_url, timeout=1, headers=header_vote, proxies=proxy).text
            print(vote)
            if vote['status']:
                print('可用代理：' + str(ip_list[i]))
                f.write(ip_list[i]+'\n')
                time.sleep(3)
        except:
            print('无效代理：'+ str(ip_list[i]))
    f.close()
