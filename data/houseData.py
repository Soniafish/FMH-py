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
# houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit
# cursor.execute("create table house(houseid VARCHAR(255) PRIMARY KEY, area_misc VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, photo_src VARCHAR(255) NOT NULL, layout_misc VARCHAR(255) NOT NULL, house_price VARCHAR(255) NOT NULL, house_price_unit VARCHAR(255) NOT NULL, area_price VARCHAR(255) NOT NULL, country VARCHAR(255) NOT NULL, community VARCHAR(255), kindStr VARCHAR(255) NOT NULL, layout VARCHAR(255) NOT NULL, management_fee VARCHAR(255), management_fee_unit VARCHAR(255), house_size FLOAT NOT NULL, house_size_unit VARCHAR(255) NOT NULL)")

data=None
with open("data3-4.json", mode="r") as file:
    data=json.load(file)
    data=data["data"]

valList=[]
for item in data:
    houseid=item["houseid"] #房屋編號
    area_misc=item["area"] #房屋簡述
    address=item["address"] #地址(含社區)
    title=item["title"] #標題
    photo_src=item["photo_src"] #圖片
    layout_misc=item["layout_str"]  #總格局
    house_price=item["price_arr"]["price"]  #總金額-數字
    house_price=house_price.replace(",", "")
    house_price=int(house_price)
    house_price_unit=item["price_arr"]["unit"] #總金額-單位
    area_price=item["area_price"] #單價
    country=item["section"] #鄉鎮市區
    community=item["community_addr"] #社區
    kindStr=item["kindStr"] #房屋類型
    layout=item["layoutStr"] #格局
    management_fee=item["priceUnit"]["price"] #管理費-數字
    management_fee_unit=item["priceUnit"]["unit"] #管理費-單位
    house_size=item["areaUnit"]["area"] #總坪數-數字
    house_size_unit=item["areaUnit"]["unit"] #總坪數-單位

    val = (houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit)
    valList.append(val)
    # print(val)
    
sql = "INSERT INTO house (houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(sql, valList)
    
cnnt.commit()    

# string="1,450"
# string=string.replace(",", "")
# number=int(string)
# print(number)
# print(type(number))