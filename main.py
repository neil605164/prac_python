# main.py
import json
from app.helper import (
    writeJsonFile, webCrawler
    )


# 主程式碼
def main():
    # url = "http://www.99kubo.tv/vod-read-id-26351.html"
    # url = "http://www.99kubo.tv/vod-read-id-140587.html"
    url = "http://www.99kubo.tv/vod-read-id-92197.html"

    # 開始爬蟲
    res = webCrawler(url)

    # 寫入json文件
    writeJsonFile(res)

# 程式碼起始點
main()