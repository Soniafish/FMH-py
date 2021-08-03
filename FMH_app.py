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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
    print(insertValues)
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
                firstFilter=False
            else:
                statement = statement + " and (layout ='"+filter_layout+"')"
        if filter_price_min!=-1:
            if firstFilter:
                statement = statement + f" (house_price between {filter_price_min} and {filter_price_max} )"
                firstFilter=False
            else:
                statement = statement + f" and (house_price between {filter_price_min} and {filter_price_max} )"
        if filter_size_min!=-1:
            if firstFilter:
                statement = statement + f" (house_size between {filter_size_min} and {filter_size_max} )"
                firstFilter=False
            else:
                statement = statement + f" and (house_size between {filter_size_min} and {filter_size_max} )"
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
        filterStatement = "select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, lat, lng, all_addr, im_name from house" + statement + " order by " + sortby_kind + " " + sortby_order
    else:
        filterStatement = "select houseid, area_misc, address, title, photo_src, layout_misc, house_price, house_price_unit, area_price, lat, lng, all_addr, im_name from house" + statement + " order by houseid"
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
                "lng": item[10],
                "all_addr": item[11],
                "im_name" : item[12]
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
    houseid=insertValues["houseid"]    #取得houseid
    filterStatement = "select houseid, area_misc, address, all_addr, title, photo_src, layout_misc, house_price, house_price_unit, area_price, house_size, photos, age, floor, direction, im_name, company_name, statusquo, shape, fitment, management_fee, isrent_ing, parking, area_main, area_sub, area_land, community, remark, house_life from house where houseid='"+houseid+"'"
    cursor.execute(filterStatement)
    filterData=cursor.fetchone() #取得物件
    print("filterData")
    print(filterData)
    
    if filterData:
        data={
            "houseid": filterData[0],
            "area_misc": filterData[1],
            "address": filterData[2],
            "all_addr":filterData[3],
            "title": filterData[4],
            "photo_src": filterData[5],
            "layout_misc": filterData[6],
            "house_price": filterData[7],
            "house_price_unit": filterData[8],
            "area_price": filterData[9],
            "house_size": filterData[10],
            "photos": filterData[11], 
            "age": filterData[12], 
            "floor": filterData[13], 
            "direction": filterData[14], 
            "im_name": filterData[15], 
            "company_name": filterData[16], 
            "statusquo": filterData[17], 
            "shape": filterData[18], 
            "fitment": filterData[19], 
            "managefee": filterData[20], 
            "isrent_ing": filterData[21], 
            "parking": filterData[22], 
            "area_main": filterData[23], 
            "area_sub": filterData[24], 
            "area_land": filterData[25], 
            "community": filterData[26],
            "remark": filterData[27],
            "house_life": filterData[28]
        }

        # 實價登錄
        searchAddress=filterData[2].split("-")
        print(searchAddress)
        searchRoad=searchAddress[1]
        print(searchRoad)
        filterStatement = f"select address, date, floor, total_floor, building_state, complete_years, building_size, pattern_room, pattern_hall, total_price, unit_price, parking_price from deal where address like '%"+searchRoad+"%' order by date desc"
        cursor.execute(filterStatement)
        filterData2=cursor.fetchall() #取得物件
        print("filterData2")
        dealData=[]
        if filterData2:
            print(filterData2[0])
            for item in filterData2:
                dealData.append({
                    "address": item[0],
                    "date": item[1],
                    "floor": item[2],
                    "total_floor": item[3],
                    "building_state": item[4],
                    "complete_years": item[5],
                    "building_size": item[6],
                    "pattern_room": item[7],
                    "pattern_hall": item[8],
                    "total_price": item[9],
                    "unit_price": item[10],
                    "parking_price": item[11]
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

@app.route("/fmh/api/user", methods=["POST", "OPTION"]) #註冊
@cross_origin()
def handel_signup():

    if request.method=="OPTION":
        return 

    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    try:
        insertValues=request.get_json()
        userName=insertValues["name"]
        userEmail=insertValues["email"]
        userPW=insertValues["password"]

        # 篩選資料表的資料
        cursor.execute("SELECT * FROM user where email='"+userEmail+"'")
        filterData=cursor.fetchone()
        
        if filterData: # 註冊失敗:即資料表已有該使用者帳號
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "註冊失敗，重複的Email或其他原因"
                }),
                status=200,
                content_type='application/json'
            )
            
        # 註冊成功：即資料表無該使用者帳號
        cursor.execute("INSERT INTO user(name, email, password)VALUES('" + userName + "','" + userEmail + "', '" + userPW + "')")
        connection_object.commit()

        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({"ok": True}),
            status=200,
            content_type='application/json'
        ) 
    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({
                "error": True,
                "message": "系統錯誤"
            }),
            status=500,
            content_type='application/json'
        )

