# -*- coding: utf-8 -*-
"""
將同一地區分散於不同季度資料合併為一份csv(ex:a.csv (臺北市))，由於檔案大小不大，可以每次更新都從頭做
"""
import os
import json
if not os.path.isdir("concate_csvs"):
    os.mkdir("concate_csvs")
    
with open("code_to_city.json" , "r" ) as fr:
    code_to_city = json.load(fr)
    codes = list(code_to_city.keys())
    for i in range(len(codes)):
        codes[i] = str(codes[i])
dirs = [d for d in os.listdir("raw_download_data") if d[:4] == "real" ]


for i in range(0,len(codes)):#build file for each city
    with open('concate_csvs/'+codes[i]+".csv","w") as f:
        f.write("")
    for j in range(len(dirs)):#逐開個個real_estimate資料夾
        try:
            fr = open('raw_download_data/'+dirs[j]+"/"+codes[i]+"_lvr_land_a.csv" , 'rb').read()
            print(dirs[j]+"/"+codes[i]+"_lvr_land_a.csv")
            with open('concate_csvs/'+codes[i]+".csv","ab") as f:
                f.write(fr)
        except FileNotFoundError:
            pass


from clean_data import *

csv_files = [d for d in os.listdir("concate_csvs") if ".csv" in d]
data_cleaner(csv_files)

