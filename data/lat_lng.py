# house table 存入經緯度數值

import os
from dotenv import load_dotenv
import requests
import json
import pymysql

load_dotenv()
os.environ

db_settings = {
    "host": os.environ["db_host"],    #主機
    "port": 3306,           #埠號    
    "user": os.environ["db_user"],         #使用者名稱
    "password": os.environ["db_password"], #使用者帳號
}

def db_connect():
    try:
        # 建立Connection物件
        connect = pymysql.connect(**db_settings)
        print("connect db_settings")
        return connect

    except Exception as ex:
        print(ex)
        return "資料庫連線失敗"

# 連線DB
cnnt=db_connect()
cursor=cnnt.cursor()
cursor.execute("use FMH")
cursor.execute("select houseid, all_addr from house")
filterData=cursor.fetchall()

if filterData:
    for item in filterData:
        houseid=item[0]
        all_addr=item[1]
        print("houseid", houseid)
        print("all_addr", all_addr)

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + all_addr+"&key=AIzaSyDoRK3B7f6M30jo_sZa1yOb4UcDBlAQhKQ"
        print(url)

        response = requests.request("GET", url)
        result=response.json()

        lat=result["results"][0]["geometry"]["location"]["lat"]
        # print("lat", lat)
        lng=result["results"][0]["geometry"]["location"]["lng"]
        # print("lng", lng)
        statement=f"update house set lat={lat}, lng={lng} WHERE houseid='"+houseid+"'";	
        # print("statement", statement)
        cursor.execute(statement)
        cnnt.commit()  

