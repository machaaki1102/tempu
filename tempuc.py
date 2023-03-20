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


#startからfinishまでが何か月か確認する　3:int
def month_difference(date1,date2):
    months = (date2.year - date1.year) * 12 + date2.month - date1.month
    return months

#startの年月を使い。1か月間の日付ののリストを作る。 :list
def date_lists(year,month):
      date_list = []
      _, last_day = calendar.monthrange(year, month)

      for day in range(1, last_day+1):
          date_list.append(datetime.date(year, month, day))
      return date_list

#１か月分の気象庁のデータをスクレイピングする。別途　prec_no とblock_noが事前に必要、Blockは5桁。データフレームを作成
def total_tem(year,month,day):    
    url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day={day}&view='
   
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # findAllで条件に一致するものをすべて抜き出します。
    rows = soup.findAll('tr',class_='mtx')
    #データだけを抜き出す
    rows = rows[4:]
    All_list = [['平均気温(℃)','日照時間(h)','降水量(mm)','最高気温(℃)','最低気温(℃)']]
    for row in rows:

            data = row.findAll('td')
            rowData = [] #初期化
            rowData.append(float(data[6].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[16].string.replace(")", "").replace(" ", "").replace("]", "")))
            if  '--' in data[3].string:
                rowData.append(0)
            else:
                rowData.append(float(data[3].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[7].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[8].string.replace(")", "").replace(" ", "").replace("]", "")))
    
            All_list.append(rowData)
            
    data = All_list[1:]
    columns = All_list[0]
    df = pd.DataFrame(data,columns=columns)    
    
    #1か月間の日付
    date_list = []
    _, last_day = calendar.monthrange(year, month)

    for day in range(1, last_day+1):
        date_list.append(datetime.date(year, month, day))
    
    df['日付'] = date_list

    return df

