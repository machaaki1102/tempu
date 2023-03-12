import streamlit as st
import re
import pandas as pd
import datetime
import calendar
import requests
import numpy as np
#from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

#prec_noとblock_no含んだ『県マスター』が出来る
# データを読み込む
df = pd.read_csv("kishou.txt", header=None,skiprows=1,sep="\s*,\s*", engine="python")
df_sub = df.iloc[:,[0,1,2,3,4,10]] 
df_sub.columns = ["No.", "i", "地点名", "prec_no", "block_no","県"]

#block_noの前に数字を埋めて4桁にする
df_sub["block_no"] = df_sub["block_no"].astype(str)

for a in range(len(df_sub)):
    num_str = df_sub["block_no"][a]
    if len(num_str) == 4 and len(num_str) == 5:
    #4桁でも5桁でもない場合の処理
        continue
    else:
        df_sub['block_no'][a]= "{:0>4}".format(num_str)

st.dataframe(df_sub)

#何か月違いか
def month_difference(date1,date2):
    months = (date2.year - date1.year) * 12 + date2.month - date1.month
    return months

#年・月を選び、月の日付のリストを作る。
def date_lists(year,month):
      year = year
      month = month

      date_list = []
      first_day = datetime.date(year, month, 1)
      _, last_day = calendar.monthrange(year, month)

      for day in range(1, last_day+1):
          date_list.append(datetime.date(year, month, day))
          #date_str_list = [date.strftime('%Y-%m-%d') for date in date_list]
      return date_list

#平均気温と日照時間のデータフレームを作る。
def total_tem(year,month,day):
    url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day={day}&view='
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # findAllで条件に一致するものをすべて抜き出します。
    rows = soup.findAll('tr',class_='mtx')
    #データだけを抜き出す
    rows = rows[4:]

    #All_list = [['陸の平均気圧(hPa)', '海の平均気圧(hPa)', '降水量(mm)', '平均気温(℃)', '平均湿度(%)', '平均風速(m/s)', '日照時間(h)']]
    All_list = [['平均気温(℃)','日照時間(h)']]

    for row in rows:
            # 今trのなかのtdをすべて抜き出します
            data = row.findAll('td')

              #１行の中には様々なデータがあるので全部取り出す。
              # ★ポイント
            rowData = [] #初期化
    #         rowData.append(float(data[1].string))
    #         rowData.append(float(data[2].string))
    #         rowData.append(float(data[3].string))
    #前回       rowData.append(float(data[6].string.replace(")", "")))
            rowData.append(float(data[6].string.replace(")", "").replace(" ", "").replace("]", "")))
    #        rowData.append(float(data[9].string))
    #        rowData.append(float(data[11].string))
    #確認用
    #        print(type(data[16]))
    #        print(type(data[16].string))
    #        print(type(float(data[16].string.replace(")", ""))))
            rowData.append(float(data[16].string.replace(")", "").replace(" ", "").replace("]", "")))
    #前回        rowData.append(float(data[16].string.replace(")", "")))

              #次の行にデータを追加
            All_list.append(rowData)
            
    data = All_list[1:]
    columns = All_list[0]
    df = pd.DataFrame(data,columns=columns)
    
    #Indexを1からふり直す
    df['日付'] = date_list
    return df

#日付を足す    
def df_add(date_new):
    date_new = date_new + relativedelta(months=1)
    year = date_new.year
    month =  date_new.month
    return date_new,year,month

#body　データの日付の入力
start = st.date_input("開始日を選択してください", value=datetime.date(2022, 1, 5))
finish = st.date_input("終了日を選択してください", value=datetime.date(2022, 8, 3))

