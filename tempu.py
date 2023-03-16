import streamlit as st
import re
import pandas as pd
import datetime
import calendar
import requests
import numpy as np
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import base64
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


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

    #All_list = [['陸の平均気圧(hPa)', '海の平均気圧(hPa)', '降水量(mm)',最低気温(℃) '平均気温(℃)', '平均湿度(%)', '平均風速(m/s)', '日照時間(h)']]
    All_list = [['平均気温(℃)','日照時間(h)','降水量(mm)','最高気温(℃)','最低気温(℃)']]

    for row in rows:
            # 今trのなかのtdをすべて抜き出します
            data = row.findAll('td')
            #追加
            #st.write(data)

              #１行の中には様々なデータがあるので全部取り出す。
              # ★ポイント
            rowData = [] #初期化
    #         rowData.append(float(data[1].string))
    #         rowData.append(float(data[2].string))
    #         rowData.append(float(data[3].string))
    #前回       rowData.append(float(data[6].string.replace(")", "")))
      
            rowData.append(float(data[6].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[16].string.replace(")", "").replace(" ", "").replace("]", "")))
            #追加
            if  '--' in data[3].string:
            #if data[3].string == '--':
                #rowData.append(np.nan)
                rowData.append(0)
            else:
                rowData.append(float(data[3].string.replace(")", "").replace(" ", "").replace("]", "")))

            #rowData.append(float(data[3].string.replace(")", "").replace(" ", "").replace("]", "").replace("'--'","")))
            rowData.append(float(data[7].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[8].string.replace(")", "").replace(" ", "").replace("]", "")))
    #  rowData.append(float(data[9].string))
    #        rowData.append(float(data[11].string))
    #確認用
    #        print(type(data[16]))
    #        print(type(data[16].string))
    #        print(type(float(data[16].string.replace(")", ""))))
            #rowData.append(float(data[16].string.replace(")", "").replace(" ", "").replace("]", "")))
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
#prec_noとblock_no含んだ『県マスター』が出来る
## データを読み込む
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


#st.set_page_config(page_title="<title>栽培期間中の気温/降水量/日射量(気象庁データ)</title>",layout="wide",unsafe_allow_html=True)
st.set_page_config(page_title="気象データ",layout="wide")
st.title("栽培期間中の気温/降水量/日射量(気象庁データ)", style={"font-size": "24px"})

# 3つの列を作成
col1, col2, col3 = st.columns(3)
# 各列にselectboxを追加
with col1:
    ken =st.selectbox('県を選んでください',df_sub['県'].unique())
with col2:
    start = st.date_input("開始日を選択してください", value=datetime.date(2022, 5, 5))
with col3:
    finish = st.date_input("終了日を選択してください", value=datetime.date(2022, 10, 3))

#ken =st.selectbox('県を選んでください',df_sub['県'].unique())
#start = st.date_input("開始日を選択してください", value=datetime.date(2022, 1, 5))
#finish = st.date_input("終了日を選択してください", value=datetime.date(2022, 8, 3))

year = start.year
month = start.month
day = start.day
#気象庁の県コード及び地域コードを入れる
#prec_no = 57
#block_no = 47616
prec_no,block_no = df_sub.loc[df_sub['県'] == ken, ['prec_no','block_no']].values[0]
block_no = int(block_no)
#st.write(type(prec_no))
#st.write(type(block_no))

#body 
date_new = start
months = month_difference(start,finish)#月を計算
date_list = date_lists(year,month)
df = total_tem(year,month,day)

#monthの期間分足す。
while months >0:
    date_new,year,month = df_add(date_new) 
    date_list = date_lists(year,month)
    df = pd.concat([df,total_tem(year,month,1)],axis=0) 
    months = months -1
#日付をオブジェクトから日数にする 
df["日付"] = pd.to_datetime(df["日付"], format="%Y-%m-%d")
#期間を絞る。
df = df.query(f"'{start}' <= 日付 <= '{finish}'")
#df["日付"] = df["日付"].dt.strftime("%Y-%m-%d"
df = df.reset_index()
df = df.drop("index", axis=1)
df = df.reindex(columns=["日付", "平均気温(℃)","最高気温(℃)","最低気温(℃)","降水量(mm)","日照時間(h)"])
#df

#1年前のデータフレームを作成
start_ago = datetime.date(start.year -1 , start.month, start.day)#date_agoが前回のstart
finish_ago = datetime.date(finish.year -1, finish.month, finish.day)#finishの1年前

year_ago = start_ago.year
#month = date_ago.month
#day = date_ago.day

date_new = start_ago
months = month_difference(start_ago,finish_ago)
date_list = date_lists(start_ago.year,start_ago.month)
df_ago = total_tem(start_ago.year,start_ago.month,start_ago.day)

#st.write(months)
#monthの期間分足す。
while months >0:
    date_new,year,month = df_add(date_new) 
    date_list = date_lists(year,month)
    df_ago = pd.concat([df_ago,total_tem(year,month,1)],axis=0) 
    months = months -1
