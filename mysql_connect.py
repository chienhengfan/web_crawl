import pymongo
import pymysql
import time
import json
import re

def mongo_connect_build():
    global mycol
    client = pymongo.MongoClient("mongodb://192.168.1.106:27017/")
    db = client['Topic_104']
    mycol = db["Jobs"]


def connect_to_mysql():
    # 設定資料庫連線資訊
    db_setting = {
        "host" : 'localhost',
        "port" : 3306,
        "user" : 'root',
        "passwd" : 'harry8410',
        "db" : "topic_104",
        "charset" : 'utf8mb4'
        }
# 建立連線
    conn = pymysql.connect(**db_setting)
    print('Successfully connected to DB : {} !'.format(db_setting["db"]))
    return conn


# 清洗資料insert mysql的欄位
mongo_connect_build()
for data in mycol.find({}, {"_id": 0}):

    try:
        rowinsert = []

        # 連線mysql
        conn = connect_to_mysql()

        # 取出ID裡的values,將其變字典,以便搜尋
        data_total = list(data.values())[0]

        # 工作ID
        data_ID = list(data.keys())[0]
        rowinsert.append(data_ID)

        # 職稱
        data_jobname = data_total["jobName"]
        rowinsert.append(data_jobname)

        # 公司產業類別
        data_industry = data_total["industry"]
        rowinsert.append(data_industry)

        # 職務類別
        data_category = data_total["jobCategory"][0]['description']
        rowinsert.append(data_category)

        # 公司名稱
        data_companyname = data_total["companyName"]
        rowinsert.append(data_companyname)

        # 公司地區
        data_workarea = data_total["addressRegion"]
        rowinsert.append(data_workarea)

        # 工作經驗
        if data_total["workExp"] == []:
            data_workexp = "不拘"
        else:
            data_workexp = data_total["workExp"]
        rowinsert.append(data_workexp)

        # 教育程度
        if data_total["edu"] == []:
            data_edu = "不拘"
        else:
            data_edu = data_total["edu"]
        rowinsert.append(data_edu)

        # 相關科系
        if data_total["major"] == []:
            data_dept = "不拘"
        else:
            data_dp = ""
            for i in data_total["major"]:
                data_dp = data_dp + ',' + i
                data_dept = data_dp.strip(',')
        rowinsert.append(data_dept)

        # 語言能力
        if data_total["language"] == []:
            data_lan = "不拘"
        else:
            data_lan = list(data_total["language"][0].values())[0]
        rowinsert.append(data_lan)

        # 工作技能
        if data_total["skill"] == []:
            data_skill = "不拘"
        else:
            data_sk = ""
            for i in data_total["skill"]:
                data_sk = data_sk + ',' + (i["description"])
                data_skill = data_sk.strip(',')
        rowinsert.append(data_skill)

        # 主要證照
        if data_total["certificate"] == []:
            data_len = "不拘"
        else:
            data_len = ""
            for i in data_total["certificate"]:
                data_len = (data_len + ',' + i).strip(',')
        rowinsert.append(data_len)

        # 外派
        if data_total["businessTrip"] == "無需出差外派":
            data_trip = "無"
        else:
            data_trip = "有"
        rowinsert.append(data_trip)

        # 管理責任
        if data_total["manageResp"] == "":
            data_manage = "無"
        elif data_total["manageResp"] == "不需負擔管理責任":
            data_manage = "無"
        else:
            data_manage = "需要"
        rowinsert.append(data_manage)

        # 工作時間
        data_time = data_total["workPeriod"]
        data_workperiod = data_time.split("，")[0]
        rowinsert.append(data_workperiod)

        # 休假
        data_vaca = data_total["vacationPolicy"]
        rowinsert.append(data_vaca)

        # 薪水
        pattern = '\d+'
        if data_total["salary"] == "待遇面議":
            min_sal = "40000"
            max_sal = "40000"

        elif "月薪" in data_total["salary"]:
            data_money = re.findall(pattern, data_total["salary"])
            if len(data_money) == 2:
                min_sal = (data_money[0] + data_money[1])
                max_sal = min_sal

            else:
                min_sal = (data_money[0] + data_money[1])
                max_sal = (data_money[2] + data_money[3])

        elif "時薪" in data_total["salary"]:
            min_sal = (data_total["salaryMin"])
            max_sal = (data_total["salaryMax"])

        else:
            min_sal = (data_total["salaryMin"])
            max_sal = (data_total["salaryMax"])
        rowinsert.append(min_sal)
        rowinsert.append(max_sal)

        # 公司福利
        data_combenefit = data_total["welfare"].replace("\n", "").replace("\r", "").replace("\t", "")
        rowinsert.append(data_combenefit)

        # 工作內容
        data_content = data_total["jobDescription"].replace("\n", "").replace("\r", "").replace("\t", "") + data_total[
            "other"].replace("\n", "").replace("\r", "").replace("\t", "")
        rowinsert.append(data_content)

        cursor = conn.cursor() #建立mysql游標

        # insert資料
        insert_sql = '''insert into job_104 (Job_ID,Job_Name,Job_Industry,Job_Category,Company,
        Work_area,Work_exp,Edu,Department,Lan,Job_skill,License,Expat,Manage,Working_time,Vacation,
        min_sal,max_sal,Benefit_Comp,Job_Discription) values 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'''

        # 游標執行(insert指令,資料)
        cursor.execute(insert_sql, rowinsert)
        conn.commit()

        #游標關閉
        cursor.close()
        #中斷連線
        conn.close()
        print(data_ID + "已導入mysql")
        print("===========================")
    except Exception as e:
        pass
        print(list(data.keys())[0], e, "沒導入")