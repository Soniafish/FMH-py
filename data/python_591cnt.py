# 591手機版商品內頁api (https://m.591.com.tw/api.php?module=iphone&action=house.....) 可取得該頁的json資料
# 透過此方法取得20筆內頁資料, 存為data-cnt1-1-x.json

import os
from dotenv import load_dotenv
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

# 建立Cursor物件
cursor=cnnt.cursor()

# cursor.execute("create database FMH")
cursor.execute("use FMH")
# photos, age, floor, direction, im_name, company_name, statusquo, shape, fitment, managefee, isrent_ing, parking, area_main, area_sub, area_land, remark,
# cursor.execute("alter table house add (photos TEXT NOT NULL, age VARCHAR(255) NOT NULL, floor VARCHAR(255) NOT NULL, direction VARCHAR(255) NOT NULL, im_name VARCHAR(255), company_name VARCHAR(255), statusquo VARCHAR(255) NOT NULL, shape VARCHAR(255) NOT NULL, fitment VARCHAR(255) NOT NULL, managefee VARCHAR(255) NOT NULL, isrent_ing VARCHAR(255) NOT NULL, parking VARCHAR(255) NOT NULL, area_main VARCHAR(255) NOT NULL, area_sub VARCHAR(255) NOT NULL, area_land VARCHAR(255) NOT NULL, remark VARCHAR(255))")


# 取得所有db的houseid
cursor.execute("select houseid from house order by houseid asc")
filterData=cursor.fetchall()
# print(filterData) 
idData=[]
for item in filterData:
    idData.append(item[0])
# print(idData) 
# print(len(idData)) #627, 31, 62, 93, 124, 156, 187, 218, 249, 280, 311, 342, 373, 404, 435, 466, 497, 528, 559, 590, 627, 

# 指定houseid為哪個區間, 來存入cnt的資料
for idx in range(591, 627):
    houseid = idData[idx]
    
    # 開啟"data-cnt1-1-x.json"檔案, 將資料存入table house對應的欄位
    data=None
    with open("data-cnt1-1-19.json", mode="r") as file:
        data=json.load(file)
        # print(data)

        photos=data["data"]["photo"] #照片集
        age=data["data"]["age"] #屋齡
        floor=data["data"]["floor"] #樓層

        direction=data["data"]["direction"] if "direction" in data["data"] else ""  #朝向
        
        im_name=data["data"]["im_name"] #仲介
        company_name=data["data"]["company_name"] if "company_name" in data["data"] else ""#仲介公司
        # company_name=data["data"]["company_name"]  #仲介公司
        statusquo=data["data"]["info"][1]["value"]  #現況
        shape=data["data"]["shape"] #型態
        fitment=data["data"]["fitment"] #裝潢
        managefee=data["data"]["managefee"] #管理費
        isrent_ing=data["data"]["isrent_ing"] #帶租約
        parking=data["data"]["parking"] #車位
        area_main=data["data"]["area_intro_arr"][2]["value"] #主建物
        area_sub=data["data"]["area_intro_arr"][4]["value"] #附屬建物
        area_land=data["data"]["area_intro_arr"][0]["value"] #土地坪數
        remark=data["data"]["remark"] #房屋描述

    # houseid="S9557247"
    sql = "update house set photos='"+photos+"', age='"+age+"', floor='"+floor+"', direction='"+direction+"', im_name='"+im_name+"', company_name='"+company_name+"', statusquo='"+statusquo+"', shape='"+shape+"', fitment='"+fitment+"', managefee='"+managefee+"', isrent_ing='"+isrent_ing+"', parking='"+parking+"', area_main='"+area_main+"', area_sub='"+area_sub+"', area_land='"+area_land+"', remark='"+remark+"' where houseid='"+houseid+"'"
    # print(sql)
    cursor.execute(sql)
    cnnt.commit()  
