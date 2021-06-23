# フレーム完成形のコード
from datetime import datetime, timedelta, time
from da_concept_extractor import DA_Concept
import requests, json
import pandas as pd

#星座名のリスト
file_path = 'constellations.csv'
data_csv = pd.read_csv(file_path)
names = list(data_csv['name'])

# 都道府県名のリスト
prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

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
dates = ['2021-06-13']

# 情報種別のリスト
types = ['一覧','伝承']    

# システムの対話行為タイプとシステム発話を紐づけた辞書
uttdic = {
            "open-prompt": "何が見えるか知りたい？伝承を知りたい？",
            "ask-type": "情報種別を言ってください",
            "ask-place": "地名を言ってください",
            "ask-date": "日付を言ってください",
            "ask-name": "星座の名前を言ってください"
        }

origin_url = 'https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2021-06-13&hour=20&min=00'

#入力から星座とidを取り出す
def get_con(text):
    for con in data_csv['name']:
        if con in text:
            tmp = data_csv[data_csv['name']==con]
            id = int(tmp['con_id'])
            return con,id

def get_origin(con_id):
    url = requests.get(f'{origin_url}&id={con_id}&disp=on')
    data = json.loads(url.text)
    data = data["result"]
    print(f"SYS> {con_name}座に関する基本情報をお伝えします\n")
    content = data[0]["content"]
    c_result = content.split("。")
    for i in range(len(c_result)):
        print(c_result[i])
        # print(c_result[i]+'。')
    print(f"\nSYS> {con_name}座Sに関する伝承をお伝えします\n")
    origin = data[0]["origin"]
    print(origin)
    # o_result = origin.split("。")
    # for i in range(len(o_result)):
    #     print(o_result[i]+'。')

# 発話から得られた情報をもとにフレームを更新
def update_frame(frame, da, conceptdic):
    # 値の整合性を確認し，整合しないものは空文字にする
    for k,v in conceptdic.items():
        if k == "place" and v not in prefs:
            conceptdic[k] = ""
        elif k == "date" and v not in dates:
            conceptdic[k] = ""
        elif k == "type" and v not in types:
            conceptdic[k] = ""
        elif k == "name" and v not in names:
            conceptdic[k] = ""
    if da == "request-stargazing":
        for k,v in conceptdic.items():
            # コンセプトの情報でスロットを埋める
            # 伝承が来たら特定のスロットを埋めてしまう
            if v == '伝承':
                frame["place"] = "東京"
                frame["date"] = "2021-06-13"
            frame[k] = v
            
    elif da == "initialize":
        frame = {"place": "", "date": "", "type": "", "name": ""}
    elif da == "correct-info":
        for k,v in conceptdic.items():
            # 伝承が来たら特定のスロットを空にする
            if v == '伝承':
                frame["place"] = ""
                frame["date"] = ""
            if frame[k] == v:
                frame[k] = ""
    return frame

# フレームの状態から次のシステム対話行為を決定
def next_system_da(frame):
    # すべてのスロットが空であればオープンな質問を行う
    if frame["place"] == "" and frame["date"] == "" and frame["type"] == "" and frame["name"] == "":
        return "open-prompt"
    # 空のスロットがあればその要素を質問する
    elif frame["place"] == "":
        return "ask-place"
    elif frame["date"] == "":
        return "ask-date"
    elif frame["type"] == "":
        return "ask-type"
    elif frame["name"] == "":
        return "ask-name"
    else:
        return "tell-info"

# 対話行為タイプとコンセプトの推定器
da_concept = DA_Concept()    

# フレーム
frame = {"place": "", "date": "", "type": "", "name": ""}      

# システムプロンプト
print("SYS> 星をみよう(^^)")
print("SYS> 何が見えるか知りたい？伝承を知りたい？")    

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

    # 遷移先がtell_infoの場合は情報を伝えて終了
    if sys_da == "tell-info":
        print("SYS> 星についてお伝えします")
        if frame["type"] == "伝承":
            con_name,con_id = get_con(text)
            print(f"{origin_url}&id={con_id}&disp=on")
            print("SYS> id=",con_id)
            get_origin(con_id)
        break
    else:
        # 対話行為に紐づいたテンプレートを用いてシステム発話を生成
        sysutt = uttdic[sys_da]
        print("SYS>", sysutt)      

# 終了発話
print("\nSYS> ご利用ありがとうございました") 