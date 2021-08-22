# BeautifulSoup 爬蟲 取得 house data
# 手機版分類頁api (https://m.591.com.tw/mobile-list.html?.....) 可取得該頁的json資料
# 透過此方法取得台北市每一區依照1000萬以下、1000-1500萬、1500-2000萬、2000-2500萬區間, 取得7Ｘ4筆的分類頁資料, 存為datax-x.json
# 在使用 BeautifulSoup 爬文 id 下的頁面資料


import requests
from bs4 import BeautifulSoup
import time
import json

import os
from dotenv import load_dotenv
import pymysql


def scrap(houseid):
    #  爬蟲
    url = "https://sale.591.com.tw/home/house/detail/2/"+houseid+".html"
    print(url)

    payload={}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'cookie': 'DETAIL[2][9618863]=1; is_new_index=1; is_new_index_redirect=1; T591_TOKEN=cr0vfgqkgbqcf6oekkn2j7f3l5; _ga=GA1.3.1000318816.1599926792; tw591__privacy_agree=0; _ga=GA1.4.1000318816.1599926792; webp=1; PHPSESSID=thuh006kdrbfkee536eaq8lt27; bid[pc][1.34.239.123]=3228; urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82; _gid=GA1.3.1945758433.1626794026; _gid=GA1.4.1945758433.1626794026; XSRF-TOKEN=eyJpdiI6IkQ5eGpcLzJOU0RvTzgrR1daVk9IeW53PT0iLCJ2YWx1ZSI6IkwyUndCaXdXTHJjTGtnTUpUaFBiWXdJdkY2UWo4UWNvNlBUYzZNNDQyMGc3TWoxa0VlSVdvelRKNXlZYkkrZTlOYzl0VHAyS3NEVWI5MTVQQlNRUnFRPT0iLCJtYWMiOiJlMzg1NDQzZTc5ODFkNDkzNWI1N2I2NTUxY2M5ZmYwZmI5NWQ0NDYxMjhlZDUzZDFlZDY0OWQ3Y2NiMGI4OWVhIn0%3D; _fbp=fb.2.1626794027494.1742080001; user_index_role=2; user_browse_recent=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A2%3Bs%3A7%3A%22post_id%22%3Bi%3A9618863%3B%7D%7D; 591_new_session=eyJpdiI6Inl0NWtsSkFEOUVNcGxuaUJmbUt1MWc9PSIsInZhbHVlIjoiMnE3dzBEUUxTWWdjZ3lhSUQzZU1wV09OaHdWMFJsZzM1ZU0zQXh0b3BNMWxpS2dueWgrZEF1dkhTY25rM2RcL3FZclYyXC9CSnlJNm80QWRpaFNqcVR5QT09IiwibWFjIjoiOWFmM2Y4YTY1NzdmMjBmYTc5OTJjNWVlY2Y0ZWVlNGZiOGZlMWQ5NDZmYmE4OGQ4N2UzMzI4M2VmNTNkMzY3NCJ9; 591_new_session=eyJpdiI6IlwvVUVaaDVYbmF1Rk5oWXY0RzhKTmd3PT0iLCJ2YWx1ZSI6ImNTZWFDVFJTSGVXQkp1QVNCakdcL3lHVTBSZXFqSzM5eU43cFhKUExNV0c4UU1KTm56ZDFwNTg0ek45eXZYdWhNd1RmajlRZFY4emR5cFRibVRQTWpRZz09IiwibWFjIjoiOWI4N2NiMjQ4NjA1NjNlMDFlN2RkOTUwOGRkN2IyYzVlNGU5MzMzNzNmYTU1YzNkYTE5MGE4MmM5MjI2ZjQzMCJ9; user_index_role=2; user_browse_recent=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A2%3Bs%3A7%3A%22post_id%22%3Bi%3A9618863%3B%7D%7D',
        'referer': 'https://sale.591.com.tw/',
        'mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Host': 'sale.591.com.tw'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    sp = BeautifulSoup(response.text, 'html.parser')
    

    layout_misc=sp.find_all("div", "info-floor-key")[0].text
    print("layout_misc:", layout_misc)

    age=sp.find_all("div", "info-floor-key")[1].text
    print("age:", age)


    direction=""
    community=""

    for idx in range(len(sp.find_all("span", "info-addr-key"))):
        key_name=sp.find_all("span", "info-addr-key")[idx].text
        val_str=sp.find_all("span", "info-addr-value")[idx].text
        if key_name == "樓層":
            floor=val_str
        elif key_name == "朝向":
            direction=val_str
        elif key_name == "社區":
            community=val_str
        elif key_name == "地址":
            address=val_str

    print("floor:", floor)
    print("direction:", direction)
    print("community:", community)
    print("address:", address)

    im_name=sp.find("span", "info-span-name").text
    print("im_name:", im_name)

    company_name=sp.find("span", "info-span-msg").text
    print("company_name:", company_name)

    statusquo=""
    shape=""
    fitment=""
    isrent_ing=""
    parking=""
    area_main=""
    area_sub=""
    area_land=""
    for idx in range(len(sp.find_all("div", "detail-house-key"))):
        key_name=sp.find_all("div", "detail-house-key")[idx].text
        val_str=sp.find_all("div", "detail-house-value")[idx].text
        print("key_name:", key_name)
        print("val_str:", val_str)
        if "現" in key_name: #現況
            # print("has 現況")
            statusquo=val_str
        elif "態" in key_name: #型態
            # print("has 型態")
            shape=val_str
        elif "潢" in key_name: #裝潢程度
            # print("has 裝潢程度")
            fitment=val_str
        elif "租" in key_name: #帶租約
            # print("has 帶租約")
            isrent_ing=val_str
        elif "車" in key_name: #車位
            # print("has 車位")
            parking=val_str
        elif "主" in key_name: #主建物
            # print("has 主建物")
            area_main=val_str
        elif "附" in key_name: #附屬建物
            # print("has 附屬建物")
            area_sub=val_str
        elif "土" in key_name: #土地坪數
            # print("has 土地坪數")
            area_land=val_str
        
    print("statusquo:", statusquo)
    print("shape:", shape)
    print("fitment:", fitment)
    print("isrent_ing:", isrent_ing)
    print("parking:", parking)
    print("area_main:", area_main)
    print("area_sub:", area_sub)
    print("area_land:", area_land)

    # db無此欄位：生活機能
    house_life=[]
    for item in sp.find_all("div", "detail-house-life"):
        house_life.append(item.text)
        # print(item.text)
    print("house_life", house_life)

    # 圖檔是縮小版
    photos=[]
    photos_tage=sp.select("#img_list li img")
    for item in photos_tage:
        item=item['src']
        if("591.com" in item):
            photos.append(item)
    print("photos:", photos)

    remark=sp.select("#detail-feature-text")
    remark=str(remark[0])
    print("remark:", remark)

    scrap_data={
        "address": address,
        "layout_misc": layout_misc,
        "community": community,
        "photos": photos,
        "age": age,
        "floor": floor,
        "direction": direction,
        "im_name": im_name,
        "company_name": company_name,
        "statusquo": statusquo,
        "shape": shape,
        "fitment": fitment,
        "isrent_ing": isrent_ing,
        "parking": parking,
        "area_main": area_main,
        "area_sub": area_sub,
        "area_land": area_land,
        "remark": remark,
        "house_life": house_life
    }
    print("-------------------------------------------------------------")
    return scrap_data


