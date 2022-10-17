import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import urllib.request
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#from google.colab import files
#uploaded = files.upload()
#with open('C:\Users\srira\Downloads\GBP_JPY Historical Data.csv',newline='') as csvfile:
print('Please use the format "AUDUSD" to enter Fx Pair')
fx_pair1 = input('Enter Currency Pair: ')
go_back_period = input('Enter historical analysis period(5Y,1Y,1M,1Wk,1d,days): ')


#Define Analysis period based on user input
def end_date(periods):
    if periods == '5Y':
        end_period = (datetime.now() + timedelta(days=-(365*5)))        
    elif periods == '1Y':
        end_period = (datetime.now() + timedelta(days=-365))
    elif periods == '1M':
        end_period = (datetime.now() + timedelta(days=-30))
    elif periods == '1Wk':
        end_period = (datetime.now() + timedelta(days=-7))
    elif periods == '1d':
        end_period = (datetime.now() + timedelta(days=-1))
    elif periods == '':
        print('Incorrect Analysis period')
        sys.exit()
    else:
        end_period = (datetime.now() + timedelta(days=-int(periods)))


    return end_period

look_back_period = end_date(go_back_period)


#convert time periods to int pass it to data link
start = int(time.mktime(datetime.now().timetuple()))
end = int(time.mktime(look_back_period.timetuple()))

     
#Link copied from Yahoo finace as demo link
demo_link = f'https://query1.finance.yahoo.com/v7/finance/download/fx_pair=X?period1=start_period&period2=end_period&interval=1d&events=history&includeAdjustedClose=true'

#Prepare Fx pair1 data download link
repl_fx = demo_link.replace("fx_pair",fx_pair1.upper())
repl_period_start = repl_fx.replace("start_period",str(end))
final_fx1_link = repl_period_start.replace("end_period",str(start))

#Test URL validity
try:
    #if valid load fx data into dataframe
    GBP_JPY = pd.read_csv(final_fx1_link)    
except urllib.error.HTTPError as e:
    print('Incorrect Currency Pair')
    sys.exit()




#Strategy Start
#Calculate different SMA and Max and Min of SMA over a given period.
SMA30 = pd.DataFrame()
SMA30['Price'] = GBP_JPY['Close'].rolling(window=30).mean()
SMA30

SMA100 = pd.DataFrame()
SMA100['Price']=GBP_JPY['Close'].rolling(window=100).mean()
SMA100

MAX30 = pd.DataFrame()
MAX30['Price']=GBP_JPY['Close'].rolling(window=10).max()
MAX30

MIN20 = pd.DataFrame()
MIN20['Price']=GBP_JPY['Close'].rolling(window=10).min()
MIN20

##plt.figure(figsize=(12.5,4.5))
##plt.plot(GBP_JPY['Price'],label='Original Close Price')
##plt.plot(SMA30['Price'],label='SMA30')
##plt.plot(SMA100['Price'],label='SMA100')
##plt.plot(MAX30['Price'],label='MAX30')
##plt.plot(MIN20['Price'],label='MIN20')
##plt.legend(loc='lower right')
##plt.show()

data = pd.DataFrame()
data['Org_Price']=GBP_JPY['Close']
data['SMA30']=SMA30['Price']
data['SMA100']=SMA100['Price']
data['MAX30']=MAX30['Price']
data['MIN20']=MIN20['Price']
data

def BS_Signal(data):
  Buy_Signal = []
  Sell_Signal = []
  buy_flag = 0
  sell_flag = 0

  for i in range(len(data)):
    if data['Org_Price'][i]>data['SMA30'][i] and data['Org_Price'][i]<data['MAX30'][i]:
      if buy_flag == 0:
        Buy_Signal.append(data['Org_Price'][i])
        Sell_Signal.append(np.nan)
        buy_flag = 1
        sell_flag = 0
      else:
        Buy_Signal.append(np.nan)
        Sell_Signal.append(np.nan)
    elif data['Org_Price'][i]==data['MAX30'][i] or data['Org_Price'][i]==data['MIN20'][i]:
      if sell_flag == 0:
        Buy_Signal.append(np.nan)
        Sell_Signal.append(data['Org_Price'][i])
        sell_flag = 1
        buy_flag = 0
      else:
        Buy_Signal.append(np.nan)
        Sell_Signal.append(np.nan)
    else:
      Buy_Signal.append(np.nan)
      Sell_Signal.append(np.nan)

  return(Buy_Signal,Sell_Signal)

BS_Signal = BS_Signal(data)
data['Buy_Signal']=BS_Signal[0]
data['Sell_Signal']=BS_Signal[1]
data

plt.figure(figsize=(12.8,4.8))
plt.plot(data['Org_Price'],label='Org_Price')
plt.plot(data['SMA30'],label='SMA30')
plt.plot(data['SMA100'],label='SMA100')
plt.scatter(data.index, data['Buy_Signal'], label='Sell', marker='v', color='red')
plt.scatter(data.index,data['Sell_Signal'], label='Sell', marker='^', color='green')
plt.title(fx_pair1+ " Buy/Sell Signals")
plt.xlabel("Analysis Period Start - "+str(look_back_period))
plt.ylabel('Price')
plt.legend(loc='upper right')
plt.show()
