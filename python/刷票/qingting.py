import requests
import random
import time
url = "https://proxy.horocn.com/api/proxies?order_id=NYBR1635646971720188&num=20&format=text&line_separator=win&can_repeat=yes"

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



header_vote = {
    "user-agent":random.choice(USER_AGENTS)
}


vote_url = "http://cdjcvote.lz.net.cn/home/index/vp/"

vote_id = 236

def go():
    res = requests.get(url=url).text
    ip_list = res.split('\r\n')

    for i in range(len(ip_list)):
        try:
            proxy = {
                'http': ip_list[i]
            }

            vote = requests.post(url=vote_url, timeout=1, data={'id': vote_id}, headers=header_vote, proxies=proxy).text
            print(vote)
            time.sleep(3)
                # print('可用ip:' + str(ip_list[i]))
        except:
            print("该ip不可用:" + str(ip_list[i]))

if __name__ == '__main__':
    while True:
        go()
        time.sleep(10)
