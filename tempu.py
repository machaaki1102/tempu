import streamlit as st
import re
import pandas as pd

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