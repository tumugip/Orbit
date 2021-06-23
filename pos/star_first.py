import sys
from PySide2 import QtCore, QtScxml
import requests
import json
from datetime import datetime, timedelta, time

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

# 星座名のリスト
sign = ['アンドロメダ', 'ポンプ', 'ふうちょう', 'わし', 'みずがめ', 'さいだん', 'おひつじ', 'ぎょしゃ', 'うしかい',
         'ちょうこくぐ', 'きりん', 'やぎ', 'りゅうこつ', 'カシオペヤ', 'ケンタウルス', 'ケフェウス', 'くじら',
         'カメレオン', 'コンパス','おおいぬ', 'こいぬ', 'かに', 'はと', 'かみのけ', 'みなみのかんむり','かんむり', 'コップ',
         'みなみじゅうじ', 'からす', 'りょうけん', 'はくちょう', 'いるか', 'かじき', 'りゅう', 'こうま', 'エリダヌス',
         'ろ', 'ふたご', 'つる', 'ヘルクレス', 'とけい', 'うみへび', 'みずへび', 'インディアン', 'とかげ', 'しし', 
         'うさぎ', 'てんびん', 'こじし', 'おおかみ', 'やまねこ', 'こと', 'テーブルさん', 'けんびきょう', 'いっかくじゅう',
         'はえ', 'じょうぎ', 'はちぶんぎ', 'へびつかい', 'オリオン', 'くじゃく', 'ペガスス', 'ペルセウス', 'ほうおう', 'がか',
         'みなみのうお', 'うお', 'とも', 'らしんばん', 'レチクル', 'ちょうこくしつ', 'さそり', 'たて', 'へび', 'ろくぶんぎ',
         'や', 'いて', 'おうし', 'ぼうえんきょう', 'みなみのさんかく','さんかく', 'きょしちょう', 'おおぐま', 'こぐま', 'ほ', 'おとめ', 'とびうお',
         'こぎつね'
         ]

#星座名からIDを取得するための辞書
sign_id = {'アンドロメダ':1, 'ポンプ':2, 'ふうちょう':3, 'わし':4, 'みずがめ':5, 'さいだん':6, 'おひつじ':7, 'ぎょしゃ':8, 'うしかい':9,
         'ちょうこくぐ':10, 'きりん':11, 'やぎ':12, 'りゅうこつ':13, 'カシオペヤ':14, 'ケンタウルス':15, 'ケフェウス':16, 'くじら':17,
         'カメレオン':18, 'コンパス':19,'おおいぬ':20, 'こいぬ':21, 'かに':22, 'はと':23, 'かみのけ':24, 'みなみのかんむり':25, 'かんむり':26, 'コップ':27,
         'みなみじゅうじ':28, 'からす':29, 'りょうけん':30, 'はくちょう':31, 'いるか':32, 'かじき':33, 'りゅう':34, 'こうま':35, 'エリダヌス':36,
         'ろ':37, 'ふたご':38, 'つる':39, 'ヘルクレス':40, 'とけい':41, 'うみへび':42, 'みずへび':43, 'インディアン':44, 'とかげ':45, 'しし':46, 
         'うさぎ':47, 'てんびん':48, 'こじし':49, 'おおかみ':50, 'やまねこ':51, 'こと':52, 'テーブルさん':53, 'けんびきょう':54, 'いっかくじゅう':55,
         'はえ':56, 'じょうぎ':57, 'はちぶんぎ':58, 'へびつかい':59, 'オリオン':60, 'くじゃく':61, 'ペガスス':62, 'ペルセウス':63, 'ほうおう':64, 'がか':65,
         'みなみのうお':66, 'うお':67, 'とも':68, 'らしんばん':69, 'レチクル':70, 'ちょうこくしつ':71, 'さそり':72, 'たて':73, 'へび':74, 'ろくぶんぎ':75,
         'や':76, 'いて':77, 'おうし':78, 'ぼうえんきょう':79, 'みなみのさんかく':80, 'さんかく':81, 'きょしちょう':82, 'おおぐま':83, 'こぐま':84, 'ほ':85, 'おとめ':86, 'とびうお':87,
         'こぎつね':88
         }

# 惑星名のリスト
planet =['太陽','水星','金星','月','火星','木星','土星','天王星','海王星','冥王星']

# 惑星名からIDを取得するための辞書
planet_id ={'太陽':101,'水星':102,'金星':103,'月':106,'火星':107,'木星':108,'土星':109,'天王星':110,'海王星':111,'冥王星':112}


# 時間のリスト
times=['17時','18時','19時','20時','21時','22時','23時','24時','5時','6時','7時','8時','9時','10時','11時','12時','0時','1時','2時','3時','4時']

# 時間を数字化するための辞書
times_all={'17時':17,'18時':18,'19時':19,'20時':20,'21時':21,'22時':22,'23時':23,'24時':0,'5時':17,'6時':18,
            '7時':19,'8時':20,'9時':21,'10時':22,'11時':23,'12時':0,'1時':1,'2時':2,'3時':3,'4時':4,'0時':0}


sign_list_url = 'https://livlog.xyz/hoshimiru/constellation'
planet_list_url = 'https://livlog.xyz/hoshimiru/planet'

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
    else:
        return ""

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

# Qtに関するおまじない
app = QtCore.QCoreApplication()
el  = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm  = QtScxml.QScxmlStateMachine.fromFile('star_states.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> こちらは星の案内システムです")

# 状態とシステム発話を紐づけた辞書
uttdic = {"ask_place": "地名を言ってください",
          "ask_date": "日付を言ってください",
          "ask_time": "時間を言ってください",
          "ask_type": "情報種別を言ってください"}

# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)

# ユーザ入力の処理
while True:
    text = input("> ")

    # ユーザ入力を用いて状態遷移
    if current_state == "ask_place":
        place = get_place(text)
        if place != "":
            sm.submitEvent("place")
            el.processEvents()
    elif current_state == "ask_date":
        date = get_date(text)
        if date != "":
            sm.submitEvent("date")
            el.processEvents()                   
    elif current_state == "ask_time":
        time = get_time(text)
        if time != "":
            sm.submitEvent("time")
            el.processEvents() 
    elif current_state == "ask_type":
        _type = get_type(text)
        if _type != "":
            sm.submitEvent("type")
            el.processEvents()                   

    # 遷移先の状態を取得
    current_state = sm.activeStateNames()[0]
    print("current_state=", current_state)

          
    # 遷移先がtell_infoの場合は情報を伝えて終了
    if current_state == "tell_info":
 #       clock=get_time(time)
 #       print("{}{}時の{}では以下の星が見えます".format(date, clock, place))
        lat = latlondic[place][0] # placeから緯度を取得
        lon = latlondic[place][1] # placeから経度を取得
        clock=times_all[time] #timeを数字のみ&17時〜4時に変換


        print("lat=",lat,"lon=",lon)
        if _type == "星座":
            if date=="今日":
                cw, new_date = get_sign_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_sign_list_tom(lat,lon,clock)
            

        elif _type == "惑星":
            if date=="今日":
                cw, new_date = get_planet_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_planet_list_tom(lat,lon,clock)

        print("{} {}時の{}では以下の星が見えます".format(new_date, clock, place))

        for i in range(len(cw["result"])):
            if cw["result"][i]["altitude"]!="水平線の下":
                print("{}->方角:{}　高度：{}".format(cw["result"][i]["jpName"],cw["result"][i]["direction"],cw["result"][i]["altitude"]))

        break
    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[current_state]
        print("SYS>", sysutt) 

# 終了発話
print("ご利用ありがとうございました")       

# end of file
