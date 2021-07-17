# 因591取得的商品列表資料(data1-x.json)乏經緯度, 因次複製data1-x.json至data-map1-x.json, 並於複製過程中加入經緯度欄位
# 以假定該區的經緯度範圍, 隨機給定範圍內的值, 透過開啟舊檔案(data1-x.json)複寫並加入經緯度欄位至新檔案(data-map1-x.json)
import json
import random
with open("data7-4.json", mode="r", encoding="utf-8") as file:     #讀取JSON檔案
    data=json.load(file)

    for item in data["data"]:
        print(item["address"])
        # 中正區1-1 / 1-4
        # item["lat"]=25.0+random.uniform(0.02,0.04)
        # item["lng"]=121.5+random.uniform(0.01,0.02)

        # 大同區2-1 / 2-4
        # item["lat"]=25.0+random.uniform(0.05,0.07)
        # item["lng"]=121.5+random.uniform(0.00,0.01)

        # 中山區3-1 / 3-4
        # item["lat"]=25.0+random.uniform(0.04,0.06)
        # item["lng"]=121.5+random.uniform(0.02,0.03)

        # 松山區4-1 / 4-4
        # item["lat"]=25.0+random.uniform(0.04,0.06)
        # item["lng"]=121.5+random.uniform(0.05,0.07)

        # 大安區5-1 / 5-4
        # item["lat"]=25.0+random.uniform(0.03,0.04)
        # item["lng"]=121.5+random.uniform(0.04,0.05)

        # 萬華區6-1 / 6-4
        # item["lat"]=25.0+random.uniform(0.02,0.04)
        # item["lng"]=121.4+random.uniform(0.09,0.15)

        # 區7-1 / 7-4
        item["lat"]=25.0+random.uniform(0.02,0.04)
        item["lng"]=121.4+random.uniform(0.06,0.08)

    newdata=data
    print(newdata["data"][0]["lat"])


with open("data-map7-4.json", mode="w", encoding="utf-8") as file:     #複寫JSON檔案
    json.dump(newdata, file, ensure_ascii=False)

# print( 25.03+random.uniform(0.001,0.009) ) 
# print( 121.52+random.uniform(0.001,0.009) ) 