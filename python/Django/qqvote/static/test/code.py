import re

url1 = "ptuiCB('0','0','https://ptlogin2.qzone.qq.com/check_sig?pttype=1&uin=1396956549&service=ptqrlogin&nodirect=0&ptsigx=cf0e3e90e62a345107bb8cef89bab511e4a537583a5a2e3605445c1154533ed7cbf364fd3b30c5f3b7aa2cb8127aaaf1647cfd303ff62cbc9d53171d94e36776&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3FFpara%3DDizone&f_url=&ptlang=2052&ptredirect=100&aid=549000912&daid=5&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0','0','登录成功！', '低端人口')"


url = re.findall(r"ptuiCB\('(.*)'\)",url1)
print(url[0].split("','"))

url_list = url[0].split("','")

for i in url_list:
    print(i)
