"""

Date:- 3-Aug-2020 
Libraries Require:
- Pandas 
- yfinance

I have uploaded IndiaStockList.csv but incase if you need to update your list,
You Can Download Indian StockList File from 
- https://www.bseindia.com/corporates/List_Scrips.aspx

Rename the downloaded file to IndiaStockList.csv
I have use concurrent.futures ThreadPoolExecutor to download data in Parallelly and faster
"""


# import all required Libraries
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from os import path,mkdir

# check if data folder exist, if yes then skip, if no create one
if not path.exists('data'):
    mkdir('data')
    
# load the download file from bseIndia website 
stocks = pd.read_csv('IndiaStockList.csv') 

"""
Total list of stocks dataframe is 
12856 rows × 10 columns

"""




# Here I am Choosing to Download Equity's from the list
"""
The Whole List is here

['Equity', 'MF', 'Preference Shares', 'Commercial Papers', ' ','Debentures and Bonds']

"""
"""
At time of Writing this code there are 6774 Equity stocks so It might take some time to download


0              ABB.NS
1         AEGISLOG.NS
2       AMARAJABAT.NS
3        AMBALALSA.NS
4             HDFC.NS
            ...      
6770          PCPL.NS
6771     SUPERNOVA.NS
6772        CITYON.NS
6773      HASJUICE.NS
6774         WEBSL.NS
Name: Security Id, Length: 4205, dtype: object


"""

Equity = stocks.loc[stocks['Instrument']=='Equity']

# getting SecurityId which is unique for all stocks and adding .NS so that we can search for this in yahoo finance
Security_Id = Equity['Security Id']
Security_Id = Security_Id.map('{}.NS'.format)

# Created A function so that it can run concurrently with ThreadPoolExcutor module
# It will download files and save it to data/ folder
def downloadCSV(ticker):
    try:
        yf.Ticker(ticker).history(period="max").to_csv('data/' + ticker + '.csv')
    except Exception as e:
        print(e)

# Now Calling the function concurrently 
with ThreadPoolExecutor() as executor:
    for id in Security_Id:
        executor.submit(downloadCSV, id)

