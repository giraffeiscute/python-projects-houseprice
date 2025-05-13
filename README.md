# 房價預測幫手
## 專案簡介 
本專案透過歷年房價資料分析，協助不同類型的房地產投資者評估風險、挑選標的地點，達成「理性投資、穩健獲利」的目標。

## 系統功能 
### 功能一：依區域計算房價風險與收益
計算每坪單價的標準差與平均成長率

整理資料依「年份」與「路段」分類

### 功能二：投資建議系統
依據使用者輸入的「資金」與「風險承受能力」，進行三層分類：

| 投資人類型 | 資本額 | 承擔風險 | 推薦策略            |
| ----- | --- | ---- | --------------- |
| 小資族   | 少   | 是    | 推薦高成長率、低風險標的    |
| 投資新手  | 任意  | 否    | 僅推薦波動低於 10% 的標的 |
| 炒房客   | 高   | 是    | 推薦高潛力、風險較高路段    |

### 功能三：地點推薦查詢
查詢縣市最佳投資鄉鎮

查詢特定縣市內報酬率最佳之路段

### 功能四：風險容忍查詢
顯示可承受風險 vs. 無法承擔風險的不同推薦組合

### 功能五：預測房價走勢
結合建設利多（如捷運、開發案）與歷史波動，預測房價上漲潛力

## 程式架構 
使用 Python 撰寫

自動爬蟲更新內政部實價登錄資料

每季自動分類、整理、刪除缺值與工商用地

利用標準差 / 本金 決定風險水平

## 操作範例 
範例投資人條件： <br/>
資本額：1000 萬元，願意承擔風險 <br/>
→ 系統將推薦 5 筆報酬率高、風險可控的前五標的區段與預期報酬
<img src="https://github.com/giraffeiscute/python-projects-houseprice/blob/main/result/demo.png" alt="image" width="900">

## 技術關鍵 | Technical Highlights
- 網路爬蟲（即時同步房價資料）

- 檔案預處理（合併季度、計算均價、土地面積等）

- 自動分層推薦演算法

- 房價預測模型（依歷史波動擬合趨勢）

## 參考資料 
內政部實價登錄資料

## 作者
楊致遠 (Chih-Yuan Yang)

戴晟恩 (Sheng-En Tai)

林羽霈 (Yu-Pei Lin)


****

# House Price Forecasting Assistant 
## Project Overview
This project leverages historical housing price data to help various types of real estate investors assess risk, identify target locations, and achieve the goal of rational investing and stable returns.

## System Features
### Function 1: Regional Housing Price Risk and Return Analysis
Calculates the standard deviation and average growth rate of price per ping (坪).

Organizes data by year and street segment.

### Function 2: Investment Recommendation System
Based on the user's input capital and risk tolerance, the system categorizes investors into three tiers:

| Investor Type   | Capital | Risk Tolerance | Recommended Strategy                          |
| --------------- | ------- | -------------- | --------------------------------------------- |
| Budget Investor | Low     | Yes            | High growth, low-risk areas                   |
| New Investor    | Any     | No             | Only recommend segments with < 10% volatility |
| Flipper         | High    | Yes            | High-potential, higher-risk areas             |


### Function 3: Location Recommendation Queries
Suggests the best towns for investment within a city/county.

Identifies top-performing streets in a selected city based on return rates.

### Function 4: Risk Tolerance-based Suggestions
Displays recommendation sets based on whether the user can tolerate risk or not.

### Function 5: Housing Price Trend Forecast
Combines favorable construction news (e.g., new MRT lines or developments) with historical volatility to forecast potential housing price increases.

## Code Structure
Written in Python

Web crawler automatically updates housing price data from the Ministry of the Interior

Quarterly data is automatically categorized, cleaned (removing missing values and commercial land), and preprocessed

Risk level determined by standard deviation / capital

## Demo
Sample Investor Profile: <br/>
Capital: NT$10 million, Willing to take risks <br/>
→ The system will recommend 5 high-return, controllable-risk street segments along with expected returns.

<img src="https://github.com/giraffeiscute/python-projects-houseprice/blob/main/result/demo.png" alt="image" width="900">

## Technical Highlights
- Web Scraping: Syncs with real-time housing price data

- Data Preprocessing: Quarterly merging, average price calculations, land area filtering

- Auto Tiered Recommendation Algorithm

- Price Forecasting Model: Based on historical volatility trends

## References
Ministry of the Interior Real Estate Transaction Database (Taiwan)

## Authors
Chih-Yuan Yang (楊致遠)

Sheng-En Tai (戴晟恩)

Yu-Pei Lin (林羽霈)


