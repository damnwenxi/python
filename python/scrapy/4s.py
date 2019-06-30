import requests
from bs4 import BeautifulSoup

session = requests.Session()


print("------")
r1 = session.get('https://github.com/login')
print(r1.headers)
soup = BeautifulSoup(r1.text,features='html.parser')

target = soup.find('form').find('input',attrs={"name":"authenticity_token"})['value']
print(target)
# print(r1.text)


r2 = session.post(
    url='https://github.com/session',
    headers={
        # 'Cookie':'_ga=GA1.2.1290552237.1547987643; _octo=GH1.1.195581237.1547987646; tz=Asia%2FShanghai; has_recent_activity=1; logged_in=no; _gat=1; _gh_sess=Q0FtWDdnR0N6ODNWcEdFSXZpSHFtZlJRQnM5QWtDblRkY3FXakhCbktuL29kTy9QdzRmNXdKeDFrdXp2WlVTRGJTak5NRk85TFpHNzdpWWZ1MWM0cU5pempjWWdKSCtDejNNZk9LWi92eTJyMW0zaE5XSTIyZUl3dnpPOE1WK2x2dTdnazhwV1FXVWtCeFBudHZtK1IwRUUvcFIxSXlNSTRUSjN1NmhXTE1UcktNMGh6YW9ZdGk0Z0p0aWp2RFUwbkJuMWFZSHVRMlZCVlZhYXNqMDBUYUp3VWpFWnVIZVphaTRNSXJLMk1HZHh5b0xYanY1WDIrOXp3OExiclljRGY5NHZrd1NZblBWSW9vVTk3UURXbGMyekQ4bkd0OHhvbXZ5dDJ4SzJFNHdtUkYvbDYyVHlVUXl4bWQyUi9oN29MTG1YTTZxV3lUODlwa3dvTFlEbThBclBGNzlCTG9pZ1FCY3hKVlNDYitxcVIvUnJvL01SWExOaFRsVlFxNk9hMUxoNGFVVlloUGFNMDR6MjdIT004WC9tYWh4SGcwZ1VmNE0wbEZISHdXQjMvTVE4b1lGdWFkcmZmSWxYdFVpbjIxaU9EWkxtUStBVDZKUTgxMlp6Tnc9PS0tSjdhcG5yeGpIaVc5UXYwcGhZNnFnQT09--dd80206c3eabf87994c79384ac2bbef9707f6ff2',
        'Referer': 'https://github.com/login',
        'Host': 'github.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',

    },
    data={
        'commit': 'Sign in',
        'utf8': '✓',
        'authenticity_token': target,
        'login': '1396956549@qq.com',
        'password': '4786195161.com'
    }
)
print(r2.headers)