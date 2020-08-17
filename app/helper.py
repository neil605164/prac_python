import requests
from bs4 import BeautifulSoup
import os
import json
import re
import errno
import numpy as np

# 檢查資料夾是否存在
def checkDirExist(dirPath):
    # 使用 try 建立目錄
    try:
        os.makedirs(dirPath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# 讀檔案
def readFile(filePath):

    content = None
    # 使用 try 開啟
    try:
        f = open(filePath, 'r')
        content = f.read()
        f.close()
    # 檔案不存在的例外處理
    except FileNotFoundError:
        f = open(filePath, 'w+')
        f.close()
    # 路徑為目錄的例外處理
    except IsADirectoryError:
        print("該路徑為目錄")

    return content
   
    
#  寫 json 檔案
def writeJsonFile(data):
    dirPath = "./json/"
    fileName = "video.json"

    # 檢查資料夾是否存在
    checkDirExist(dirPath)

    # 檢查檔案是否在
    content = readFile(dirPath+fileName)

    # 整理檔案內容，準備進行比對
    if content != "":
        urlsName = []
        totalList = []
        jsonContent = json.loads(content)
        for value in jsonContent:
            totalList.append(value["total"])
            for url in value["detail"]:
                urlsName.append(url["name"])
    
        # 挑出要比對的位置，「只有最多集的類型需要比對」
        position = np.argmax(totalList)
        
        # 檢查沒有在檔案內的在新增
        tmp = data[position]
        for url in tmp["detail"]:
            if url["name"] not in urlsName:
                print("最新新增影片有:\n" + str(url))
        
    

    file = open(dirPath+fileName, "w+", encoding='utf8')
    json.dump(data,file, ensure_ascii=False)
    file.close()

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
        videoName = allHTML.find("meta", itemprop="name").get("content")
        lis = ul.find_all("li")

        # 整理資料
        lists = []
        res = []
        for k,v in enumerate(vpls):
            b = lis[k].find("b")
            em = lis[k].find("em")
            

            data = {
                "name": videoName,
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
                    "href": "http://www.99kubo.tv" + url.get('href')
                    # "href":""
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
