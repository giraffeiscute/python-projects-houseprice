# -*- coding: utf-8 -*-
import json 
import pandas as pd
with open("city_to_code.json" , "r") as fr:
    city_to_code = json.load(fr)

print(\
      """
       (1)檢查資料是否已經下載，若否則開始下載
       (2)查詢某縣市推薦投資鄉鎮市區
       (3)查詢某縣市最優路段
       (4)投資推薦
       (5)模擬走勢
       
      """
      )

mode = input("請輸入模式: ")
city= input("請輸入目標城市: ").replace("台","臺")
city_code = city_to_code[city]

if mode == "4" :#投資推薦
    from final_project_yang import *
    #讀入已經處理好的資料
    table = pd.read_csv("RiskReturnTables/risk_return_"+city_to_code[city]+".csv")
    資金量 = int(input("請輸入您所擁有資金量(單位:萬)"))*10000
    #只考慮使用者當前資金較可能買得起的範圍
    fliter_買得起 = table["mean_area"]*table["meanValue"] <=資金量
    table = table[fliter_買得起]
    
    print("""
          
          若願意承擔風險，將列舉成長率最高前五路段為可選標的
          若不願意承擔風險，則只列舉5個可能將風險幅度限縮於10%以下之標的
          *****地價上升10%與地價下降10%都對風險計算貢獻一樣
          
          """)
    是否可承擔風險 = input("是否可承擔風險 y/n :")
    assert 是否可承擔風險=="y" or 是否可承擔風險=="n" , "請輸入小寫y或n"
    if 是否可承擔風險 =="y":
        是否可承擔風險 =True
    elif 是否可承擔風險 =="n":
        是否可承擔風險 =False    
    if 是否可承擔風險  == False:#直接給可以賺最多錢的那地段
        #這個fliter篩出所有一個標準差以內的選擇
        fliter_風險內項目= table["每平方公尺標準差"] < 0.1*資金量/table["mean_area"]
        table = table[fliter_風險內項目]
    df_sortByGrowthRate  = table.copy().sort_values(by = ["每平方公尺年成長率"],ascending = False)[0:5]
    df_sortByGrowthRate = df_sortByGrowthRate.sort_values(by = ["每平方公尺標準差"])
    df_sortByGrowthRate = df_sortByGrowthRate.reset_index(drop = True)
    df_sortByGrowthRate["預測五年後單位房價"] = df_sortByGrowthRate["meanValue"]*( (df_sortByGrowthRate["每平方公尺年成長率"]+1)**5)
    city_csv = pd.read_csv("concate_csvs/"+city_code+'.csv')
    house_age_list = [int(get_houseAge_road(city_csv,i)) for i in df_sortByGrowthRate["road"]]
    df_sortByGrowthRate["price_now"]= df_sortByGrowthRate["meanValue"]*df_sortByGrowthRate["mean_area"]
    price_now_list = list(df_sortByGrowthRate["meanValue"]*df_sortByGrowthRate["mean_area"])
    tax_list = []
    for i in range(5):
        tax = housetax(price_now_list[i],house_age_list[i]) + landtax(price_now_list[i]) + transactiontax(price_now_list[i])
        tax_list.append(tax)
    df_sortByGrowthRate["tax"] = tax_list 
    df_sortByGrowthRate["profit"] = df_sortByGrowthRate["預測五年後單位房價"]*df_sortByGrowthRate["mean_area"]-df_sortByGrowthRate["tax"]
    print(df_sortByGrowthRate)
    
elif mode == "1":
    import download
    import os
    os.chdir("..")
    import MakeBigCsv
    '''MakeBigCsv就已經執行以下內容
    from clean_data import data_cleaner
    csv_files = [d for d in "concate_csvs" if ".csv" in d]
    data_cleaner(csv_files)
    '''
    import return_risk_calculator_ROAD
elif mode =="2":#查詢某縣市推薦投資鄉鎮市區
    from return_risk_calculator import risk_evalulate
    df_sortByGrowthRate = risk_evalulate(city)
    df_sortByGrowthRate = df_sortByGrowthRate.sort_values(by = ["每平方公尺標準差"])
    df_sortByGrowthRate = df_sortByGrowthRate.reset_index(drop = True)
    df_sortByGrowthRate["預測五年後房價"] = df_sortByGrowthRate["meanValue"]*( (df_sortByGrowthRate["每平方公尺年成長率"]+1)**5)

elif mode == "3":
    #讀入已經處理好的資料
    table = pd.read_csv("RiskReturnTables/risk_return_"+city_to_code[city]+".csv")
    df_sortByGrowthRate  = table.copy().sort_values(by = ["每平方公尺年成長率"],ascending = False)
    top_5_sections = df_sortByGrowthRate[0:5].copy()
    df_sortByGrowthRate = df_sortByGrowthRate.sort_values(by = ["每平方公尺標準差"])
    df_sortByGrowthRate = df_sortByGrowthRate.reset_index(drop = True)
elif mode == '5':
    from final_project_yang import *
    pasted_time = input('過去指定時段(格式ex1010903): ')
    #df = get_houseAge(data)
    road = input('地點: ')
    fund = int(input('資金量(單位:萬元): '))*10000
    times = find(city_code,pasted_time,road)
    price = fund*(times**5)
    data = pd.read_csv( city_code + ".csv")
       # get_houseAge(data)
    fliter_交易年月日欄位為國字 = data["交易年月日"] == "交易年月日"
    data =  data[~fliter_交易年月日欄位為國字]
    fliter_交易年月日欄位為英文 = data["交易年月日"] == "transaction year month and day"
    data = data[~fliter_交易年月日欄位為英文]
    
    data = data.sort_values(by = ["交易年月日"])
    data = data.reset_index()
    
    house_age = get_houseAge(data,road)
    house_age_list = []
    for i in range(0,len(house_age)):
        if str(data['五年後屋齡'][i]) != 'nan':
            house_age_list.append(data['五年後屋齡'][i])       
    
    tax = housetax(fund,average(house_age_list)) + landtax(fund) + transactiontax(price)
    profit = price - fund - tax
    
    print('淨利: ' + str(profit/10000) + '萬元')

    

    
    
    