def parse_file (file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:     #讀取JSON檔案
        data=json.load(file)

        for obj in data["data"]:
            houseid = obj["houseid"]
            print(houseid)

            houseid=houseid.split("S")[1]
            scrap_data=scrap(houseid)

            obj["all_addr"]=scrap_data["address"]
            obj["all_layout"]=scrap_data["layout_misc"]
            obj["community"]=scrap_data["community"]
            obj["photos"]=scrap_data["photos"]
            obj["age"]=scrap_data["age"]
            obj["floor"]=scrap_data["floor"]
            obj["direction"]=scrap_data["direction"]
            obj["im_name"]=scrap_data["im_name"]
            obj["company_name"]=scrap_data["company_name"]
            obj["statusquo"]=scrap_data["statusquo"]
            obj["shape"]=scrap_data["shape"]
            obj["fitment"]=scrap_data["fitment"]
            obj["isrent_ing"]=scrap_data["isrent_ing"]
            obj["parking"]=scrap_data["parking"]
            obj["area_main"]=scrap_data["area_main"]
            obj["area_sub"]=scrap_data["area_sub"]
            obj["area_land"]=scrap_data["area_land"]
            obj["remark"]=scrap_data["remark"]
            obj["house_life"]=scrap_data["house_life"]
            
            time.sleep( 1 )

        newdata=data
        
    with open(file_name, mode="w", encoding="utf-8") as file:     #複寫JSON檔案
        json.dump(newdata, file, ensure_ascii=False)


for x in range(1, 13):
    for y in range(1, 5):
        file_name="data"+str(x)+"-"+str(y)+".json"
        print(file_name)
        parse_file(file_name)
        



# houseid="S9504547".split("S")[1]
# print(houseid)
# scrap_data=scrap(houseid)

