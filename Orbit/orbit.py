import sys
from PySide2 import QtCore, QtScxml
from comb_da_concept_extractor import DA_Concept
import requests
import json
from datetime import datetime, timedelta, time
import pandas as pd


# 都道府県名のリスト
prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

# 都道府県名から緯度と経度を取得するための辞書
latlondic = {'北海道': (43.06, 141.35), '青森': (40.82, 140.74), '岩手': (39.7, 141.15), '宮城': (38.27, 140.87),
             '秋田': (39.72, 140.1), '山形': (38.24, 140.36), '福島': (37.75, 140.47), '茨城': (36.34, 140.45),
             '栃木': (36.57, 139.88), '群馬': (36.39, 139.06), '埼玉': (35.86, 139.65), '千葉': (35.61, 140.12),
             '東京': (35.69, 139.69), '神奈川': (35.45, 139.64), '新潟': (37.9, 139.02), '富山': (36.7, 137.21),
             '石川': (36.59, 136.63), '福井': (36.07, 136.22), '山梨': (35.66, 138.57), '長野': (36.65, 138.18),
             '岐阜': (35.39, 136.72), '静岡': (34.98, 138.38), '愛知': (35.18, 136.91), '三重': (34.73, 136.51),
             '滋賀': (35.0, 135.87), '京都': (35.02, 135.76), '大阪': (34.69, 135.52), '兵庫': (34.69, 135.18),
             '奈良': (34.69, 135.83), '和歌山': (34.23, 135.17), '鳥取': (35.5, 134.24), '島根': (35.47, 133.05),
             '岡山': (34.66, 133.93), '広島': (34.4, 132.46), '山口': (34.19, 131.47), '徳島': (34.07, 134.56),
             '香川': (34.34, 134.04), '愛媛': (33.84, 132.77), '高知': (33.56, 133.53), '福岡': (33.61, 130.42),
             '佐賀': (33.25, 130.3), '長崎': (32.74, 129.87), '熊本': (32.79, 130.74), '大分': (33.24, 131.61),
             '宮崎': (31.91, 131.42), '鹿児島': (31.56, 130.56), '沖縄': (26.21, 127.68)}

# 日付のリスト
dates = ["今日","明日"]

#　情報種別のリスト
types = ["星座","惑星","伝承"]

# 時間のリスト
times=['17時','18時','19時','20時','21時','22時','23時','24時','5時','6時','7時','8時','9時','10時','11時','12時','0時','1時','2時','3時','4時']

# 時間を数字化するための辞書
times_all={'17時':17,'18時':18,'19時':19,'20時':20,'21時':21,'22時':22,'23時':23,'24時':0,'5時':17,'6時':18,
            '7時':19,'8時':20,'9時':21,'10時':22,'11時':23,'12時':0,'1時':1,'2時':2,'3時':3,'4時':4,'0時':0}

#星座名のリスト
file_path = 'constellations.csv'
data_csv = pd.read_csv(file_path)
names = list(data_csv['name'])

##print(data_csv)

sign_list_url = 'https://livlog.xyz/hoshimiru/constellation'
planet_list_url = 'https://livlog.xyz/hoshimiru/planet'
origin_url = 'https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2021-06-13&hour=20&min=00'


# テキストから時間を抽出する関数．見つからない場合は空文字を返す．
def get_time(text):
    for time in times:
        if time in text:
            return time
    return ""

# テキストから都道府県名を抽出する関数．見つからない場合は空文字を返す．
def get_place(text):
    for pref in prefs:
        if pref in text:
            return pref
    return ""

# テキストに「今日」もしくは「明日」があればそれを返す．見つからない場合は空文字を返す．
def get_date(text):
    if "今日" in text:
        return "今日"
    elif "明日" in text:
        return "明日"
    else:
        return ""

# テキストに「惑星」もしくは「星座」があればそれを返す．見つからない場合は空文字を返す．    
def get_type(text):
    if "星座" in text:
        return "星座"
    elif "惑星" in text:
        return "惑星"
    elif "伝承" in text:
        return "伝承"
    else:
        return ""


#入力から星座とidを取り出す
def get_con(text):
    for con in data_csv['name']:
        if con in text:
            tmp = data_csv[data_csv['name']==con]
            id = int(tmp['con_id'])
            return con,id


