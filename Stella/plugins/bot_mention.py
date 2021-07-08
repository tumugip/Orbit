from slackbot.bot import respond_to     
from slackbot.bot import listen_to      
from slackbot.bot import default_reply 
import json

from comb_da_concept_extractor import DA_Concept
from functions_basic import get_con, get_origin, update_frame, next_system_da
from functions_basic import get_sign_list_tod, get_sign_list_tom, get_planet_list_tod, get_planet_list_tom


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

# 状態とシステム発話を紐づけた辞書
uttdic = {"open-prompt": "見える星座や惑星を知りたい？ 伝承を知りたい？",
          "ask-type": "情報種別を言うんだゾ",
          "ask-place": "地名を言うんだゾ",
          "ask-date": "日付を言うんだゾ",
          "ask-time": "時間を言うんだゾ",
          "ask-name": "星座の名前を言うんだゾ"
}

# 時間を数字化するための辞書
times_all={'17時':17,'18時':18,'19時':19,'20時':20,'21時':21,'22時':22,'23時':23,'24時':0,'5時':17,'6時':18,
            '7時':19,'8時':20,'9時':21,'10時':22,'11時':23,'12時':0,'1時':1,'2時':2,'3時':3,'4時':4,'0時':0}

# 対話行為タイプとコンセプトの推定器
da_concept = DA_Concept()         
# フレーム
frame = {"place": "", "date": "", "time": "", "type": "", "name": ""}

#起動直後のみのメッセージを表示させる
cnt = 0 

@respond_to('(.*)')
def tell_comb(message,something):

    global cnt, frame

    if cnt == 0:
        message.send('星について教えるゾ！')
        sysutt = uttdic["open-prompt"]
        #message.send(sysutt)
        cnt = 1    



    da, conceptdic = da_concept.process(something)          

    # 対話行為タイプとコンセプトを用いてフレームを更新
    frame = update_frame(frame, da, conceptdic)

    # 更新後のフレームを表示    
    print("updated frame=", frame)    

    # フレームからシステム対話行為を得る   
    sys_da = next_system_da(frame)

    # 遷移先がtell_infoの場合は情報を伝えて終了
    if sys_da == "tell-info":
        message.send('星について教えるゾ！')

        place = frame["place"]
        date = frame["date"]
        time = frame["time"]
        _type = frame["type"]

        if _type == "星座":
            lat = latlondic[place][0] # placeから緯度を取得
            lon = latlondic[place][1] # placeから経度を取得
            clock=times_all[time] #timeを数字のみ&17時〜4時に変換
            
            if date=="今日":
                cw, new_date = get_sign_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_sign_list_tom(lat,lon,clock)
            
            message.send("{} {}時の{}では以下の{}がが見えるゾ！".format(new_date, clock, place,_type))
            for i in range(len(cw["result"])):
                if cw["result"][i]["altitude"]!="水平線の下":
                    attachments=[
                        {
                            'color':"#5980C0",
                            'fields':[
                                {'title':"方角", 'value':cw["result"][i]["direction"], 'short':True},
                                {'title':"高度", 'value':cw["result"][i]["altitude"], 'short':True}
                            ]
                        }
                    ]
                    message.send_webapi(cw["result"][i]["jpName"], json.dumps(attachments))

        elif _type == "惑星":
            
            lat = latlondic[place][0] # placeから緯度を取得
            lon = latlondic[place][1] # placeから経度を取得
            clock=times_all[time] #timeを数字のみ&17時〜4時に変換

            if date=="今日":
                cw, new_date = get_planet_list_tod(lat,lon,clock)
            elif date=="明日":
                cw, new_date = get_planet_list_tom(lat,lon,clock)

            message.send("{} {}時の{}では以下の{}が見えるゾ！".format(new_date, clock, place,_type))
            for i in range(len(cw["result"])):                
                if cw["result"][i]["altitude"]!="水平線の下":
                    
                    attachments=[
                        {
                            'color':"#5980C0",
                            'fields':[
                                {'title':"方角", 'value':cw["result"][i]["direction"], 'short':True},
                                {'title':"高度", 'value':cw["result"][i]["altitude"], 'short':True}
                            ]
                        }
                    ]
                    message.send_webapi(cw["result"][i]["jpName"], json.dumps(attachments))

        elif _type == "伝承":
            con_name,con_id = get_con(something)
            con, content, ori, origin = get_origin(con_id,con_name)
            attachments=[
                {
                    'color':"#5980C0",
                    'fields':[
                        {'title':"基本情報", 'value':content},
                        {'title':"　", 'value':"" },
                        {'title':"伝承", 'value':origin}
                    ]
                }
            ]            
            message.send_webapi("{}座".format(con_name), json.dumps(attachments))
        
        message.send('以上だゾ！\nご利用、ありがとござます〜！')
        # フレームとカウントの初期化
        frame = {"place": "", "date": "", "time": "", "type": "", "name": ""}
        cnt = 0



    else:
        # 対話行為に紐づいたテンプレートを用いてシステム発話を生成
        sysutt = uttdic[sys_da]
        message.send(sysutt) 


# # デコレータで入力内容のメンションがbotに飛ばされた際の反応を設定
# # 絵文字での反応も
# @respond_to('可愛い')
# def mention_func1(message):
#     message.send('知ってる') 
#     message.react('+1')
#     message.react('triumph')

