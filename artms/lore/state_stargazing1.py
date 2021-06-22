# 状態遷移完成形のコード
import sys
from PySide2 import QtCore, QtScxml
import json, requests
from datetime import datetime,timedelta,time
import pandas as pd

stargazing_url = 'https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2021-06-13&hour=20&min=00'
# season_url = 'https://livlog.xyz/hoshimiru/constellation?lat=35.6581&lng=139.7414&date=2021-06-13&hour=20&min=00'

#星座の一覧表を取ってくる
file_path = 'constellations.csv'
data_csv = pd.read_csv(file_path)

#入力から星座とidを取り出す
def get_con(text):
    for con in data_csv['name']:
        if con in text:
            tmp = data_csv[data_csv['name']==con]
            id = int(tmp['con_id'])
            return con,id

def get_origin(con_id):
    url = requests.get(f'{stargazing_url}&id={con_id}&disp=on')
    data = json.loads(url.text)
    data = data["result"]
    print(f"SYS> {con_name}に関する基本情報をお伝えします\n")
    content = data[0]["content"]
    c_result = content.split("。")
    for i in range(len(c_result)):
      print(c_result[i]+'。')
    print(f"\nSYS> {con_name}に関する伝承をお伝えします\n")
    origin = data[0]["origin"]
    o_result = origin.split("。")
    for i in range(len(o_result)):
      print(o_result[i]+'。')


app = QtCore.QCoreApplication()
el = QtCore.QEventLoop()

sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

sm.start()
el.processEvents()

print("SYS> こちらは星座の基本情報や伝承をお伝えするサービスです")

uttdic = {"ask_con":"星座名を言ってください"}

current_state = sm.activeStateNames()[0]
print("current_state=",current_state)

sysutt = uttdic[current_state]
print("SYS>",sysutt)

while True:
    text = input("> ")
    if current_state == "ask_con":
        con_name,con_id = get_con(text)
        if con_name != "":
            sm.submitEvent("con_name")
            el.processEvents()

    current_state = sm.activeStateNames()[0]
    print("current_state=",current_state)

    if current_state == "tell_origin":
        # print(f"SYS> {con_name}に関する情報をお伝えします")
        print(f"{stargazing_url}&id={con_id}&disp=on")
        print("SYS> id=",con_id)
        get_origin(con_id)
        
        break

    else:
        sysutt = uttdic[current_state]
        print("SYS>",sysutt)


print("\nSYS> ご利用ありがとうございました")