# 在電腦先開啟mongodb
# 下載adminmongo
# 於網址輸入http://127.0.0.1:1234/ => 進入adminmongo

import pymongo

def mongo_connect_build():
    # 跟mongodb建立連線
    global mycol
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # client = pymongo.MongoClient(host="mongodb", port=27017)

    # 選擇使用的db,不存在則會在資料輸入時自動建立
    db = client['mongo_test']

    # 選擇collection,不存在則會在資料輸入時自動建立
    mycol = db["test"]

def data_insert(data):
    # 建立字典,輸入資料

    data_one = mycol.insert_one(data)
    print(data_one)


    # 輸入多項資料
    # mylist = [
    #     {"_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
    #     {"_id": 2, "name": "Google", "address": "Google 搜索"},
    #     {"_id": 3, "name": "Facebook", "address": "脸书"},
    #     {"_id": 4, "name": "Taobao", "address": "淘宝"},
    #     {"_id": 5, "name": "Zhihu", "address": "知乎"}
    # ]

    # data_many = mycol.insert_many(mylist)
    # # 輸出輸入資料的ID
    # print(data_many.inserted_ids)

def data_find():
    # 尋找第一筆資料
    # find_data = mycol.find_one()
    # print(find_data)
    # 尋找多筆資料
    for find_manydata in mycol.find():
        print(find_manydata)

    # 尋找指定欄位 1為要顯示 , 0為不顯示
    # for data_select in mycol.find({}, {"_id": 0, "name": 1, "cn_name": 1}):
        # print(data_select)

    # 下面會噴錯,不可同時指定1和0(除了id),若不顯示就不要打出來
    # for data_select in mycol.find({}, {"_id": 0, "name": 1, "cn_name": 0}):
        # print(data_select)

def data_modify():
    oldquery = {"sex":"dog"}
    newquery = {"$set": {"sex":"male"}}
    # 修改內容 $set ,一次改一筆,從第一筆開始
    mycol.update_one(oldquery, newquery)
    # 一次全改
    mycol.update_many(oldquery,newquery)

def data_delete():
    mydelete = {"name":"Fran"}
    #刪除第一筆
    mycol.delete_one(mydelete)

    #刪除多筆
    mycol.delete_many(mydelete)

    #刪除全部檔案
    mycol.delete_many({})


if __name__ == '__main__':
    mongo_connect_build()