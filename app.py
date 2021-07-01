# !/usr/bin/python2
# coding:utf-8

# 安裝 pip3 install Flask
import os
from dotenv import load_dotenv
from flask import Flask     #載入Flask物件

load_dotenv()
os.environ

#建立 Application 物件,
app=Flask(__name__)     


# 建立路徑 / 對應的處理函式
@app.route("/")     
def index():    #用來回應路徑 / 的處理方式
    return("Hello Flask")    #回傳網站首頁的內容


#啟動網站伺服器
app.run()     

if (os.environ['localdebug']=='true'):
    app.run(port=5000)
else:
    app.run(port=5000, host='0.0.0.0')