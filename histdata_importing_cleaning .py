##importing and cleaning data

# mkdir histdata_eurusd

# HISTDATA_COM_ASCII_EURUSD_M1202007
#     DAT_ASCII_EURUSD_M1_202007.csv
# HISTDATA_COM_ASCII_EURUSD_M1202007.zip
# HISTDATA_COM_ASCII_EURUSD_T202007
#     DAT_ASCII_EURUSD_T_202007.csv
# HISTDATA_COM_ASCII_EURUSD_T202007.zip
# HISTDATA_COM_MT_EURUSD_M1202007
#     DAT_MT_EURUSD_M1_202007.csv
# HISTDATA_COM_MT_EURUSD_M1202007.txt
# HISTDATA_COM_MT_EURUSD_M1202007.zip

#figure out best way to download data from histdata.com, unzip files, move to histdata_eurusd folder, 
#and delete duplicate files and txt files
from datetime import datetime
from datetime import timedelta 

t1 = datetime.now()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
mt4_7 = pd.read_csv('DAT_MT_EURUSD_M1_202007.csv')
mt4_7.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
mt4_7 = mt4_7.drop('vol', axis=1)
mt4_6 = pd.read_csv('DAT_MT_EURUSD_M1_202006.csv')
mt4_6.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
mt4_6 = mt4_6.drop('vol', axis=1)
frames = [mt4_6, mt4_7]
mt4 = pd.concat(frames, ignore_index = True)

ask7 = pd.read_csv('DAT_ASCII_EURUSD_T_202007.csv')
ask7.columns = ['datetime', 'bid', 'ask', 'vol']
ask7 = ask7.drop('vol', axis=1)  
ask6 = pd.read_csv('DAT_ASCII_EURUSD_T_202006.csv')
ask6.columns = ['datetime', 'bid', 'ask', 'vol']
ask6 = ask6.drop('vol', axis=1)  
frames = [ask6, ask7]
ask = pd.concat(frames, ignore_index = True)

#algo is slow so create new column to save second/ms data- saving data this way could save computing time   
ask['secs'] = ask['datetime'].str[13:15].str.cat(ask['datetime'].str[15:], sep = '.') 

t2 = datetime.now()
print('importing data took ' + str(t2-t1) + ' seconds')

##make sure you fill in missing valus at intersection of two dataframes correctly
##double check if minutes of ask and mt4 dataframes line up correctly or if they are one off from each other

t1 = datetime.now()
import ciso8601
#only necessary if using cisco algo, double check it saves time with extra step
ask['datetime'] = ask['datetime'].str[:-5]

##import cisco8601 function even faster apparently
ask['datetime'] = ask['datetime'].apply(lambda x: ciso8601.parse_datetime(x))
t2 = datetime.now()
print('cisco algo took ' + str(t2-t1) + ' seconds')

# t1 = datetime.now()
# #will start taking longer as you combine months, maybe place up top and run this on each month before you combine them
# def f(datestr):
#     return datetime(
#         int(datestr[:4]),
#         int(datestr[4:6]),
#         int(datestr[6:8]),
#         int(datestr[9:11]),
#         int(datestr[11:13]),
#     )
# ask['datetime'] = ask['datetime'].apply(lambda x: f(x))
# t2 = datetime.now()
# print('nested function algo took ' + str(t2-t1) + ' seconds')

cols = list(ask.columns)
cols = [cols[0]] + [cols[-1]] + cols[1:-1]
ask = ask[cols]



mt4['datetime'] =  mt4[['date', 'time']].agg(' '.join, axis=1)
#this one might be fastest test on larger dataset
mt4['datetime'] =  mt4["date"] + mt4["time"]
#mt4['datetime'] = mt4[['date', 'time']][u'date'] + mt4[['date', 'time']][u'time']
# mt4['datetime'] = '+'.join(['date', 'time']][u'date'], [['date', 'time']][u'time'])
#fastest function? got ValueError: Invalid character while parsing month ('.', Index: 4)
#also need to import cisco8601 again
#mt4['datetime'] = mt4['datetime'].apply(lambda x: ciso8601.parse_datetime(x))

t1 = datetime.now()
def f1(datestr):
    return datetime(
        int(datestr[:4]),
        int(datestr[5:7]),
        int(datestr[8:10]),
        int(datestr[10:12]),
        int(datestr[13:15]),
    )
mt4['datetime'] = mt4['datetime'].apply(lambda x: f1(x))
t2 = datetime.now()
print('nested function algo took ' + str(t2-t1) + ' seconds')

# drop date and time string columns
mt4 = mt4.drop(['date', 'time'], axis=1)
#move datetime column to first column
cols = list(mt4.columns)
cols = [cols[-1]] + cols[:-1]
mt4 = mt4[cols]

