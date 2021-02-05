# -*- coding: utf-8 -*-
import pandas as pd
import os
'''
回傳每個區的統計數值,以dataframe紀錄
'''


import json 
with open("city_to_code.json" , "r") as fr:
    city_to_code = json.load(fr)


def risk_evalulate(city:str):
    code = city_to_code[city]
    df = pd.read_csv('concate_csvs/'+code+'.csv')

    '''排序與篩選資料'''
    df_sorted = df.sort_values(by = ['鄉鎮市區' , "交易年月日"])
    filter_都市土地使用分區為住 = df_sorted['都市土地使用分區'] == "住"
    df_sorted  = df_sorted[filter_都市土地使用分區為住]
    df_for_analysis = df_sorted[["鄉鎮市區","交易年月日","單價元平方公尺","土地區段位置建物區段門牌"]]
    
    #取出距今5年前資料
    from datetime import datetime
    y= str(int('{:%Y}'.format(datetime.today()))-1911)
    month_day = '{:%m%d}'.format(datetime.today())
    today_date_string = y+month_day
    five_year_ago_date = str(int(today_date_string)-50000)
    filter_5年內資料 = pd.to_numeric(df_for_analysis["交易年月日"]) > (int(today_date_string)-50000)
    df_for_analysis = df_for_analysis[filter_5年內資料]
    
 
    sd = pd.DataFrame(columns = ["鄉鎮市區","每平方公尺標準差","每平方公尺年成長率"])#存放各地區 每平方公尺標準差
    '''
    每平方公尺標準差:每筆交易紀錄都有每平方公尺價格p,p的標準差
    每平方公尺年成長率:p的年成長率
    '''
   
    #整理出這區域有哪些鄉鎮市區
    areas = set(list(df_for_analysis['鄉鎮市區']))
    for location in areas:
        fliter_location = df_for_analysis["鄉鎮市區"] == location
       
        if any(fliter_location):#當有找到相符路段才執行dataframe操握
            df_location = df_for_analysis[fliter_location]
            df_location["單價元平方公尺"]=pd.to_numeric(df_location["單價元平方公尺"])
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
            tempt = pd.DataFrame({"鄉鎮市區":location,"每平方公尺標準差":sd_of_location,"每平方公尺年成長率":annual_gross_rate,"meanValue":mean_value_of_location},index=[1])
            
            sd = sd.append(tempt,ignore_index = True)
        
    
    return sd




















