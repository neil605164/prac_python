from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display


display = Display(visible=0, size=(1, 1))  
display.start()

# 指定網址
url = "https://medium.com/dualcores-studio/make-an-android-custom-view-publish-and-open-source-99a3d86df228"

# 指定瀏覽器
browser = webdriver.Chrome(executable_path="./chromedriver_linux64/chromedriver")

# 開始取網頁內容
browser.get(url)

# 取的指定clas名稱資料
content_element = browser.find_element_by_class_name('ja')  # Find the search box

# 取的該 clas 底下的 HTML
content_html = content_element.get_attribute("innerHTML")


# 整理 HTML 代碼
soup = BeautifulSoup(content_html, "html.parser")
p_tags = soup.find_all("h3")
for p in p_tags:
    print(p.string)


# 關閉瀏覽器
browser.quit()