#見える星を教える
#星座情報を取得
#今日
def get_sign_list_tod(lat,lon,time):
    # 現在の日時を取得&希望の時間に設定
    today = str(datetime.today()+timedelta(hours=9))
    #日付と時間に分割
    new_date, new_time = today.split()

    min=00
    id=""
    disp="off"

    # 星座情報を取得
    dic= requests.get("{}?lat={}&lng={}&date={}&hour={}&min={}&id={}&disp={}".format(sign_list_url,lat,lon,new_date,time,min,id,disp)).json()
    return dic, new_date

#明日
def get_sign_list_tom(lat,lon,time):
    # 現在の日時を取得&希望の時間に設定
    today = datetime.today()+timedelta(hours=9)

    # 日付を明日に変更
    tomorrow = str(today + timedelta(days=1))
    new_date, new_time = tomorrow.split()

    min=00
    id=""
    disp="off"

    # 星座情報を取得
    dic= requests.get("{}?lat={}&lng={}&date={}&hour={}&min={}&id={}&disp={}".format(sign_list_url,lat,lon,new_date,time,min,id,disp)).json()
    return dic, new_date

#惑星情報を取得
#今日
def get_planet_list_tod(lat,lon,time):
    # 現在の日時を取得&希望の時間に設定
    today = str(datetime.today()+timedelta(hours=9))
    #日付と時間に分割
    new_date, new_time = today.split()

    min=00
    id=""
    disp="off"

    # 星座情報を取得
    dic= requests.get("{}?lat={}&lng={}&date={}&hour={}&min={}&id={}".format(planet_list_url ,lat,lon,new_date,time,min,id)).json()
    return dic, new_date

#明日
def get_planet_list_tom(lat,lon,time):
    # 現在の日時を取得&希望の時間に設定
    today = datetime.today()+timedelta(hours=9)

    # 日付を明日に変更
    tomorrow = str(today + timedelta(days=1))
    new_date, new_time = tomorrow.split()

    min=00
    id=""
    disp="off"

    # 星座情報を取得
    dic= requests.get("{}?lat={}&lng={}&date={}&hour={}&min={}&id={}".format(planet_list_url ,lat,lon,new_date,time,min,id)).json()
    return dic, new_date

#伝承を教える
def get_origin(con_id):
    url = requests.get(f'{origin_url}&id={con_id}&disp=on')
    data = json.loads(url.text)
    data = data["result"]
    print(f"SYS> {con_name}座に関する基本情報をお伝えします！\n")
    content = data[0]["content"]
    c_result = content.split("。")
    for i in range(len(c_result)):
        print(c_result[i])
        # print(c_result[i]+'。')
    print(f"\nSYS> {con_name}座に関する伝承をお伝えします！\n")
    origin = data[0]["origin"]
    print(origin)

'''文章の表示方法の変更
    o_result = origin.split("。")
    for i in range(len(o_result)):
        print(o_result[i]+'。')
'''



# 発話から得られた情報をもとにフレームを更新
def update_frame(frame, da, conceptdic):
    # 値の整合性を確認し，整合しないものは空文字にする
    for k,v in conceptdic.items():
        if k == "place" and v not in prefs:
            conceptdic[k] = ""
        elif k == "date" and v not in dates:
            conceptdic[k] = ""
        elif k == "time" and v not in times:
            conceptdic[k] = ""
        elif k == "type" and v not in types:
            conceptdic[k] = ""
    if da == "request-star":
        for k,v in conceptdic.items():
            # コンセプトの情報でスロットを埋める
            frame[k] = v

    if da == "request-stargazing":
        for k,v in conceptdic.items():
            # コンセプトの情報でスロットを埋める
            # 伝承が来たら特定のスロットを埋めてしまう
            if v == '伝承':
                frame["place"] = "東京"
                frame["date"] = "2021-06-13"
            frame[k] = v
            
    elif da == "initialize":
        frame = {"place": "", "date": "", "time":"", "type": "", "star": ""}
    elif da == "correct-info":
        for k,v in conceptdic.items():
            if frame[k] == v:
                frame[k] = ""
    return frame

