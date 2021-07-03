# !/usr/bin/python2
# coding:utf-8

# Python 網路爬蟲 Web Crawler 教學 - AJAX / XHR 網站技術分析實務

# 以"https://medium.com/"為例, 登入後開啟開發人員模式, 選擇"Network"的"XHR", 重新載入後可觀察到多隻api
# 點選api的preview可以看到api傳送的內容物, 如果是json將可以json展開閱讀

#抓取medium.com的文章
import urllib.request as req
import ssl      #mac才要加
ssl._create_default_https_context = ssl._create_unverified_context  #mac才要加
from bs4 import BeautifulSoup

url="https://m.591.com.tw/mobile-list.html?type=sale&dropDown=1&version=2017&firstRow=0&regionid=1&region_id=1&device=touch&_appid=nqqpaGbhpu"
# url="https://m.591.com.tw/mobile-list.html?type=sale&dropDown=1&version=2017&firstRow=0&regionid=1&region_id=1&device=touch&_signature=MDE5N2VkY2MzNTliMzgxODMxOWI2ZGEzZDRiMjkzN2M%3D&_timestamp=1624787776&_randomstr=CTkcztkw&_appid=nqqpaGbhpu"
# url="https://m.591.com.tw/mobile-list.html?type=sale&dropDown=1&version=2017&firstRow=24&regionid=1&region_id=1&device=touch&_signature=MzA0OWU5YzBjZTk5ZTBmZmJhZjNlNmJlYjYzNDRjMDM%3D&_timestamp=1624787778&_randomstr=rGM8jRWR&_appid=nqqpaGbhpu"
# 建立一個Request物件, 附加一個Request Headers的資訊
request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"
})

with req.urlopen(request) as response:
    data=response.read().decode("utf-8")  #根據觀察, 取得的資料是JSON格式

# 解析 JSON 格式的資料, 取得每篇文章的標題
import json
# data=data.replace('])}while(1);</x>', '')   
data=json.loads(data)   #把原始的 JSON資料解析成字典/列表的表示形式
posts=data["status"]
print(data)
# 取得 JSON 資料中的文章標題
# for key in posts:
#     print(posts[key]["houseid"], posts[key]["area"])