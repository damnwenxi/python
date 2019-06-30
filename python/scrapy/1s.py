import requests
from bs4 import BeautifulSoup

response = requests.get(
    url='https://dig.chouti.com/',
    headers={
        'Referer':'https://dig.chouti.com/',
        'cookie':'gpsd=49d30e4494a9dc34f0ee61a95477a588; JSESSIONID=aaa09fgqHVKfAgzbQhPKw; gpid=e68ca6afcc804c278bf321705f1dee9c; gdxidpyhxdE=fDR02dUfTBg8DgCYMgEAtu9nIf4AZyZQqopSVExoi5SeiK5SjAK9o58IPK7oD3XI1xVEnKpfTW8taR0hq4umXs6Jidgf8gHkrUr0LPjLMXgCLgic0%5C%2Bg%2FJ%2Bb1c2CM0USsjSJu8ffEvmvPKYlWhYGyH%2BJ6s%5CITMbAbLgQSx0DYkqEP6dQ%3A1552141119813; _9755xjdesxxd_=32; YD00000980905869%3AWM_NI=RKZ60Dv9fB1SAMIhB4YfNdDebUR7g2pvH9EfHlGhIp5OXgAbnQhb483X9urRFlO0Zfls0Rwhi%2FMXP2jjTAgAKECfjyHM77mBt4kbPVDSpbUnaU7TJyoxZcanFVhLhYR9V1k%3D; YD00000980905869%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee97c14bb8b597aef021a8eb8fb3d14b828a9e85bb61aab98294d64ea395ae9bae2af0fea7c3b92a929596d7b350b6e7aaa3b45983938789c1409bba8285c76fa28b9ed8e63ab4aa88dac86e8cb48989cc7cf7919888c46aae8fa883b734f188f796f15a86b481d1d96eb0ad00b3f664abf183b9d33aaab69ca2e64b899b8d87e9738c93f9d8f04ab8eca583d35e888dc083d866a38bf9b5c973ada89684e466868aa8adeb5392e79ad2ea37e2a3; YD00000980905869%3AWM_TID=OLHMBMw%2FOOBEBBEREVdsh30Y9GUaOKy%2F',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'upgrade-insecure-requests': '1'
    }
)
response.encoding = response.apparent_encoding

soup = BeautifulSoup(response.text,features='html.parser')
content = soup.find(id='content-list').find_all('a')

for a in content:
    print(a.text.strip())
# print(response.text)