@app.route("/fmh/api/user", methods=["PATCH", "OPTION"]) #登入
@cross_origin()
def handel_signin():

    if request.method=="OPTION":
        return 

    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_user")
    print(connection_object)
    print(cursor)
    
    try:
        insertValues=request.get_json()
        userEmail=insertValues["email"]
        userPW=insertValues["password"]
        
        # print("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        # 篩選資料表的資料
        cursor.execute("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        select_data=cursor.fetchone()#取得使用者資料
        # print(select_data)
        
        if select_data:   # 登入成功：即帳號/密碼皆存在資料表
        
            session["userId"] = select_data[0]
            session["userName"] = select_data[1]
            session["userEmail"] = select_data[2]

            print("login_session", session)

            cursor.close()
            connection_object.close()
            return Response(
                    response=json.dumps({
                        "ok": True,
                        "data": {
                            "id": session["userId"],
                            "name": session["userName"],
                            "email": session["userEmail"]
                        }
                    }),
                    status=200,
                    content_type='application/json'
                )
        
        # 登入失敗：即帳號或密碼不存在資料表
        cursor.close()
        connection_object.close()
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "帳號或密碼輸入錯誤"
                    }),
                    status=400,
                    content_type='application/json'
                )
    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "系統錯誤"
                    }),
                    status=500,
                    content_type='application/json'
                )

@app.route("/fmh/api/wishlist", methods=["POST", "OPTION"]) #加入最愛清單
@cross_origin()
def handel_addWish():

    if request.method=="OPTION":
        return 

    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_user")
    print(connection_object)
    print(cursor)
    try:
        insertValues=request.get_json()
        userid=insertValues["userid"]
        houseid=insertValues["houseid"]
        wishlistid=str(userid)+houseid

        # 篩選資料表的資料
        cursor.execute("SELECT * FROM wishlist where id='"+wishlistid+"'")
        filterData=cursor.fetchone()
        if filterData: #已加過清單
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "物件已在最愛清單裡"
                }),
                status=200,
                content_type='application/json'
            )

        # 加入最愛清單
        statement="INSERT INTO wishlist(id, userid, houseid)VALUES('"+wishlistid +f"', { userid }, '"+ houseid +"')"
        print(statement)
        result=cursor.execute(statement)
        connection_object.commit()
        cursor.close()
        connection_object.close()

        if result == 0: #新增失敗, 可能已加過清單
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "新增失敗"
                }),
                status=400,
                content_type='application/json'
            )

        #成功加入最愛清單 
        return Response(
                response=json.dumps({"ok": True}),
                status=200,
                content_type='application/json'
            )

    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({
                "error": True,
                "message": "系統錯誤"
            }),
            status=500,
            content_type='application/json'
        )
        
@app.route("/fmh/api/wishlist", methods=["PATCH", "OPTION"]) #取得最愛清單
@cross_origin()
def handel_wishlist():

    if request.method=="OPTION":
        return 

    try:
        # 建立cursor物件 
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        print("connection_object_user")
        print(connection_object)
        print(cursor)

        insertValues=request.get_json()
        print(insertValues)
        userid=insertValues["userid"]
        # 篩選資料表的資料
        statement=f"SELECT house.houseid, house.area_misc, house.address, house.title, house.photo_src, house.layout_misc, house.house_price, house.house_price_unit, house.area_price, house.lat, house.lng, house.all_addr, house.im_name FROM wishlist inner join house on wishlist.houseid=house.houseid where wishlist.userid={userid} order by wishlist.time desc"
        cursor.execute(statement)
        filterData=cursor.fetchall() #取得物件
        # print("filterData")
        # print("filterData[0]", filterData[0])

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
                    "lng": item[10],
                    "all_addr": item[11],
                    "im_name" : item[12]
                })

            # 關閉db連線
            cursor.close()
            connection_object.close()

            return Response(
                    response=json.dumps({
                        "data": data
                    }),
                    status=200,
                    content_type='application/json'
                )

        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "查無資料"
                    }),
                    status=400,
                    content_type='application/json'
                )

	
    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "系統錯誤"
                    }),
                    status=500,
                    content_type='application/json'
                )

@app.route("/fmh/api/wishlist", methods=["DELETE", "OPTION"]) #刪除最愛清單
@cross_origin()
def handel_deltWish():

    if request.method=="OPTION":
        return 

    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_user")
    print(connection_object)
    print(cursor)
    try:
        insertValues=request.get_json()
        userid=insertValues["userid"]
        print("userid", userid)
        houseid=insertValues["houseid"]
        print("houseid", houseid)
        wishlistid=str(userid)+houseid
        print("wishlistid", wishlistid)

        # 刪除最愛清單
        statement="DELETE FROM wishlist WHERE id = '"+wishlistid+"'"
        print(statement)
        result=cursor.execute(statement)
        connection_object.commit()
        cursor.close()
        connection_object.close()

        #成功刪除最愛清單 
        return Response(
                response=json.dumps({"ok": True}),
                status=200,
                content_type='application/json'
            )

    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({
                "error": True,
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