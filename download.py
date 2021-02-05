# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import time

'''
Summary of dwonlaod.py:
    if 檢查是否已經更新至最新實價登陸資料 == True:
        pass
    else:
        開始爬缺失資料
'''
if not os.path.isdir("raw_download_data"):
    os.mkdir("raw_download_data")

def real_estate_crawler(year, season):
    if "raw_download_data" in os.listdir():    
        os.chdir("raw_download_data")
    if year > 1911:
        year -= 1911
    
    # download real estate zip content
    res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season="+str(year)+"S"+str(season)+"&type=zip&fileName=lvr_landcsv.zip")
    
    # save content to file
    fname = str(year)+str(season)+'.zip'
    open(fname, 'wb').write(res.content)
    
    # make additional folder for files to extract
    folder = 'real_estate' + str(year) + str(season)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    # extract files to the folder
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(folder)
    
    time.sleep(10)
    
def check_if_first_downlaod():
    dirs = [d for d in os.listdir("./raw_download_data") if d[0:4] == "real"]
    if len(dirs) == 0:
        return True
    else:
        return False

def time_iter(lastTime , today_date_string):
    begin_season=int(lastTime[-1])
    begin_year = int(lastTime.rstrip(str(begin_season)))
    end_season = int(today_date_string[-1])
    end_year = int(today_date_string.rstrip(str(end_season)))
    time_period = []
    y_idx = begin_year
    s_idx = begin_season
    flag = True
    while(y_idx<=end_year and flag):
        while(s_idx<=4 and flag):
            if str(y_idx)+str(s_idx) == str(end_year)+str(end_season) :
                flag =False
                time_period.append( (y_idx,s_idx) )
            else:
                time_period.append( (y_idx,s_idx) )
                s_idx+=1
        y_idx+=1
        s_idx=1
    return time_period


from datetime import datetime
y= str(int('{:%Y}'.format(datetime.today()))-1911)
month= '{:%m}'.format(datetime.today())
today_date_string = y+str((int(month)-1)//3+1)


if check_if_first_downlaod():
    time_period = time_iter("1021",today_date_string)
else:
    dirs = [d for d in os.listdir("raw_download_data") if d[0:4] == "real"]
    lastTime = dirs[-1].replace("real_estate","")
    time_period = time_iter(lastTime,today_date_string)

for year,season in time_period:
    print(year, season)
    try:
        real_estate_crawler(year, season)
    except zipfile.BadZipFile:
        if os.path.isdir("real_estate"+ str(year) + str(season)):
            os.rmdir("real_estate" + str(year) + str(season))


'''
x_lvr_land_a：房屋買賣交易
x_lvr_land_b：新成屋交易
x_lvr_land_c：租房交易
其中 x 是一個英文字母，代表每個縣市，也就是你身份證字號的開頭
例如台北，就是「a」，新北市就是「f」，以此類推
'''