#日付をオブジェクトから日数にする 
df_ago["日付"] = pd.to_datetime(df_ago["日付"], format="%Y-%m-%d")
df_ago = df_ago.reset_index()
df_ago = df_ago.drop("index", axis=1)
df_ago = df_ago.reindex(columns=["日付", "平均気温(℃)","最高気温(℃)","最低気温(℃)","降水量(mm)","日照時間(h)"])
#期間を絞る。
df_ago = df_ago.query(f"'{start_ago}' <= 日付 <= '{finish_ago}'")
#df_ago

#設定のグラフ
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
#"日付", "平均気温(℃)","最高気温(℃)","最低気温(℃)","降水量(mm)","日照時間(h)"]
fig2.add_trace(go.Scatter(x=df["日付"], y=df["平均気温(℃)"], name="平均気温(℃)", line=dict(color='green')))
fig2.add_trace(go.Scatter(x=df["日付"], y=df["最高気温(℃)"], name="最高気温(℃)", line=dict(color='red')))
fig2.add_trace(go.Scatter(x=df["日付"], y=df["最低気温(℃)"], name="最低気温(℃)", line=dict(color='blue')))

fig2.add_trace(go.Bar(x=df["日付"], y=df["降水量(mm)"], name="降水量(mm)", marker_color='gray'), secondary_y=True)
fig2.add_trace(go.Bar(x=df["日付"], y=df["日照時間(h)"], name="日照時間(h)", marker_color='orange'), secondary_y=True)

# 1つめのy軸の範囲設定
fig2.update_yaxes(range=[-20, 40], title_text="気温(℃)", secondary_y=False)
# 2つめのy軸の範囲設定
fig2.update_yaxes(range=[0, 100], title_text="降水量(mm)", secondary_y=True)
fig2.update_layout(title="今回の天候")    
#st.plotly_chart(fig2)

#1年分のグラフ
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
#"日付", "平均気温(℃)","最高気温(℃)","最低気温(℃)","降水量(mm)","日照時間(h)"]
fig3.add_trace(go.Scatter(x=df_ago["日付"], y=df_ago["平均気温(℃)"], name="平均気温(℃)", line=dict(color='green')))
fig3.add_trace(go.Scatter(x=df_ago["日付"], y=df_ago["最高気温(℃)"], name="最高気温(℃)", line=dict(color='red')))
fig3.add_trace(go.Scatter(x=df_ago["日付"], y=df_ago["最低気温(℃)"], name="最低気温(℃)", line=dict(color='blue')))
#棒グラフ
fig3.add_trace(go.Bar(x=df_ago["日付"], y=df_ago["降水量(mm)"], name="降水量(mm)", marker_color='gray'), secondary_y=True)
fig3.add_trace(go.Bar(x=df_ago["日付"], y=df_ago["日照時間(h)"], name="日照時間(h)", marker_color='orange'), secondary_y=True)

# 1つめのy軸の範囲設定
fig3.update_yaxes(range=[-20, 40], title_text="気温(℃)", secondary_y=False)
# 2つめのy軸の範囲設定
fig3.update_yaxes(range=[0, 100], title_text="降水量(mm)", secondary_y=True)
fig3.update_layout(title="1年前の天候")    

#差分を出す
df_dif = df_ago[["平均気温(℃)","降水量(mm)","日照時間(h)"]] - df[["平均気温(℃)","降水量(mm)","日照時間(h)"]]

df_dif['日付'] = df["日付"]
#df_dif

# グラフを作成します
fig = go.Figure()
# 差分の折れ線グラフを追加します
fig.add_trace(go.Scatter(x=df_dif["日付"], y=df_dif["平均気温(℃)"], mode="lines", name="差分"))
# 積み上げ値の折れ線グラフを追加します
fig.add_trace(go.Scatter(x=df_dif["日付"], y=df_dif["平均気温(℃)"].cumsum(), mode="lines", name="積み上げ"))

# X軸を日付として設定します
fig.update_xaxes(type='date', tickformat='%Y-%m-%d', title="日付")
fig.update_layout(title="気温差")

#st.plotly_chart(fig)

#========
col1, col2 = st.columns(2)

# 各列にselectboxを追加
col1, col2 = st.columns(2)

# 各列にselectboxを追加
with col1:
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

# 各列にselectboxを追加
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    df


#with col1:
#    st.plotly_chart(fig2)
    #df
#with col2:
#    st.plotly_chart(fig3)
    #start = st.date_input("開始日を選択してください", value=datetime.date(2022, 1, 5))
#with col3:
#    st.plotly_chart(fig)
    #finish = st.date_input("終了日を選択してください", value=datetime.date(2022, 8, 3))


#if st.button('Download CSV'):
csv = df.to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label="csv_download",
    data=csv,
    file_name="data.csv"
    )

