import requests

print("----")
session = requests.Session()

r1 = session.get(
    url='https://dig.chouti.com/',
    headers={
        'Referer':'https://dig.chouti.com/',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'upgrade-insecure-requests': '1'
    }
)

r2 = session.post(
    url='https://dig.chouti.com/login',

    headers={
        'origin': 'https://dig.chouti.com',
        'referer': 'https://dig.chouti.com/',
        # 'cookie':cookie_code,
        'X-Requested-With': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    },
    data={
        'phone':'8617362752315',
        'password':'4786195161.com',
        'oneMonth':1
    }
)

print(r2.text)
vote_cookies = r2.cookies.get_dict()
print(vote_cookies)


r3 = session.post(
    url='https://dig.chouti.com/link/vote?linksId=25083401',

    headers={
        'origin': 'https://dig.chouti.com',
        'referer': 'https://dig.chouti.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
)
print("------")
print(r3.text)