#maybe use this function to fill missing values if faster? measure computation time
#for j in range(1, 7): if multiple months- add month index j inside datetime as well
for i in [0, 1]:
    ask_subset = ask[(ask['datetime'] >= datetime(2020, 6, 30, 23, 59) + timedelta(minutes=i)) & (ask['datetime'] < datetime(2020, 7, 1, 0, 0)  + timedelta(minutes=i))]
    # Let's create a row which we want to insert 
    row_number = len(mt4_6) + i
    # Starting value of upper half 
    start_upper = 0
    # End value of upper half 
    end_upper = row_number 
    # Start value of lower half 
    start_lower = row_number 
    # End value of lower half 
    end_lower = mt4.shape[0] 
    # Create a list of upper_half index 
    upper_half = range(start_upper, end_upper, 1) 
    # Create a list of lower_half index 
    lower_half = range(start_lower, end_lower, 1)
    # Increment the value of lower half by 1 
    lower_half = [x.__add__(1) for x in lower_half] 
    # Combine the two lists 
    index_ = upper_half + lower_half
    # Update the index of the dataframe 
    mt4.index = index_ 
    # Insert a row at the end- taking mean of values for row above and row below
    mt4.loc[row_number] = [ask_subset['datetime'].iloc[0], ask_subset['bid'].iloc[0], ask_subset['bid'].max(), ask_subset['bid'].min(), ask_subset['bid'].iloc[-1]]
    # Sort the index labels 
    mt4 = mt4.sort_index() 



## maybe you do this before converting to timestamp?
mt4['timedelta'] = mt4['datetime'].apply(lambda x: x.minute)
mt4['timedelta'] = mt4['timedelta'].diff() 
#pandas series.le() method also could work 
mt4['timedelta'] = np.where(mt4['timedelta'] < 0, mt4['timedelta']+60, mt4['timedelta'])
td = mt4['timedelta'][mt4['timedelta'] != 1][1:][::-1] 
mt4 = mt4.drop('timedelta', axis=1)
td = td.to_frame()
td = td.reset_index() 

# Let's create a row which we want to insert 
row_number = int(td.loc[0]['index'])
# Starting value of upper half 
start_upper = 0
# End value of upper half 
end_upper = row_number 
# Start value of lower half 
start_lower = row_number 
# End value of lower half 
end_lower = mt4.shape[0] 
# Create a list of upper_half index 
upper_half = range(start_upper, end_upper, 1) 
# Create a list of lower_half index 
lower_half = range(start_lower, end_lower, 1)
# Increment the value of lower half by 1 
lower_half = [x.__add__(1) for x in lower_half] 
# Combine the two lists 
index_ = upper_half + lower_half
# Update the index of the dataframe 
mt4.index = index_ 
# Insert a row at the end- taking mean of values for row above and row below
mt4.loc[row_number] = [mt4[row_number-1:row_number+1]['datetime'][row_number+1]-timedelta(minutes=1), mt4[row_number-1:row_number+1]['open_bid'].mean(), mt4[row_number-1:row_number+1]['high_bid'].mean(), mt4[row_number-1:row_number+1]['low_bid'].mean(), mt4[row_number-1:row_number+1]['close_bid'].mean()] 
# Sort the index labels 
mt4 = mt4.sort_index()   
mt4['timedelta'] = mt4['datetime'].apply(lambda x: x.minute)
mt4['timedelta'] = mt4['timedelta'].diff()  
mt4['timedelta'] = np.where(mt4['timedelta'] < 0, mt4['timedelta']+60, mt4['timedelta'])
td = mt4['timedelta'][mt4['timedelta'] != 1][1:][::-1] 
mt4 = mt4.drop('timedelta', axis=1)
td = td.to_frame()
td = td.reset_index() 

#repeat above loop taking just copying value for next row not taking mean of one above and one below- no need to keep halving
#datetime you subtract one from next row though just as above
#repeat loop until no more missing rows
while len(td) > 0:
    for i in range(0, len(td)):
        row_number = int(td.loc[i]['index'])
        start_upper = 0
        end_upper = row_number 
        start_lower = row_number 
        end_lower = mt4.shape[0] 
        upper_half = range(start_upper, end_upper, 1) 
        lower_half = range(start_lower, end_lower, 1)
        lower_half = [x.__add__(1) for x in lower_half] 
        index_ = upper_half + lower_half
        mt4.index = index_ 
        #this is the only row that is different from above
        mt4.loc[row_number] = [mt4[row_number-1:row_number+1]['datetime'][row_number+1]-timedelta(minutes=1), mt4.loc[row_number+1]['open_bid'], mt4.loc[row_number+1]['high_bid'], mt4.loc[row_number+1]['low_bid'], mt4.loc[row_number+1]['close_bid']]
        mt4 = mt4.sort_index()   
    mt4['timedelta'] = mt4['datetime'].apply(lambda x: x.minute)
    mt4['timedelta'] = mt4['timedelta'].diff()  
    mt4['timedelta'] = np.where(mt4['timedelta'] < 0, mt4['timedelta']+60, mt4['timedelta'])
    td = mt4['timedelta'][mt4['timedelta'] != 1][1:][::-1] 
    mt4 = mt4.drop('timedelta', axis=1)
    td = td.to_frame()
    td = td.reset_index() 