# フレームの状態から次のシステム対話行為を決定
def next_system_da(frame):
    # すべてのスロットが空であればオープンな質問を行う
    if frame["place"] == "" and frame["date"] == "" and frame["time"] == "" and frame["type"] == "" and frame["name"] == "":
        return "open-prompt"
    # 空のスロットがあればその要素を質問する
    elif frame["type"] == "":
        return "ask-type"
    elif frame["type"] == "伝承":
        if frame["name"] == "":
            return "ask-name"
        else:
            return "tell-info"
    elif frame["type"] == "星座" or frame["type"] == "惑星":
        if frame["place"] == "":
            return "ask-place"
        elif frame["date"] == "":
            return "ask-date"
        elif frame["time"] == "":
            return "ask-time"
        else:
            return "tell-info"
    else :
        return "tell-info"

# 対話行為タイプとコンセプトの推定器
da_concept = DA_Concept()  

# フレーム
frame = {"place": "", "date": "", "time": "", "type": "", "name": ""} 


# システムプロンプト
print("SYS> 星について学ぼう！")
print("SYS> 見える星座や惑星を知りたい？ 伝承を知りたい？")


# 状態とシステム発話を紐づけた辞書
uttdic = {"open-prompt": "見える星座や惑星を知りたい？ 伝承を知りたい？",
          "ask-type": "情報種別を言ってね",
          "ask-place": "地名を言ってね",
          "ask-date": "日付を言ってね",
          "ask-time": "時間を言ってね",
          "ask-name": "星座の名前を言ってね"
}


# ユーザ入力の処理
while True:
    text = input("> ")

    # 現在のフレームを表示
    print("frame=", frame)

    # 手入力で対話行為タイプとコンセプトを入力していた箇所を
    # 自動推定するように変更
    da, conceptdic = da_concept.process(text)        
    print(da, conceptdic)

    # 対話行為タイプとコンセプトを用いてフレームを更新
    frame = update_frame(frame, da, conceptdic)

    # 更新後のフレームを表示    
    print("updated frame=", frame)    

    # フレームからシステム対話行為を得る   
    sys_da = next_system_da(frame)

     # 遷移先がtell-infoの場合は情報を伝えて終了
    if sys_da == "tell-info":

        place = frame["place"]
        date = frame["date"]
        time = frame["time"]
        _type = frame["type"]
        


        if _type == "星座":
            lat = latlondic[place][0] # placeから緯度を取得
            lon = latlondic[place][1] # placeから経度を取得
            clock=times_all[time] #timeを数字のみ&17時〜4時に変換

            print("lat=",lat,"lon=",lon)
            
            if date=="今日":
                cw, new_date = get_sign_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_sign_list_tom(lat,lon,clock)
            
            print("{} {}時の{}では以下の{}が見えるよ！".format(new_date, clock, place,_type))
            for i in range(len(cw["result"])):
                if cw["result"][i]["altitude"]!="水平線の下":
                    print("{}->方角:{}　高度：{}".format(cw["result"][i]["jpName"],cw["result"][i]["direction"],cw["result"][i]["altitude"]))

        elif _type == "惑星":
            lat = latlondic[place][0] # placeから緯度を取得
            lon = latlondic[place][1] # placeから経度を取得
            clock=times_all[time] #timeを数字のみ&17時〜4時に変換

            print("lat=",lat,"lon=",lon)

            if date=="今日":
                cw, new_date = get_planet_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_planet_list_tom(lat,lon,clock)

            print("{} {}時の{}では以下の{}が見えるよ！".format(new_date, clock, place,_type))
            for i in range(len(cw["result"])):
                if cw["result"][i]["altitude"]!="水平線の下":
                    print("{}->方角:{}　高度：{}".format(cw["result"][i]["jpName"],cw["result"][i]["direction"],cw["result"][i]["altitude"]))


        
        if _type == "伝承":
            print("SYS> 星の伝承についてお伝えします！")

            con_name,con_id = get_con(text)
            ##print(f"{origin_url}&id={con_id}&disp=on")
            print("SYS> id=",con_id)
            get_origin(con_id)
        break

    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[sys_da]

        print("SYS>", sysutt)       

# 終了発話
print("ご利用ありがとうございました！")       


# end of file
