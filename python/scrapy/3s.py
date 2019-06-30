import requests

print("----")
# session = requests.Session()

r1 = requests.get(
    url='https://dig.chouti.com/',
    headers={
        'Referer':'https://dig.chouti.com/',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'upgrade-insecure-requests': '1'
    }
)

print(r1.cookies.get_dict())

r2 = requests.post(
    url='https://dig.chouti.com/login',

    headers={
        'origin': 'https://dig.chouti.com',
        'referer': 'https://dig.chouti.com/',
        'cookie':str(r1.cookies.get_dict()),
        'X-Requested-With': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    },
    data={
        'phone':'8617362752315',
        'password':'4786195161.com',
        'oneMonth':''
    }
)

print(r2.text)
vote_cookies = r2.cookies.get_dict()
print(vote_cookies)


r3 = requests.post(
    url='https://dig.chouti.com/link/vote?linksId=25083401',

    headers={
        'cookie':str(vote_cookies),
        'origin': 'https://dig.chouti.com',
        'referer': 'https://dig.chouti.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
)
print("------")
print(r3.text)



