# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json 
import requests   
from flask_cors import CORS, cross_origin


load_dotenv()
os.environ

#建立 Application 物件,
app=Flask(__name__)     
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")     
def index(): 
    return("Hello Flask")  

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


#啟動網站伺服器  
if (os.environ['localdebug']=='true'):
    app.run(port=5000)
else:
    app.run(port=5000, host='0.0.0.0')