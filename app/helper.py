import requests
from bs4 import BeautifulSoup
import os
import json
import re

#  寫 json 檔案
def writeJsonFile(data):
    dirPath = "./json/"
    fileName = "video.json"

    # 檢查路徑是否存在
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)

    # 檢查檔案是否存在，不存在就寫檔案
    if not os.path.isfile(dirPath+fileName):
        file = open(dirPath+fileName, "w+", encoding='utf8')
        json.dump(data,file, ensure_ascii=False)

# 爬取網頁 HTML
def webCrawler(url):
    # 使用 GET 方式下載普通網頁
    res = requests.get(url)

    # 檢查是否爬網頁資訊成功
    if res.status_code == requests.codes.ok:
        # 以 Beautiful Soup 解析 HTML 程式碼
        allHTML = BeautifulSoup(res.content, 'html.parser')

         # 輸出排版後的 HTML 程式碼
        vpls = allHTML.find_all("div", class_="vpl")
        ul = allHTML.find("ul", class_="tabs")
        lis = ul.find_all("li")

        

        # 整理資料
        lists = []
        res = []
        for k,v in enumerate(vpls):
            b = lis[k].find("b")
            em = lis[k].find("em")
            

            data = {
                "type": b.string,
                "total": int(em.string),
                "detail": ""
            }
            urls = v.find_all("a")

            # 名稱沒包含 FLY 不理會
            if "FLV" not in data["type"]:
                continue


            # 取該類型的所有影片連結
            lists = []
            for url in urls:
                txt = {
                    "name":url.string, 
                    # "href":""
                    "href": "http://www.99kubo.tv" + url.get('href')
                }

                # 取 m3u8 連結網址
                # videoUrl = "http://www.99kubo.tv" + url.get('href')
                # videoRes = requests.get(videoUrl)

                # print(videoUrl)
                # # 檢查是否爬網頁資訊成功
                # if videoRes.status_code == requests.codes.ok:
                #     # 以 Beautiful Soup 解析 HTML 程式碼
                #     videoHTML = BeautifulSoup(videoRes.content, 'html.parser')
                #     m3u8UrlHtml = videoHTML.find("div", class_="play")
                #     m3u8UrlScript = m3u8UrlHtml.find('script')

                #     pattern = re.compile(r'(http.+index.m3u8)\\\"\]')
                #     jsonData = pattern.findall(m3u8UrlScript.string)

                #     txt["href"] = jsonData


                # 塞入陣列清單
                lists.append(txt)

            data["detail"] = lists
            res.append(data)
    
    return res
