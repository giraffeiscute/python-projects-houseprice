# -*- coding: utf-8 -*-
"""
含製作每條路的
每平方公尺標準差 每平方公尺年成長率 單位面積均價 此路段平均交易土地面積
的CSV檔案
"""
import pandas as pd
import os
if not os.path.isdir("RiskReturnTables"):
    os.mkdir("RiskReturnTables")
import json 
with open("code_to_city.json" , "r") as fr:
    code_to_city = json.load(fr)

citys = list(code_to_city.keys())
for i in range(len(citys)):
    calculator_road(citys[i])

def calculator_road(city_code):
    roads_city = pd.read_csv("全國路名/"+city_code+"_road.csv")
    df = pd.read_csv("concate_csvs/"+city_code+".csv")
    df = df.dropna(subset = ['鄉鎮市區',"土地區段位置建物區段門牌",'交易年月日','建物移轉總面積平方公尺','交易筆棟數','單價元平方公尺'])
    
    roads=[]
    for i in range(len(roads_city)):
        site_id = roads_city["site_id"][i]
        road = roads_city["road"][i]
        roads.append(site_id+road)
    
    
    #取出距今5年前資料
    from datetime import datetime
    y= str(int('{:%Y}'.format(datetime.today()))-1911)
    month_day = '{:%m%d}'.format(datetime.today())
    today_date_string = y+month_day
    five_year_ago_date = str(int(today_date_string)-50000)
    filter_5年內資料 = pd.to_numeric(df["交易年月日"]) > (int(today_date_string)-50000)
    df_for_analysis = df[filter_5年內資料]
    
    
    sd = pd.DataFrame(columns = ["road","每平方公尺標準差","每平方公尺年成長率"])#存放各地區 每平方公尺標準差
  
    count = 1
    for location in roads:
        fliter_location = df_for_analysis["土地區段位置建物區段門牌"].str.contains(location)
        print(location)
        print(count/len(roads))
        count+=1
        if any(fliter_location):#當有找到相符路段才執行dataframe操握
            df_location = df_for_analysis[fliter_location]
            df_location["單價元平方公尺"]=pd.to_numeric(df_location["單價元平方公尺"])
            df_location["建物移轉總面積平方公尺"] = pd.to_numeric(df_location["建物移轉總面積平方公尺"])
            df_location["土地數"] = df_location["交易筆棟數"].str.get(2)
            df_location["土地數"] = pd.to_numeric(df_location["土地數"])
            df_location["平均土地面積of一筆交易"] =  df_location["建物移轉總面積平方公尺"]//df_location["土地數"]
            #計算標準差
            sd_of_location = df_location["單價元平方公尺"].std()
            
            #計算年成長率
            mean_value_of_each_year = []    
            for i in range(5):
                fliter_certain_year = (pd.to_numeric(df_location['交易年月日']) >=int(five_year_ago_date)+i*10000) & (pd.to_numeric(df_location['交易年月日']) < int(five_year_ago_date) +10000+i*10000)
                mean_value_of_each_year.append(df_location[fliter_certain_year].mean()[1])
            gross_rate_of_each_year=[]
            for i in range(1,5):
                gross_rate_of_each_year.append( (mean_value_of_each_year[i]-mean_value_of_each_year[i-1])/mean_value_of_each_year[i] )
            annual_gross_rate = sum(gross_rate_of_each_year)/len(gross_rate_of_each_year)
            
            mean_value_of_location = df_location["單價元平方公尺"].mean()
            mean_area_of_location = df_location["平均土地面積of一筆交易"].mean()
            tempt = pd.DataFrame({"road":location,"每平方公尺標準差":sd_of_location,"每平方公尺年成長率":annual_gross_rate,"meanValue":mean_value_of_location,"mean_area":mean_area_of_location},index=[1])
            
            sd = sd.append(tempt,ignore_index = True)
       
        
        '''
    #處理中文顯示
    from pylab import mpl
    #mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定預設字型:解決plot不能顯示中文問題
    
    fliter_成長率小於0 = sd["每平方公尺年成長率"] <0
    sd = sd[~fliter_成長率小於0]
    sd = sd.dropna()
    sd = sd.sort_values(by=["每平方公尺年成長率"],ascending = False)
    sd.plot.scatter(x="每平方公尺標準差",y="每平方公尺年成長率")
    print("橫軸:風險 縱軸:年成長率")
    
    sd.to_csv("RiskReturnTables/risk_return_"+city_code+'.csv')
    return sd
    '''





