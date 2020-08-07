# 安裝 Python 2 的 requests 模組
import requests
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup


def Print():
    res = requests.get('https://ipeen-taiwan.tumblr.com/')
    if res.status_code == requests.codes.ok:
        soup = BeautifulSoup(res.content, 'html.parser')

       
        # 輸出排版後的 HTML 程式碼
        print(soup.prettify())
        print(soup.title.string)
        
        a_tags = soup.find_all('a')
        for tag in a_tags:
            # 輸出超連結的文字
            print(tag)
            # 輸出超連結網址
            print(tag.get('href'))



Print()