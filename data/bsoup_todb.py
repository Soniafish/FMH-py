# house table 建置

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
cursor=cnnt.cursor()
# cursor.execute("create database FMH")
cursor.execute("use FMH")
# houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, community_addr, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit, lat, lng
# photos, age, floor, direction, im_name, company_name, statusquo, shape, fitment, isrent_ing, parking, area_main, area_sub, area_land, remark, all_addr, all_layout, house_life
cursor.execute("create table house(houseid VARCHAR(255) PRIMARY KEY, area_misc VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, photo_src VARCHAR(255) NOT NULL, layout_misc VARCHAR(255) NOT NULL, house_price int NOT NULL, house_price_unit VARCHAR(255) NOT NULL, area_price VARCHAR(255) NOT NULL, country VARCHAR(255) NOT NULL, community VARCHAR(255), community_addr VARCHAR(255), kindStr VARCHAR(255) NOT NULL, layout VARCHAR(255) NOT NULL, management_fee VARCHAR(255), management_fee_unit VARCHAR(255), house_size FLOAT NOT NULL, house_size_unit VARCHAR(255) NOT NULL, lat FLOAT, lng FLOAT, photos TEXT NOT NULL, age VARCHAR(255), floor VARCHAR(255), direction VARCHAR(255), im_name VARCHAR(255), company_name VARCHAR(255), statusquo VARCHAR(255), shape VARCHAR(255), fitment VARCHAR(255), isrent_ing VARCHAR(255), parking VARCHAR(255), area_main VARCHAR(255), area_sub VARCHAR(255), area_land VARCHAR(255), remark TEXT, all_addr VARCHAR(255), all_layout VARCHAR(255), house_life VARCHAR(255))")

for x in range(1, 13):
    for y in range(1, 5):
        file_name="data"+str(x)+"-"+str(y)+".json"
        print(file_name)
        
        # 開啟data
        data=None
        with open(file_name, mode="r") as file:
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
            community=item["community"] #社區
            community_addr=item["community_addr"] #社區2
            kindStr=item["kindStr"] #房屋類型
            layout=item["layoutStr"] #格局
            management_fee=item["priceUnit"]["price"] #管理費-數字
            management_fee_unit=item["priceUnit"]["unit"] #管理費-單位
            house_size=item["areaUnit"]["area"] #總坪數-數字
            house_size_unit=item["areaUnit"]["unit"] #總坪數-單位
            # lat=item["lat"] #經度
            # lng=item["lng"] #緯度

            photos_str=""
            for photos_item_idx in range(len(item["photos"])):
                if photos_item_idx == len(item["photos"])-1:
                    photos_str=photos_str+item["photos"][photos_item_idx]
                else:
                    photos_str=photos_str+item["photos"][photos_item_idx]+","
            photos=photos_str #照片集

            age=item["age"]  #屋齡
            floor=item["floor"] #樓層
            direction=item["direction"] if "direction" in item else ""  #朝向
            im_name=item["im_name"]  #仲介
            company_name=item["company_name"] #仲介公司
            statusquo=item["statusquo"] if "statusquo" in item else ""  #現況
            shape=item["shape"] if "shape" in item else ""  #型態
            fitment=item["fitment"] if "fitment" in item else ""  #裝潢
            isrent_ing=item["isrent_ing"] if "isrent_ing" in item else "" #帶租約
            parking=item["parking"] if "parking" in item else "" #車位
            area_main=item["area_main"] if "area_main" in item else "" #主建物
            area_sub=item["area_sub"] if "area_sub" in item else "" #附屬建物
            area_land=item["area_land"] if "area_land" in item else "" #土地坪數
            remark=item["remark"] if "remark" in item else ""  #房屋描述
            all_addr=item["all_addr"]  #房屋完整地址
            all_layout=item["all_layout"]  #房屋完整格局

            house_life_str=""
            for house_life_idx in range(len(item["house_life"])):
                if house_life_idx == len(item["house_life"])-1:
                    house_life_str=house_life_str+item["house_life"][house_life_idx]
                else:
                    house_life_str=house_life_str+item["house_life"][house_life_idx]+","
            house_life=house_life_str  #周邊機能

            
            val = (houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, community_addr, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit, photos, age, floor, direction, im_name, company_name, statusquo, shape, fitment, isrent_ing, parking, area_main, area_sub, area_land, remark, all_addr, all_layout, house_life)
            valList.append(val)
            # print(val)

        print("houseid:", houseid)  
        sql = "INSERT INTO house (houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, country, community, community_addr, kindStr, layout, management_fee, management_fee_unit, house_size, house_size_unit, photos, age, floor, direction, im_name, company_name, statusquo, shape, fitment, isrent_ing, parking, area_main, area_sub, area_land, remark, all_addr, all_layout, house_life) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, valList)
            
cnnt.commit()    
