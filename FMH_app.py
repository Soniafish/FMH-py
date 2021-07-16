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
    return("Wellcome FHM page!!")  

@app.route("/fmh") 
def fmh(): 
    return("Wellcome FHM api page!!")  

@app.route("/fmh/api/houses", methods=["POST", "OPTION"])  #取得房屋物件列表
@cross_origin()
def handleHouses():

    if request.method=="OPTION":
        return 

    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object")
    print(connection_object)
    print(cursor) 

    insertValues=request.get_json()
    page=insertValues["currentPage"]    #預設page值為1
    keyword=insertValues["keyword"]     #預設keyword值為""
    filter_country=insertValues["filter"]["country"] 
    filter_layout=insertValues["filter"]["layout"]
    filter_price_min=insertValues["filter"]["price"]["min"]
    filter_price_max=insertValues["filter"]["price"]["max"]
    filter_size_min=insertValues["filter"]["size"]["min"]
    filter_size_max=insertValues["filter"]["size"]["max"]
    sortby_kind=insertValues["sortby"]["kind"]
    sortby_order=insertValues["sortby"]["order"]
    print(page)
    print(keyword)

    statement=""
    p_idx = 20 * (page - 1)
    p_count = 20
    nextPage = page+1
    totalPage = 0
    sumItem = 0

    # 有關鍵字
    if keyword!="":
        statement=f" where address like '%"+keyword+"%'"
    
    # 有filter
    elif filter_country!="all" or filter_layout!="all" or filter_price_min!=-1 or filter_size_min!=-1:
        statement = " where"
        firstFilter=True
        if filter_country!="all":
            statement = statement +" (country ='"+filter_country+"')"
            firstFilter=False
        if filter_layout!="all":
            if firstFilter:
                statement = statement + " (layout ='"+filter_layout+"')"
            else:
                statement = statement + " and (layout ='"+filter_layout+"')"
                firstFilter=False
        if filter_price_min!=-1:
            if firstFilter:
                statement = statement + f" (house_price between {filter_price_min} and {filter_price_max} )"
            else:
                statement = statement + f" and (house_price between {filter_price_min} and {filter_price_max} )"
                firstFilter=False
        if filter_size_min!=-1:
            if firstFilter:
                statement = statement + f" (house_size between {filter_size_min} and {filter_size_max} )"
            else:
                statement = statement + f" and (house_size between {filter_size_min} and {filter_size_max} )"
                firstFilter=False
    else:
        statement=""

    # 取得符合條件的總數
    countStatement = "select count(*) from house" + statement
    print("countStatement:", countStatement)
    
    cursor.execute(countStatement)
    count=cursor.fetchone()
    sumItem = count[0]
    print("count", sumItem)
    totalPage = math.ceil(sumItem / p_count)
    
    # 查無結果 或 總數小於查詢頁數*20
    if count[0] <= p_idx:
        return Response(
            response=json.dumps({
                "sumItem": sumItem,
                "totalPage": totalPage,
                "nextPage": -1,
                "data": []
            }),
            status=200,
            content_type='application/json'
        )
    elif count[0] <  20 * page :
        p_count = count[0] % 20
        nextPage = -1
        # print("p_count:", p_count)

    # 取得符合條件的資料, 並加入排序
    if sortby_kind !="":        
        filterStatement = "select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, lat, lng from house" + statement + " order by " + sortby_kind + " " + sortby_order
    else:
        filterStatement = "select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, lat, lng from house" + statement + " order by houseid"
    print("filterStatement:", filterStatement)

    # 取得符合條件且對應頁碼的資料
    finalStatement = filterStatement+f" limit {p_idx},{p_count}"
    print("finalStatement", "finalStatement")

    cursor.execute(finalStatement)
    filterData=cursor.fetchall() #取得物件
    # print("filterData")
    print("filterData[0]", filterData[0])

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
                "area_price": item[8],
                "lat": item[9],
                "lng": item[10]
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

@app.route("/fmh/api/house", methods=["POST", "OPTION"])  #取得房屋物件資料
@cross_origin()
def handleHouse():

    if request.method=="OPTION":
        return 

    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object")
    print(connection_object)
    print(cursor) 

    insertValues=request.get_json()
    houseid=insertValues["houseid"]    #預設page值為1
    filterStatement = "select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price from house where houseid='"+houseid+"'"
    cursor.execute(filterStatement)
    filterData=cursor.fetchone() #取得物件
    print("filterData")
    print(filterData)

    if filterData:
        data={
            "houseid": filterData[0],
            "area_misc": filterData[1],
            "address": filterData[2],
            "title": filterData[3],
            "photo_src": filterData[4],
            "layout_misc": filterData[5],
            "house_price": filterData[6],
            "house_price_unit": filterData[7],
            "area_price": filterData[8],
        }

        # 實價登錄
        searchAddress=filterData[2].split("-")
        print(searchAddress)
        searchRoad=searchAddress[1]
        print(searchRoad)
        filterStatement = f"select address, date, floor, total_floor, building_state, house_age, building_size, pattern_room, pattern_hall, total_price, unit_price, cart_price from deal where address like '%"+searchRoad+"%' order by date desc"
        cursor.execute(filterStatement)
        filterData2=cursor.fetchall() #取得物件
        print("filterData2")
        print(filterData2[0])
        dealData=[]
        if filterData2:
            for item in filterData2:
                dealData.append({
                    "address": item[0],
                    "date": item[1],
                    "floor": item[2],
                    "total_floor": item[3],
                    "building_state": item[4],
                    "house_age": item[5],
                    "building_size": item[6],
                    "pattern_room": item[7],
                    "pattern_hall": item[8],
                    "total_price": item[9],
                    "unit_price": item[10],
                    "cart_price": item[11]
                })

        # 關閉db連線
        cursor.close()
        connection_object.close()

        # print(data)
        return Response(
                response=json.dumps({
                    "data": {
                        "houseInfo": data, 
                        "dealList": dealData,    
                    }
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
                "error": "true",
                "message": "物件編號不正確"
            }),
            status=400,
            content_type='application/json'
        )

    # 關閉db連線
    cursor.close()
    connection_object.close()

    return Response(
            response=json.dumps({
                "error": "true",
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