#細かい地点用で1か月のデータフレームを作る。
def total_tem2(year,month,day):
    if block_no_2 <1000:
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_a1.php?prec_no={prec_no_2}&block_no=0{block_no_2}&year={year}&month={month}&day={day}&view='
    elif block_no_2 <10000:
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_a1.php?prec_no={prec_no_2}&block_no={block_no_2}&year={year}&month={month}&day={day}&view='
    else:
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day={day}&view='
        
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # findAllで条件に一致するものをすべて抜き出します。
    rows = soup.findAll('tr',class_='mtx')
    
    All_list = [['平均気温(℃)','日照時間(h)','降水量(mm)','最高気温(℃)','最低気温(℃)']]
   
    if block_no_2 <10000:
        rows = rows[3:]
    #All_list = [['陸の平均気圧(hPa)', '海の平均気圧(hPa)', '降水量(mm)',最低気温(℃) '平均気温(℃)', '平均湿度(%)', '平均風速(m/s)', '日照時間(h)']]
    #All_list = [['平均気温(℃)','日照時間(h)','降水量(mm)','最高気温(℃)','最低気温(℃)']]
        for row in rows:
            # 今trのなかのtdをすべて抜き出します
            data = row.findAll('td')

              #１行の中には様々なデータがあるので全部取り出す。
            rowData = [] #初期化
            if  '--' in data[4].string or '/' in data[4].string:
                rowData.append(0)
            else:
                rowData.append(float(data[4].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            if  '--' in data[15].string or '/' in data[15].string:
            #if data[3].string == '--':
                #rowData.append(np.nan)
                rowData.append(0)
            else:
                rowData.append(float(data[15].string.replace(")", "").replace(" ", "").replace("]", "")))
 
            if  '--' in data[1].string or '/' in data[1].string:
            #if data[3].string == '--':
                #rowData.append(np.nan)
                rowData.append(0)
            else:
                rowData.append(float(data[1].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            if  '--' in data[5].string or '/' in data[5].string:
            #if data[3].string == '--':
                #rowData.append(np.nan)
                rowData.append(0)
            else:
                rowData.append(float(data[5].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            if  '--' in data[6].string or '/' in data[6].string:
            #if data[3].string == '--':
                #rowData.append(np.nan)
                rowData.append(0)
            else:
                rowData.append(float(data[6].string.replace(")", "").replace(" ", "").replace("]", "")))

            All_list.append(rowData)
            
    else:   
        rows = rows[4:] 

        for row in rows:

            data = row.findAll('td')
            rowData = [] #初期化
            rowData.append(float(data[6].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[16].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            if  '--' in data[3].string:
                rowData.append(0)
            else:
                rowData.append(float(data[3].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            rowData.append(float(data[7].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[8].string.replace(")", "").replace(" ", "").replace("]", "")))
    
            All_list.append(rowData)


    data = All_list[1:]
    columns = All_list[0]
    df_3 = pd.DataFrame(data,columns=columns)

    date_list = []
    _, last_day = calendar.monthrange(year, month)

    for day in range(1, last_day+1):
        date_list.append(datetime.date(year, month, day))
    
    #日付を月を付ける。
    df_3['日付'] = date_list

    return df_3

#過去の30年平均値を取る。降水量、平均気温、日照時間。別途　prec_no とblock_noが事前に必要
def total_tem_30(year,month,day):
    url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/nml_sfc_d.php?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day={day}&view='
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # findAllで条件に一致するものをすべて抜き出します。
    rows = soup.findAll('tr',class_='mtx')
    #データだけを抜き出す
    rows = rows[3:]
    All_list = [['平均気温(℃)','日照時間(h)','降水量(mm)']]
    for row in rows:

            data = row.findAll('td')
            #data
            rowData = [] #初期化
            rowData.append(float(data[1].string.replace(")", "").replace(" ", "").replace("]", "")))
            rowData.append(float(data[4].string.replace(")", "").replace(" ", "").replace("]", "")))
            
            if  '--' in data[0].string:
                rowData.append(0)
            else:
                rowData.append(float(data[0].string.replace(")", "").replace(" ", "").replace("]", "")))
   
            All_list.append(rowData)
            
    data = All_list[1:]
    columns = All_list[0]
    df = pd.DataFrame(data,columns=columns)    
    #Indexを1からふり直す
    date_list = []
    _, last_day = calendar.monthrange(year, month)

    for day in range(1, last_day+1):
        date_list.append(datetime.date(year, month, day))
    
    df['日付'] = date_list

    return df

#startの日にちからデータフレームを作る。自己関数total_tems　1か月分 (total_tem:通常、total_tem2:細かい,
#total_tem30:過去30年）を使っている。
def detaFrame_meke(start,finish,total_tems):
    year = start.year
    month = start.month
    day = start.day
    #1か月分のデータフレームを作る。自己関数total_tem
    df = total_tems(year,month,day)
    #必要な月分で増やす
    start_add = start
    #自己関数month_differencを栽培期間の何か月かとる。
    months = month_difference(start,finish)
    while months >0:
        start_add = start_add + relativedelta(months=1)
        year_2 = start_add.year 
        month_2 = start_add.month
        df = pd.concat([df,total_tems(year_2,month_2,1)],axis=0)
        months = months -1
    #日付をオブジェクトから日数にする 
    df["日付"] = pd.to_datetime(df["日付"], format="%Y-%m-%d")

    #期間を絞る。
    df = df.query(f"'{start}' <= 日付 <= '{finish}'")

    #indexを0から降りなおす
    df = df.reset_index()

    #余分なデータを消して並び変える。
    df = df.drop("index", axis=1)
    df = df.reindex(columns=["日付", "平均気温(℃)","最高気温(℃)","最低気温(℃)","降水量(mm)","日照時間(h)"])
    return df

#データフレームから気温と降水量と日照時間のグラフを作る。df:データフレーム　title:気温差_前年比較(例)
def figu(df,title):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["日付"], y=df["平均気温(℃)"], name="平均気温(℃)", line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["日付"], y=df["最高気温(℃)"], name="最高気温(℃)", line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df["日付"], y=df["最低気温(℃)"], name="最低気温(℃)", line=dict(color='blue')))
    fig.add_trace(go.Bar(x=df["日付"], y=df["降水量(mm)"], name="降水量(mm)", marker_color='gray'), secondary_y=True)
    fig.add_trace(go.Bar(x=df["日付"], y=df["日照時間(h)"], name="日照時間(h)", marker_color='orange'), secondary_y=True)

    # 1つめのy軸の範囲設定
    fig.update_yaxes(range=[-20, 40], title_text="気温(℃)", secondary_y=False)
    # 2つめのy軸の範囲設定
    fig.update_yaxes(range=[0, 100], title_text="降水量(mm)", secondary_y=True)
    fig.update_layout(title=title)    
    return fig

#df_ago と　df　の　差をグラフかする y=平均気温(℃),title=気温差の前年比較
def diff(df_ago,df,what,title):
    df_dif = df_ago[["平均気温(℃)","降水量(mm)","日照時間(h)"]] - df[["平均気温(℃)","降水量(mm)","日照時間(h)"]]
    df_dif['日付'] = df["日付"]
    fig = go.Figure()
    # 差分の折れ線グラフを追加します
    fig.add_trace(go.Scatter(x=df_dif["日付"], y=df_dif[what], mode="lines", name="差分"))
    # 積み上げ値の折れ線グラフを追加します
    fig.add_trace(go.Scatter(x=df_dif["日付"], y=df_dif[what].cumsum(), mode="lines", name="積み上げ"))
    # X軸を日付として設定します
    fig.update_xaxes(type='date', tickformat='%Y-%m-%d', title="日付")
    fig.update_layout(title=title)
    return fig

#body

#事前準備　prec_noとblock_no含んだ『県マスター』作成し、データを読み込む
df = pd.read_csv("kishou.txt", header=None,skiprows=1,sep="\s*,\s*", engine="python")
df_sub = df.iloc[:,[0,1,2,3,4,10]] 
df_sub.columns = ["No.", "i", "地点名", "prec_no", "block_no","県"]

#画面表示
st.set_page_config(page_title="気象データ",layout="wide")
st.title("栽培期間中の気温/降水量/日射量(気象庁データ)")
show_30 = st.sidebar.checkbox('過去30年平均とも比較する')
show_min = st.sidebar.checkbox('より細かい地点で確認する')
st.sidebar.write('注意:気象庁のデータが無い場合あり')

# 3つの列を作成　県,start,finish を入力値を決まる。
col1, col2, col3 = st.columns(3)
with col1:
    ken =st.selectbox('県を選んでください',df_sub['県'].unique())
with col2:
    start = st.date_input("開始日を選択してください", value=datetime.date(2022, 5, 5))
with col3:
    finish = st.date_input("終了日を選択してください", value=datetime.date(2022, 10, 3))

#県からデータを取得
prec_no,block_no = df_sub.loc[df_sub['県'] == ken, ['prec_no','block_no']].values[0]
block_no = int(block_no)

#データフレームを今年と一年前を作る。
df = detaFrame_meke(start,finish,total_tem)
df_ago = detaFrame_meke(start - relativedelta(years=1),finish - relativedelta(years=1),total_tem)

#今年のデータを表示　figという自己関数を使う。
fig2 = figu(df,'今年の天候')
#1年前のデータを表示
fig3 = figu(df_ago,'1年前の天候')

#diffという自己関数を使って1年前と比較したグラフを作成する。
fig = diff(df_ago,df,'平均気温(℃)','気温差_前年比較')
fig4 = diff(df_ago,df,'日照時間(h)','日照時間_前年比較')


#diffという自己関数を使って30年前平均と比較したグラフを作成する
if show_30:
#30年平均のデータフレーム
    df_30 = detaFrame_meke(start,finish,total_tem_30)

#show_30 = st.sidebar.checkbox('過去30年平均とも比較する')
    fig_30 = diff(df_30,df,'平均気温(℃)','気温差_30年平均比較')
    fig_30_h = diff(df_30,df,'日照時間(h)','日照時間_30年平均比較')

#2段目以降のグラフを作る。
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
    st.plotly_chart(fig4, use_container_width=True)


#サイドバーチェック付けた時のみ30年平均との差を表示
if show_30:
#30年平均のデータフレーム
    df_30 = detaFrame_meke(start,finish,total_tem_30)
#show_30 = st.sidebar.checkbox('過去30年平均とも比較する')
    fig_30 = diff(df_30,df,'平均気温(℃)','気温差_30年平均比較')
    fig_30_h = diff(df_30,df,'日照時間(h)','日照時間_30年平均比較')
    with col1:
        st.plotly_chart(fig_30, use_container_width=True)
    with col2:
        st.plotly_chart(fig_30_h, use_container_width=True)


csv = df.to_csv(index=False).encode('utf-8-sig')
csv2 = df_ago.to_csv(index=False).encode('utf-8-sig')

# 各列にselectboxを追加
col1, col2 = st.columns(2)

with col1:
    st.download_button(
    label="今年のデータ　csv_download",
    data=csv,
    file_name="data.csv"
    )
with col2:
    st.download_button(
    label="1年前のデータ　csv_download",
    data=csv2,
    file_name="data.csv"
    )
#チェックがついた場合、県の以下のレベルを作る
if show_min:
    #すべての点のデータ
    df_nono = pd.read_csv('df3.csv')
    #kenは基のデータから引っ張る = '北海道'だった時
    df_nono = df_nono[df_nono['県'] == ken]
    df_nono_2 = df_nono[['県','prec_no','block_no','地点名']]
    df_nono_2 = df_nono_2.sort_values('block_no', ascending=False)

    prec =st.selectbox('地名を選んでください',df_nono_2['地点名'].unique())
    prec_no_2 = df_nono_2[df_nono_2['地点名'] == prec]['prec_no'].values[0]
    block_no_2 = df_nono_2[df_nono_2['地点名'] == prec]['block_no'].values[0]

    df_min = detaFrame_meke(start,finish,total_tem2)
    df_min_ago = detaFrame_meke(start - relativedelta(years=1),finish - relativedelta(years=1),total_tem2)
    
    #今年のデータを表示　figという自己関数を使う。
    fig_min_2 = figu(df_min,'今年の天候')
    #1年前のデータを表示
    fig_min_3 = figu(df_min_ago,'1年前の天候')

    #diffという自己関数を使って1年前と比較したグラフを作成する。
    fig_min = diff(df_min_ago,df_min,'平均気温(℃)','気温差_前年比較')
    fig_min4 = diff(df_min_ago,df_min,'日照時間(h)','日照時間_前年比較')

    #diffという自己関数を使って30年前平均と比較したグラフを作成する
    if show_30:
    #30年平均のデータフレーム
        df_min_30 = detaFrame_meke(start,finish,total_tem_30)
    #show_30 = st.sidebar.checkbox('過去30年平均とも比較する')
        fig_min_30 = diff(df_min_30,df_min,'平均気温(℃)','気温差_30年平均比較')
        fig_min_30_h = diff(df_min_30,df_min,'日照時間(h)','日照時間_30年平均比較')

    #2段目以降のグラフを作る。
    col1, col2 = st.columns(2)
    # 各列にselectboxを追加
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_min_2, use_container_width=True)
    with col2:
        st.plotly_chart(fig_min_3, use_container_width=True)

    col1, col2 = st.columns(2)

    # 各列にselectboxを追加
    with col1:
        st.plotly_chart(fig_min, use_container_width=True)
    with col2:
        st.plotly_chart(fig_min4, use_container_width=True)

    #サイドバーチェック付けた時のみ30年平均との差を表示
    if show_30:
        df_min_30 = detaFrame_meke(start,finish,total_tem_30)
        fig_min_30 = diff(df_min_30,df_min,'平均気温(℃)','気温差_30年平均比較')
        fig_min_30_h = diff(df_min_30,df_min,'日照時間(h)','日照時間_30年平均比較')
        with col1:
            st.plotly_chart(fig_min_30, use_container_width=True)
        with col2:
            st.plotly_chart(fig_min_30_h, use_container_width=True)

    csv_min = df_min.to_csv(index=False).encode('utf-8-sig')
    csv_min2 = df_min_ago.to_csv(index=False).encode('utf-8-sig')

   # 各列にselectboxを追加
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
        label="今年のデータ_詳細　csv_download",
        data=csv_min,
        file_name="data.csv"
        )
    with col2:
        st.download_button(
        label="1年前のデータ_詳細　csv_download",
        data=csv_min2,
        file_name="data.csv"
        )
