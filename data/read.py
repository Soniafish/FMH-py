# 使用 JSON 格式讀取檔案、複寫檔案
import json
with open("data-test.json", mode="r", encoding="utf-8") as file:     #讀取JSON檔案
    data=json.load(file)

    for item in data["data"]:
        print(item["address"])
        if item["address"].find("臨沂街")!=0:
            print("has")
            item["lat"]=25.0389801
            item["lng"]=121.5272577
        elif item["address"].find("重慶南路三段")!=0:
            item["lat"]=25.0259389
            item["lng"]=121.5140441
        elif item["address"].find("桃源街")!=0:
            item["lat"]=25.0401674
            item["lng"]=121.5081122
        elif item["address"].find("林森北路")!=0:
            item["lat"]=25.0477035
            item["lng"]=121.5220058
        elif item["address"].find("三元街")!=0:
            item["lat"]=25.0283909
            item["lng"]=121.5083201
        elif item["address"].find("中華路二段")!=0:
            item["lat"]=25.0284581
            item["lng"]=121.5033437
        elif item["address"].find("惠安街")!=0:
            item["lat"]=25.0292042
            item["lng"]=121.5047759
        elif item["address"].find("汀州路二段")!=0:
            item["lat"]=25.0248088
            item["lng"]=121.517829
        elif item["address"].find("汀州路一段")!=0:
            item["lat"]=25.0289478
            item["lng"]=121.5063579
        elif item["address"].find("信義路二段")!=0:
            item["lat"]=25.0339475
            item["lng"]=121.5265789
        elif item["address"].find("羅斯福路四段")!=0:
            item["lat"]=25.0139784
            item["lng"]=121.532808
        elif item["address"].find("廈門街")!=0:
            item["lat"]=25.0244451
            item["lng"]=121.5152349
        elif item["address"].find("晉江街")!=0:
            item["lat"]=5.0236829
            item["lng"]=121.521579
        elif item["address"].find("汀州路三段")!=0:
            item["lat"]=25.0161233
            item["lng"]=121.528521
        elif item["address"].find("詔安街")!=0:
            item["lat"]=25.0255518
            item["lng"]=121.5096225
        elif item["address"].find("中華路一段")!=0:
            item["lat"]=25.0438123
            item["lng"]=121.506757
        elif item["address"].find("南昌路一段")!=0:
            item["lat"]=25.0316768
            item["lng"]=121.5146806
        elif item["address"].find("莒光路")!=0:
            item["lat"]=25.0312067
            item["lng"]=121.5037413
        elif item["address"].find("博愛路")!=0:
            item["lat"]=25.0403341
            item["lng"]=121.5092223
        elif item["address"].find("濟南路二段")!=0:
            item["lat"]=25.0406291
            item["lng"]=121.5278428
        elif item["address"].find("延平南路")!=0:
            item["lat"]=25.0406291
            item["lng"]=121.5278428
        elif item["address"].find("水源路")!=0:
            item["lat"]=25.03974
            item["lng"]=121.4913819
        elif item["address"].find("和平西路二段")!=0:
            item["lat"]=25.0304372
            item["lng"]=121.5074526
        elif item["address"].find("重慶南路二段")!=0:
            item["lat"]=25.0326367
            item["lng"]=121.5116704
        elif item["address"].find("仁愛路二段")!=0:
            item["lat"]=25.038131
            item["lng"]=121.5271706
        elif item["address"].find("牯嶺街")!=0:
            item["lat"]=25.0274508
            item["lng"]=121.5161369

    newdata=data
    print(newdata["data"][0]["lat"])
# 中正區-臨沂街 25.0389801,121.5272577
# 中正區-重慶南路三段 25.0259389,121.5140441
# 中正區-桃源街 25.0401674,121.5081122
# 中正區-林森北路 25.0477035,121.5220058
# 中正區-三元街 25.0283909,121.5083201
# 中正區-中華路二段 25.0284581,121.5033437
# 中正區-惠安街 25.0292042,121.5047759
# 中正區-汀州路二段 25.0248088,121.517829
# 中正區-汀州路一段 25.0289478,121.5063579
# 中正區-信義路二段 25.0339475,121.5265789
# 中正區-羅斯福路四段 25.0139784,121.532808
# 中正區-廈門街 25.0244451,121.5152349
# 中正區-晉江街 25.0236829,121.521579
# 中正區-汀州路三段 25.0161233,121.528521
# 中正區-詔安街 25.0255518,121.5096225
# 中正區-中華路一段 25.0438123,121.506757
# 中正區-南昌路一段 25.0316768,121.5146806
# 中正區-莒光路 25.0312067,121.5037413
# 中正區-博愛路 25.0403341,121.5092223
# 中正區-濟南路二段 25.0406291,121.5278428
# 中正區-延平南路 25.0396973,121.5067028
# 中正區-水源路 25.03974,121.4913819
# 中正區-和平西路二段 25.0304372,121.5074526
# 中正區-重慶南路二段 25.0326367,121.5116704
# 中正區-仁愛路二段 25.038131,121.5271706
# 中正區-牯嶺街 25.0274508,121.5161369

# 大同區-華亭街 25.052942,121.5110032
# 大同區-延平北路二段 25.0583095,121.5093048
# 大同區-承德路三段 25.0711638,121.516345
# 大同區-酒泉街 25.0715078,121.5124164

# 中山區-新生北路一段 25.0479507,121.5279084
# 中山區-林森北路 25.0570574,121.5233167
# 中山區-南京東路二段 25.051946,121.5302286
# 中山區-中原街 25.0598196,121.5267398

# 松山區-市民大道六段 25.0492061,121.5726375
# 松山區-南京東路四段 25.0517507,121.5505622
# 松山區-南京東路五段 25.0513775,121.5616032
# 松山區-撫遠街 25.0644657,121.5636015

# 大安區-復興南路一段 25.0397901,121.5416372
# 大安區-仁愛路四段 25.0375801,121.5516246
# 大安區-大安路一段 25.0393849,121.5438863
# 大安區-光復南路 25.0376663,121.5554478

# 萬華區-武昌街二段 25.0448399,121.5042148
# 萬華區-西園路二段 25.0282053,121.4930013
# 萬華區-柳州街 25.0382336,121.5030707
# 萬華區-漢中街 25.0434796,121.5050278

# 信義區-吳興街 25.0265271,121.5620001
# 信義區-永吉路 25.0455262,121.571363
# 信義區-忠孝東路五段 25.0409713,121.5718387
# 信義區-福德街 25.0388877,121.5838253

with open("data-newtest.json", mode="w", encoding="utf-8") as file:     #複寫JSON檔案
    json.dump(newdata, file, ensure_ascii=False)