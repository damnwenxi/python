from django.shortcuts import render,HttpResponse

# Create your views here.
import requests
import random
import uuid
import os
import json
import time
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

session = requests.Session()

'''
https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.6527849768458225&daid=5&pt_3rd_aid=0
https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.3875849716393387&daid=5&pt_3rd_aid=0

https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptqrtoken=296733310&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=2-0-1552318338056&js_ver=90305&js_type=1&login_sig=lTVL4m1JlC6FndWEON*t5sBYaqcNYmBhLTuKdUt7Q7UnjbKxfQRTY*qAJQl-YKD*&pt_uistyle=40&aid=549000912&daid=5&has_onekey=1&

ptqrtoken=1705605977

action=0-0-1552318947321

'''

def hash33(t):
    e = 0
    for i in range(len(t)):
        e += (e << 5) + ord(t[i])
    return 2147483647 & e



def login(request):
    # 请求QQ空间登录页面
    r1 = session.get('http://qzs.qq.com/')

    # 根据URL规则要生成随机数拼接在URL里面获取登录二维码
    ran = random.random()
    r2 = session.get('https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=%s&daid=5&pt_3rd_aid=0'%(ran))

    # 二维码token
    global qr_code
    qr_code = hash33(r2.cookies.get_dict()['qrsig'])

    # 生成唯一名称
    uuid_str = uuid.uuid4()
    url = str(uuid_str)+'.png'
    # 将图片写入到static中
    with open(os.path.join(BASE_DIR,'static/imgs/%s.png'%(uuid_str)),'wb') as f:
        f.write(r2.content)
        f.close()
    # 返回图片名称给前台
    return render(request,'login.html',{'img':url})

def is_login(request):

    args = {'code':0,'data':''}
    r3 = session.get(
        url="https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https://qzs.qzone.qq.com/qzone/v5/loginsucc.html?Fpara=Dizone&ptqrtoken=%s&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=2-0-%s&js_ver=90305&js_type=1&login_sig=lTVL4m1JlC6FndWEON*t5sBYaqcNYmBhLTuKdUt7Q7UnjbKxfQRTY*qAJQl-YKD*&pt_uistyle=40&aid=549000912&daid=5&has_onekey=1&"%(qr_code,time.time())
    )

    if '66' in r3.text:
        args['code'] = 66

    elif '67' in r3.text:
        args['code'] = 67

    # 点击确认登录，当前链接返回下一请求URL
    elif 'https://ptlogin2.qzone.qq.com/check_sig' in r3.text:
        url = re.findall(r"ptuiCB\('(.*)'\)", r3.text)

        url_list = url[0].split("','")
        # print(url_list[2])

        # 根据返回的链接请求，阻止重定向
        r4 = session.get(
            url=url_list[2],
            allow_redirects=False
        )
        # print(r4.cookies)


        # 拿到一切凭据， 搞定
        r5 = session.get(
            url='https://user.qzone.qq.com/%s'%('1396956549'),
            headers = {
                "user-agent": "Mozilla / 5.0 (Macintosh;IntelMac OS X 10_14_2) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.121 Safari / 537.36"
            }
        )

        # print(r5.headers)
        # print(r5.status_code)


        args['data'] = r5.text
        args['code'] = 200

    else:
        args['code'] = 404

    print(args)

    return HttpResponse(json.dumps(args))