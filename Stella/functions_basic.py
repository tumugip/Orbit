from datetime import datetime, timedelta, time
import requests, json
import pandas as pd

# 都道府県名のリスト
prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']


# 日付のリスト
dates = ["今日","明日"]

#　情報種別のリスト
types = ["星座","惑星","伝承"]

# 時間のリスト
times=['17時','18時','19時','20時','21時','22時','23時','24時','5時','6時','7時','8時','9時','10時','11時','12時','0時','1時','2時','3時','4時']

#星座名のリスト
file_path = 'constellations.csv'
data_csv = pd.read_csv(file_path)
names = list(data_csv['name'])   

sign_list_url = 'https://livlog.xyz/hoshimiru/constellation'
planet_list_url = 'https://livlog.xyz/hoshimiru/planet'
origin_url = 'https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2021-06-13&hour=20&min=00'


# ---------------------------------------------------------------
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
def get_origin(con_id,con_name):
    url = requests.get(f'{origin_url}&id={con_id}&disp=on')
    data = json.loads(url.text)
    data = data["result"]
    con = con_name + "座に関する基本情報を伝えるゾ！"
    content = data[0]["content"]
    ori = con_name + "座に関する伝承を伝えるゾ！"
    origin = data[0]["origin"]

    return con, content, ori, origin


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
