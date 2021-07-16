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

# 建立Cursor物件
cursor=cnnt.cursor()

# cursor.execute("create database FMH")
cursor.execute("use FMH")
# deal_target, address, date, target_number, floor, total_floor, building_state, house_age, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, cart_price
cursor.execute("create table deal(deal_target VARCHAR(255) NOT NULL, address VARCHAR(255) NOT NULL, date VARCHAR(255) NOT NULL, target_number VARCHAR(255) NOT NULL, floor INT NOT NULL, total_floor INT NOT NULL, building_state VARCHAR(255) NOT NULL, house_age INT NOT NULL, building_size INT NOT NULL, pattern_room INT NOT NULL, pattern_hall INT NOT NULL, pattern_health INT NOT NULL, manages VARCHAR(255) NOT NULL, total_price INT NOT NULL, unit_price INT NULL, cart_price INT NULL)")


file="deal_modify.csv"

with open(file, "r", ) as csvFile:
    csvReader = csv.reader(csvFile)
    datas = list(csvReader)

    valList=[]
    for idx, val in enumerate(datas):
        if idx != 0:
            print(idx)
            deal_target=val[0]
            address=val[1].replace('台北市', '')
            date=val[2]
            target_number=val[3] 
            
            # 修改交易樓層 國字->阿拉伯數字 顯示
            floor1=val[4].replace('層', '')
            output1 = cn2an.cn2an(floor1)
            # print(output1)
            floor=int(output1)

            # 修改總樓層 國字->阿拉伯數字 顯示
            floor2=val[5].replace('層', '')
            output2 = cn2an.cn2an(floor2)
            # print(output2)
            total_floor=int(output2)
            
            building_state=val[6]
            house_age=val[7]

            # 總坪數 平方公尺->坪 /  顯示
            size=float(val[8])*0.3025
            size=round(size, 2)
            # print(size)
            building_size=size
            
            pattern_room=int(val[9])
            pattern_hall=int(val[10])
            pattern_health=int(val[11])
            manages=val[12]

            # 總金額 0000->萬顯示
            # print(val[13])
            price=float(val[13]) / 10000
            # print(price)
            total_price=price

            # 單位坪數金額 平方公尺->坪 / 0000->萬顯示
            price2=float(val[13]) / size / 10000
            price2=round(price2, 2)
            # print(price2)
            unit_price=price2,

            # 車位金額 0000->萬顯示
            # print(val[15])
            price3=float(val[15]) / 10000
            # print(price3)
            cart_price=price3

            dbVal = (deal_target, address, date, target_number, floor, total_floor, building_state, house_age, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, cart_price)
            valList.append(dbVal)
            # print(dbVal)

    sql = "INSERT INTO deal (deal_target, address, date, target_number, floor, total_floor, building_state, house_age, building_size, pattern_room, pattern_hall, pattern_health, manages, total_price, unit_price, cart_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, valList)
    
    cnnt.commit()    
    