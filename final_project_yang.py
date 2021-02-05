# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:58:37 2020

@author: jason
"""


import pandas as pd
from datetime import datetime

def average(n):
   try:
       ans = sum(n)/len(n)
       return (ans)
   except:
       return('資料缺失')

def landtax(lp):
    #lp = 課稅總地價
    if lp <= 39961000:
        lp = lp * 10/1000
    elif 39961001 < lp <= 239766000:
        lp = lp * 15/1000 - 199805
    elif 239766001 < lp <= 439571000:
        lp = lp * 25/1000 -2597465
    elif 439571001 < lp <= 639376000:
        lp = lp * 35/1000 - 6993175
    elif 639376001 < lp <= 839181000:
        lp = lp * 45/1000 - 13386935
    elif lp > 839181001:
        lp = lp * 55/1000 - 21778745
        
    return lp


def transactiontax(p):
    #p = 房屋現值
    #20% : 2年~20年的稅率
    return p*0.02       
'''    
def get_houseAge(data) :
    #today
    y= str(int('{:%Y}'.format(datetime.today()))-1911)
    today_year = int(y)
    
    data_age=data["建築完成年月"].copy()
    data_age=data_age//10000
    data_age=today_year-data_age
    data_age = data_age.fillna(int(data_age.mean()))
    data_age=data_age+5
    data["五年後屋齡"] = data_age.copy()
    return data
'''
def get_houseAge_road(data,location):
    #today
    y= str(int('{:%Y}'.format(datetime.today()))-1911)
    today_year = int(y)
    fliter_location = data["土地區段位置建物區段門牌"].str.contains(location)
    df_location = data[fliter_location]
    data_age=df_location["建築完成年月"].copy()
    data_age=data_age//10000
    data_age=today_year-data_age
    data_age = data_age.fillna(int(data_age.mean()))
    data_age=data_age+5
    return data_age.mean()
def get_houseAge(data,location) :
    #today
    y= str(int('{:%Y}'.format(datetime.today()))-1911)
    today_year = int(y)
    fliter_location = data["土地區段位置建物區段門牌"].str.contains(location)
    df_location = data[fliter_location]
    data_age=df_location["建築完成年月"].copy()
    data_age=data_age//10000
    data_age=today_year-data_age
    data_age = data_age.fillna(int(data_age.mean()))
    data_age=data_age+5
    data["五年後屋齡"] = data_age.copy()
    return data


def drawpic(time,price):

    import matplotlib.pyplot as plt
    
    plt.plot(time,price)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

def housetax(p,y):
    #p = 核定單價(房價) ?
    #a = 面積 ?
    #y = 折舊年數 
    return p*(1-(0.012*y))*0.9*0.015
                
def find(n,date5year_ago,old_location):
    data = pd.read_csv(n + ".csv")
   # get_houseAge(data)
    fliter_交易年月日欄位為國字 = data["交易年月日"] == "交易年月日"
    data =  data[~fliter_交易年月日欄位為國字]
    fliter_交易年月日欄位為英文 = data["交易年月日"] == "transaction year month and day"
    data = data[~fliter_交易年月日欄位為英文]
    
    data = data.sort_values(by = ["交易年月日"])
    data = data.reset_index()
       # old_location = '信義區忠孝東路五段'
       # date5year_ago = '1010106'
    date4year_ago = str(int(date5year_ago)+10000)
    date3year_ago = str(int(date5year_ago)+20000)
    date2year_ago = str(int(date5year_ago)+30000)
    date1year_ago = str(int(date5year_ago)+40000)
    now = str(int(date5year_ago)+50000)
    empty = pd.DataFrame(columns = data.columns)          
    for i in range(0,len(data)):
       if int(data["交易年月日"][i]) > int(now) :
           break
       if int(data["交易年月日"][i]) > int(date5year_ago):  
           if old_location in data['土地區段位置建物區段門牌'][i]:
               empty = empty.append(data[i:i+1],ignore_index = True)
            
    from pandas.core.frame import DataFrame
    choced_data=DataFrame(empty)            
    choced_data.to_csv('choced_data.csv', encoding='cp950')
    
    
    list_5_year_ago = []
    list_4_year_ago = []
    list_3_year_ago = []
    list_2_year_ago = []
    list_1_year_ago = []
    for i in range(0,len(choced_data)):
        if int(now) > int(choced_data["交易年月日"][i]) > int(date1year_ago):
            if str(choced_data['單價元平方公尺'][i]) != 'nan':
                list_1_year_ago.append(choced_data['單價元平方公尺'][i])
        elif int(date1year_ago) > int(choced_data["交易年月日"][i]) > int(date2year_ago):
            if str(choced_data['單價元平方公尺'][i]) != 'nan' :
                list_2_year_ago.append(choced_data['單價元平方公尺'][i])
        elif int(date2year_ago) > int(choced_data["交易年月日"][i]) > int(date3year_ago):
            if str(choced_data['單價元平方公尺'][i]) != 'nan' :
                list_3_year_ago.append(choced_data['單價元平方公尺'][i])
        elif int(date3year_ago) > int(choced_data["交易年月日"][i]) > int(date4year_ago):
            if str(choced_data['單價元平方公尺'][i]) != 'nan' :
                list_4_year_ago.append(choced_data['單價元平方公尺'][i])    
        elif int(date4year_ago) > int(choced_data["交易年月日"][i]) > int(date5year_ago):
            if str(choced_data['單價元平方公尺'][i]) != 'nan' :
                list_5_year_ago.append(choced_data['單價元平方公尺'][i])
            
            
    price_list = []
    price_list.append(average(list_5_year_ago))
    price_list.append(average(list_4_year_ago))
    price_list.append(average(list_3_year_ago))
    price_list.append(average(list_2_year_ago))
    price_list.append(average(list_1_year_ago))
            
    time_list = []
    time_list.append(int(date5year_ago[:3]))
    time_list.append(int(date4year_ago[:3]))
    time_list.append(int(date3year_ago[:3]))
    time_list.append(int(date2year_ago[:3]))
    time_list.append(int(date1year_ago[:3]))
    
    
    drawpic(time_list,price_list)
    try:
        return(((price_list[1]/price_list[0])+(price_list[2]/price_list[1])+(price_list[3]/price_list[2])+(price_list[4]/price_list[3]))/(len(price_list)-1))
    except:
        return('資料缺失')
    
    ####################################################################################################


''' 
另外功能
input:
    地區:台中市
    過去時間:1010903
    地點:信義區忠孝東路五段
    資金量:1000萬
    預計面積:50坪
    找出過去時間後推五年內和地點有關的交易紀錄
    分別算出第一年第二年第三年第四年第五年平均每平方公尺房價
    以歷年平均房價算出每平方公尺房價成長率、每平方公尺房價平均成長率
    把路段平均成長率**5資金量 視為未來五年的房價在此設此房價為X
    X*稅率 = tax     X-資金量-TAX = 獲利
output:
    獲利
'''







