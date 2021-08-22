# !/usr/bin/python2
# coding:utf-8
# wishlist table 建置

import os
from dotenv import load_dotenv
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
cursor.execute("use FMH")
#id, userid, houseid, time
cursor.execute("create table wishlist(id varchar(255) primary key, userid bigint not null, houseid varchar(255) not null, time datetime not null default current_timestamp, FOREIGN KEY(houseid) REFERENCES house(houseid))")
# cursor.execute(f"INSERT INTO wishlist (id, userid, houseid) VALUES ('1S9279322', '%"+1+"%','S9279322')")
# valList = (1, 'S9279322')
# sql = "INSERT INTO wishlist (userid, houseid) VALUES (%s, %s)"
# cursor.executemany(sql, valList)
cnnt.commit()