##create new dataframe with 15 minute bars
mt4_15m = mt4[mt4.index % 15 == 14].copy() 
# I get length mismatch error when changing index if i use this one mt4_15m = mt4.iloc[14::15, :].copy()
close_bid = mt4[mt4.index % 15 == 13]['close_bid'].copy()
close_bid.index = (close_bid.index - 13)/15
mt4_15m.index = (mt4_15m.index + 1)/15
mt4_15m['close_bid'] = close_bid
##substitute max highs and min closes for each 15 minute bar
high_bid = [max(mt4[:14]['high_bid'])]
low_bid = [min(mt4[:14]['low_bid'])]
for i in range(1, len(mt4_15m)):
    high_bid.append(max(mt4[i*15-1:i*15+14]['high_bid']))
    low_bid.append(min(mt4[i*15-1:i*15+14]['low_bid']))
mt4_15m['high_bid'] = high_bid
mt4_15m['low_bid'] = low_bid
mt4_15m['high_bid'] = mt4_15m['high_bid'].shift(-1)
mt4_15m['low_bid'] = mt4_15m['low_bid'].shift(-1)
mt4_15m.index -= 1


#create 1h bars
mt4_1h = mt4[mt4.index % 60 == 59].copy() 
close_bid = mt4[mt4.index % 60 == 58]['close_bid'].copy()
close_bid.index = (close_bid.index - 58)/60
mt4_1h.index = (mt4_1h.index + 1)/60
mt4_1h['close_bid'] = close_bid
##substitute max highs and min closes for each 1h bar
high_bid = [max(mt4[:59]['high_bid'])]
low_bid = [min(mt4[:59]['low_bid'])]
for i in range(1, len(mt4_1h)):
    high_bid.append(max(mt4[i*60-1:i*60+59]['high_bid']))
    low_bid.append(min(mt4[i*60-1:i*60+59]['low_bid']))
mt4_1h['high_bid'] = high_bid
mt4_1h['low_bid'] = low_bid
mt4_1h['high_bid'] = mt4_1h['high_bid'].shift(-1)
mt4_1h['low_bid'] = mt4_1h['low_bid'].shift(-1)
mt4_1h.index -= 1

#create 4h bars
mt4_4h = mt4[mt4.index % 240 == 239].copy() 
close_bid = mt4[mt4.index % 240 == 238]['close_bid'].copy()
close_bid.index = (close_bid.index - 238)/240
mt4_4h.index = (mt4_4h.index + 1)/240
mt4_4h['close_bid'] = close_bid
##substitute max highs and min closes for each 1h bar
high_bid = [max(mt4[:239]['high_bid'])]
low_bid = [min(mt4[:239]['low_bid'])]
for i in range(1, len(mt4_4h)):
    high_bid.append(max(mt4[i*240-1:i*240+239]['high_bid']))
    low_bid.append(min(mt4[i*240-1:i*240+239]['low_bid']))
mt4_4h['high_bid'] = high_bid
mt4_4h['low_bid'] = low_bid
mt4_4h['high_bid'] = mt4_4h['high_bid'].shift(-1)
mt4_4h['low_bid'] = mt4_4h['low_bid'].shift(-1)
mt4_4h.index -= 1

#create 1d bars with midnight as closing price
mt4_1d = mt4[mt4.index % 1440 == 1439].copy() 
close_bid = mt4[mt4.index % 1440 == 1438]['close_bid'].copy()
close_bid.index = (close_bid.index - 1438)/1440
mt4_1d.index = (mt4_1d.index + 1)/1440
mt4_1d['close_bid'] = close_bid
##substitute max highs and min closes for each 1h bar
high_bid = [max(mt4[:1439]['high_bid'])]
low_bid = [min(mt4[:1439]['low_bid'])]
for i in range(1, len(mt4_1d)):
    high_bid.append(max(mt4[i*1440-1:i*1440+1439]['high_bid']))
    low_bid.append(min(mt4[i*1440-1:i*1440+1439]['low_bid']))
mt4_1d['high_bid'] = high_bid
mt4_1d['low_bid'] = low_bid
mt4_1d['high_bid'] = mt4_1d['high_bid'].shift(-1)
mt4_1d['low_bid'] = mt4_1d['low_bid'].shift(-1)
mt4_1d.index -= 1