# 實價登錄資料來源: https://plvr.land.moi.gov.tw/DownloadOpenData
# 將實價登錄資料(00a_lvr_land_a.csv)存入table deal裏
import csv
import cn2an

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
# deal_target, district, address, date, target_number, floor, total_floor, building_state, main_use, complete_years, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, parking_type, parking_size, parking_price
# cursor.execute("create table deal(deal_target VARCHAR(255) NOT NULL, district VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL, date VARCHAR(255) NOT NULL, target_number VARCHAR(255) NOT NULL, floor INT NOT NULL, total_floor INT NOT NULL, building_state VARCHAR(255) NOT NULL, main_use VARCHAR(255) NOT NULL, complete_years VARCHAR(255) NOT NULL, building_size INT NOT NULL, pattern_room INT NOT NULL, pattern_hall INT NOT NULL, pattern_health INT NOT NULL, manages VARCHAR(255) NOT NULL, total_price INT NOT NULL, unit_price INT NULL, parking_type VARCHAR(255) NOT NULL, parking_size INT NOT NULL, parking_price INT NULL)")


file="05a_lvr_land_a.csv"

with open(file, "r", ) as csvFile:
    csvReader = csv.reader(csvFile)
    datas = list(csvReader)

    valList=[]
    for idx, val in enumerate(datas):
        if idx != 0:
            print(idx)
            district=val[0]
            deal_target=val[1]
            address=val[2]
            date=val[3]
            target_number=val[4]

            # 修改交易樓層 國字->阿拉伯數字 顯示
            floor1=val[5].replace('層', '')
            output1 = cn2an.cn2an(floor1)
            floor=int(output1)

            # 修改總樓層 國字->阿拉伯數字 顯示
            floor2=val[6].replace('層', '')
            output2 = cn2an.cn2an(floor2)
            # print(output2)
            total_floor=int(output2)

            building_state=val[7]
            main_use=val[8]
            complete_years=val[9]

            # 總坪數 平方公尺->坪 /  顯示
            size=float(val[10])*0.3025
            size=round(size, 2)
            # print(size)
            building_size=size

            pattern_room=int(val[11])
            pattern_hall=int(val[12])
            pattern_health=int(val[13])
            manages=val[14]

            # 總金額 0000->萬顯示
            # print(val[15])
            price=float(val[15]) / 10000
            # print(price)
            total_price=price

            # 單位坪數金額 平方公尺->坪 / 0000->萬顯示
            price2=float(val[16]) / size / 10000
            price2=round(price2, 2)
            # print(price2)
            unit_price=price2

            parking_type=val[17]

            # 車位坪數 平方公尺->坪 /  顯示
            size2=float(val[18])*0.3025
            size2=round(size2, 2)
            # print(size2)
            parking_size=size2

            # 車位金額 0000->萬顯示
            price3=float(val[19]) / 10000
            # print(price3)
            parking_price=price3
            
            # deal_target, district, address, date, target_number, floor, total_floor, building_state, main_use, complete_years, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, parking_type, parking_size, parking_price
            dbVal = (deal_target, district, address, date, target_number, floor, total_floor, building_state, main_use, complete_years, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, parking_type, parking_size, parking_price)
            valList.append(dbVal)
            # print(dbVal)

    sql = "INSERT INTO deal (deal_target, district, address, date, target_number, floor, total_floor, building_state, main_use, complete_years, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, parking_type, parking_size, parking_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, valList)
    
    cnnt.commit()    
    