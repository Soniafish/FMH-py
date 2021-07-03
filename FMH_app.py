# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json 
import requests   
from flask_cors import CORS, cross_origin
from mysql.connector import Error
from mysql.connector import pooling
import pymysql
import math


load_dotenv()
os.environ


# 建立connection_pool物件
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool",
    pool_size=20,
    pool_reset_session=True,
    host=os.environ["db_host"],
    database='FMH',
    user=os.environ["db_user"],
    password=os.environ["db_password"])
print("Printing connection pool properties")
print("Connection Pool Name - ", connection_pool.pool_name)
print("Connection Pool Size - ", connection_pool.pool_size)


#建立 Application 物件,
app=Flask(__name__) 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/") 
def index(): 
    return("Wellcome FHM api page!!")  

@app.route("/test", methods=["POST"])
@cross_origin()
def test():
    insertValues=request.get_json()
    userName=insertValues["name"]
    return Response(
                response=json.dumps({
                    "error": True,
                    "message": userName+": cross_origin safe!"
                }),
                status=200,
                content_type='application/json'
            )


@app.route("/api/houses", methods=["GET"])
def handleHouses():
    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_attractions")
    print(connection_object)
    print(cursor)

    #預設page值為0
    insertValues=request.get_json()
    page=insertValues["currentPage"]   #預設page值為1
    keyword=insertValues["keyword"] #預設keyword值為""
    # print(page)
    # print(keyword)

    tatement=""
    p_idx = 20 * (page - 1)
    p_count = 20
    nextPage = page+1
    totalPage = 0
    sumItem = 0

    if keyword=="":
        cursor.execute("select count(*) from house")
        count=cursor.fetchone()
        # print("count")
        # print(count[0])
        sumItem = count[0]
        totalPage = math.ceil(count[0] / p_count)

        if count[0] < p_idx:
            return Response(
                response=json.dumps({
                    "nextPage": None,
                    "data": []
                }),
                status=200,
                content_type='application/json'
            )
        elif count[0] <  20 * (page + 1):
            p_count = count[0] % 20
            nextPage = None
            # print("p_count:", p_count)
        statement=f"select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price from house order by houseid limit {p_idx},{p_count}"
    else:
        cursor.execute("select count(*) from house where address like '%"+keyword+"%'")
        count=cursor.fetchone()
        # print(count[0])
        sumItem = count[0]
        totalPage = math.ceil(count[0] / p_count)

        if count[0] <  20 * (page + 1):
            p_count = count[0] % 20
            nextPage = None
            # print("p_count:", p_count)
        statement ="select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price from house where address like '%"+keyword+f"%' order by houseid limit {p_idx},{p_count}"
        # print(statement)

    cursor.execute(statement)
    filterData=cursor.fetchall() #取得物件
    # print("filterData")
    # print(filterData)

    if filterData:   
        data=[]
        for item in filterData:
            data.append({
                "houseid": item[0],
                "area_misc": item[1],
                "address": item[2],
                "title": item[3],
                "photo_src": item[4],
                "layout_misc": item[5],
                "house_price": item[6],
                "house_price_unit": item[7],
                "area_price": item[8]
            })

        # 關閉db連線
        cursor.close()
        connection_object.close()

        return Response(
                response=json.dumps({
                    "sumItem": sumItem,
                    "totalPage": totalPage,
                    "nextPage": nextPage,
                    "data": data
                }),
                status=200,
                content_type='application/json'
            )

    else:
        # 關閉db連線
        cursor.close()
        connection_object.close()

        return Response(
                response=json.dumps({
                    "nextPage": None,
                    "data": []
                }),
                status=200,
                content_type='application/json'
            )
	
    # 關閉db連線
    cursor.close()
    connection_object.close()

    return Response(
                response=json.dumps({
                    "error": true,
                    "message": "系統錯誤"
                }),
                status=500,
                content_type='application/json'
            )

 

#啟動網站伺服器  
if (os.environ['localdebug']=='true'):
    app.run(port=5000)
else:
    app.run(port=5000, host='0.0.0.0')