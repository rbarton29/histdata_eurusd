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

#figure out best way to download data from histdata.com, unzip files, move to forex_algos folder, 
#and delete duplicate files and txt files

#move multiple files at once
# mv HISTDATA_COM_* ~/iCloudDrive/python_programs/forex_algos
# cd ~/iCloudDrive/python_programs/forex_algos
# rm -f *.zip
# rm -f *.txt

# m="mv ~/Downloads/"
# a="HISTDATA_COM_"
# b='ASCII_'
# b1='MT_'
# t='_T'
# t2='_T_'
# t1='_M1'
# t3='_M1_'
# currency='EURUSD'
# currency1='GBPUSD'
# yr=2020
# mo=04
# d='~/iCloudDrive/python_programs/forex_algos'
# z='.zip'
# x='.txt'
# dat='DAT_'

# # this only prints commands doesn't run them
# ? echo ${m}${a}${b}${currency}${t}${yr}${mo}${z} ${d}
#  * echo ${m}${a}${b1}${currency}${t1}${yr}${mo}${z} ${d}
# #unzip file.zip
#  ! unzip echo ${a}${b}${currency}${t}${yr}${mo}${z}
# // rm echo ${dat}${b}${currency}${t2}${yr}${mo}${x}
# todo rm echo ${dat}${b1}${currency}${t3}${yr}${mo}${x}
# rm echo ${a}${b}${currency}${t}${yr}${mo}${z}
# rm echo ${a}${b1}${currency}${t1}${yr}${mo}${z}


# currency1='EURGBP'
# #this only prints commands doesn't run them
# echo ${m}${a}${b}${currency1}${t}${yr}${mo}${z} ${d}
# echo ${m}${a}${b1}${currency1}${t1}${yr}${mo}${z} ${d}
# #unzip file.zip
# unzip echo ${a}${b}${currency1}${t}${yr}${mo}${z}
# rm echo ${dat}${b}${currency1}${t2}${yr}${mo}${x}
# rm echo ${dat}${b1}${currency1}${t3}${yr}${mo}${x}
# rm echo ${a}${b}${currency1}${t}${yr}${mo}${z}
# rm echo ${a}${b1}${currency1}${t1}${yr}${mo}${z}

# HISTDATA_COM_MT_EURGBP_M1202007.zip



# cd ~/iCloudDrive/python_programs/forex_algos

#ipython
from datetime import datetime
from datetime import timedelta 

#if too many months for memory set up so each month runs one after the other and then save results to a dataframe
t1 = datetime.now()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#1m bar data
m_eurusd_20_08 = pd.read_csv('DAT_MT_EURUSD_M1_202008.csv')
m_eurusd_20_08.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_08 = m_eurusd_20_08.drop('vol', axis=1)
m_eurusd_20_07 = pd.read_csv('DAT_MT_EURUSD_M1_202007.csv')
m_eurusd_20_07.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_07 = m_eurusd_20_07.drop('vol', axis=1)
m_eurusd_20_06 = pd.read_csv('DAT_MT_EURUSD_M1_202006.csv')
m_eurusd_20_06.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_06 = m_eurusd_20_06.drop('vol', axis=1)
m_eurusd_20_05 = pd.read_csv('DAT_MT_EURUSD_M1_202005.csv')
m_eurusd_20_05.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_05 = m_eurusd_20_05.drop('vol', axis=1)
m_eurusd_20_04 = pd.read_csv('DAT_MT_EURUSD_M1_202004.csv')
m_eurusd_20_04.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_04 = m_eurusd_20_04.drop('vol', axis=1)
m_eurusd_20_03 = pd.read_csv('DAT_MT_EURUSD_M1_202003.csv')
m_eurusd_20_03.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_03 = m_eurusd_20_03.drop('vol', axis=1)
m_eurusd_20_02 = pd.read_csv('DAT_MT_EURUSD_M1_202002.csv')
m_eurusd_20_02.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_02 = m_eurusd_20_02.drop('vol', axis=1)
m_eurusd_20_01 = pd.read_csv('DAT_MT_EURUSD_M1_202001.csv')
m_eurusd_20_01.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_20_01 = m_eurusd_20_01.drop('vol', axis=1)
frames = [m_eurusd_20_01, m_eurusd_20_02, m_eurusd_20_03, m_eurusd_20_04, m_eurusd_20_05, m_eurusd_20_06, m_eurusd_20_07, m_eurusd_20_08]
#frames = [m_eurusd_20_06, m_eurusd_20_07]
m_eurusd_20 = pd.concat(frames, ignore_index = True)
m_eurusd_19 = pd.read_csv('DAT_MT_EURUSD_M1_2019.csv')
m_eurusd_19.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurusd_19 = m_eurusd_19.drop('vol', axis=1)

#name m_eurusd now it will save lots of headache in rest of files!
m_eurusd = m_eurusd_19


#tick data
t_eurusd_20_08 = pd.read_csv('DAT_ASCII_EURUSD_T_202008.csv')
t_eurusd_20_08.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_08 = t_eurusd_20_08.drop('vol', axis=1)  
t_eurusd_20_07 = pd.read_csv('DAT_ASCII_EURUSD_T_202007.csv')
t_eurusd_20_07.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_07 = t_eurusd_20_07.drop('vol', axis=1)  
t_eurusd_20_06 = pd.read_csv('DAT_ASCII_EURUSD_T_202006.csv')
t_eurusd_20_06.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_06 = t_eurusd_20_06.drop('vol', axis=1)
t_eurusd_20_05 = pd.read_csv('DAT_ASCII_EURUSD_T_202005.csv')
t_eurusd_20_05.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_05 = t_eurusd_20_05.drop('vol', axis=1)
t_eurusd_20_04 = pd.read_csv('DAT_ASCII_EURUSD_T_202004.csv')
t_eurusd_20_04.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_04 = t_eurusd_20_04.drop('vol', axis=1)  
t_eurusd_20_03 = pd.read_csv('DAT_ASCII_EURUSD_T_202003.csv')
t_eurusd_20_03.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_03 = t_eurusd_20_03.drop('vol', axis=1)  
t_eurusd_20_02 = pd.read_csv('DAT_ASCII_EURUSD_T_202002.csv')
t_eurusd_20_02.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_02 = t_eurusd_20_02.drop('vol', axis=1)
t_eurusd_20_01 = pd.read_csv('DAT_ASCII_EURUSD_T_202001.csv')
t_eurusd_20_01.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_20_01 = t_eurusd_20_01.drop('vol', axis=1)
frames = [t_eurusd_20_01, t_eurusd_20_02, t_eurusd_20_03, t_eurusd_20_04, t_eurusd_20_05, t_eurusd_20_06, t_eurusd_20_07, t_eurusd_20_08]
t_eurusd_20 = pd.concat(frames, ignore_index = True)

t_eurusd_19_12 = pd.read_csv('DAT_ASCII_EURUSD_T_201912.csv')
t_eurusd_19_12.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_12 = t_eurusd_19_12.drop('vol', axis=1)
t_eurusd_19_11 = pd.read_csv('DAT_ASCII_EURUSD_T_201911.csv')
t_eurusd_19_11.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_11 = t_eurusd_19_11.drop('vol', axis=1)
t_eurusd_19_10 = pd.read_csv('DAT_ASCII_EURUSD_T_201910.csv')
t_eurusd_19_10.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_10 = t_eurusd_19_10.drop('vol', axis=1)
t_eurusd_19_09 = pd.read_csv('DAT_ASCII_EURUSD_T_201909.csv')
t_eurusd_19_09.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_09 = t_eurusd_19_09.drop('vol', axis=1)
t_eurusd_19_08 = pd.read_csv('DAT_ASCII_EURUSD_T_201908.csv')
t_eurusd_19_08.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_08 = t_eurusd_19_08.drop('vol', axis=1)
t_eurusd_19_07 = pd.read_csv('DAT_ASCII_EURUSD_T_201907.csv')
t_eurusd_19_07.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_07 = t_eurusd_19_07.drop('vol', axis=1)
t_eurusd_19_06 = pd.read_csv('DAT_ASCII_EURUSD_T_201906.csv')
t_eurusd_19_06.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_06 = t_eurusd_19_06.drop('vol', axis=1)
t_eurusd_19_05 = pd.read_csv('DAT_ASCII_EURUSD_T_201905.csv')
t_eurusd_19_05.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_05 = t_eurusd_19_05.drop('vol', axis=1)
t_eurusd_19_04 = pd.read_csv('DAT_ASCII_EURUSD_T_201904.csv')
t_eurusd_19_04.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_04 = t_eurusd_19_04.drop('vol', axis=1)
t_eurusd_19_03 = pd.read_csv('DAT_ASCII_EURUSD_T_201903.csv')
t_eurusd_19_03.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_03 = t_eurusd_19_03.drop('vol', axis=1)
t_eurusd_19_02 = pd.read_csv('DAT_ASCII_EURUSD_T_201902.csv')
t_eurusd_19_02.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_02 = t_eurusd_19_02.drop('vol', axis=1)
t_eurusd_19_01 = pd.read_csv('DAT_ASCII_EURUSD_T_201901.csv')
t_eurusd_19_01.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurusd_19_01 = t_eurusd_19_01.drop('vol', axis=1)
frames = [t_eurusd_19_01, t_eurusd_19_02, t_eurusd_19_03, t_eurusd_19_04, t_eurusd_19_05, t_eurusd_19_06, t_eurusd_19_07, t_eurusd_19_08, 
t_eurusd_19_09, t_eurusd_19_10, t_eurusd_19_11, t_eurusd_19_12]
t_eurusd_19 = pd.concat(frames, ignore_index = True)

#name t_eurusd now it will save lots of headache in rest of files!
t_eurusd = t_eurusd_19

m_gbpusd_20_07 = pd.read_csv('DAT_MT_GBPUSD_M1_202007.csv')
m_gbpusd_20_07.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_gbpusd_20_07 = m_gbpusd_20_07.drop('vol', axis=1)
t_gbpusd_20_07 = pd.read_csv('DAT_ASCII_GBPUSD_T_202007.csv')
t_gbpusd_20_07.columns = ['datetime', 'bid', 'ask', 'vol']
t_gbpusd_20_07 = t_gbpusd_20_07.drop('vol', axis=1)

#I think I got the ASCII version instead of m_eurusd- uses ; not ,
m_eurgbp_20_07 = pd.read_csv('DAT_MT_EURGBP_M1_202007.csv')
m_eurgbp_20_07.columns = ['date', 'time', 'open_bid', 'high_bid', 'low_bid', 'close_bid', 'vol']
m_eurgbp_20_07 = m_eurgbp_20_07.drop('vol', axis=1)
t_eurgbp_20_07 = pd.read_csv('DAT_ASCII_EURGBP_T_202007.csv')
t_eurgbp_20_07.columns = ['datetime', 'bid', 'ask', 'vol']
t_eurgbp_20_07 = t_eurgbp_20_07.drop('vol', axis=1)

#algo is slow so create new column to save second/ms data- saving data this way could save computing time   
t_eurusd['secs'] = t_eurusd['datetime'].str[13:15].str.cat(t_eurusd['datetime'].str[15:], sep = '.') 
t2 = datetime.now()
print('importing data took ' + str(t2-t1) + ' seconds')
#0:00:43.086642 seconds with 2 months

#~39 secs with 7 months of eurusd
#converting secs took another 0:00:40.084223 seconds with 7 months of eurusd
#combined importing data took 0:01:31.889561 seconds

#importing data took 0:00:33.435185 seconds without parsing seconds
#ciso algo took 0:00:24.933073 seconds without parsing seconds- so you lose the data but save computing time

#format dates for t_eurusd_20
t1 = datetime.now()
import ciso8601
#only necessary if using cisco algo, double check it saves time with extra step- maybe necessary with multiple dataframes?
#t_eurusd['datetime'] = t_eurusd['datetime'].to_string()
t_eurusd['datetime'] = t_eurusd['datetime'].str[:-5]
##import cisco8601 function even faster apparently
t_eurusd['datetime'] = t_eurusd['datetime'].apply(lambda x: ciso8601.parse_datetime(x))
t2 = datetime.now()
print('ciso algo took ' + str(t2-t1) + ' seconds')
#ciso algo took 0:00:44.489232 seconds with 8 months


#format dates for m_eurusd_20 - also need to import ciso8601 again?
t1 = datetime.now()
#import ciso8601
m_eurusd['datetime'] =  m_eurusd["date"] + m_eurusd["time"]
m_eurusd['datetime'] = m_eurusd['datetime'].str.replace('.', '-')
m_eurusd['datetime'] = m_eurusd['datetime'].str[:10] + 'T' + m_eurusd['datetime'].str[10:]
m_eurusd['datetime'] = m_eurusd['datetime'].apply(lambda x: ciso8601.parse_datetime(x))
#drop date and time string columns
m_eurusd = m_eurusd.drop(['date', 'time'], axis=1)
#move datetime column to first column
cols = list(m_eurusd.columns)
cols = [cols[-1]] + cols[:-1]
m_eurusd = m_eurusd[cols]
t2 = datetime.now()
print('ciso algo took ' + str(t2-t1) + ' seconds')
#ciso algo took 0:00:00.910969 seconds w 8 months



the row numbers it needs to hit
248736 #len of file
i=1
218264 #sub 30472?- stay twice
i=2
185716 #sub 32550?- stay twice
i=3
154133 #sub 31584?
i=4
123969 #sub 30165?
i=5
92357 #sub 31613?
i=6
60354 #sub 32004?
i=7
31651 #sub 28704?
#first minute of Feb is empty dataframe- so run it twice  with j as 0 
m_eurusd.loc[row_number] = [t_eurusd_subset['datetime'].iloc[0] + timedelta(minutes=1), t_eurusd_subset['bid'].iloc[-1], t_eurusd_subset['bid'].iloc[-1], t_eurusd_subset['bid'].iloc[-1], t_eurusd_subset['bid'].iloc[-1]]
m_eurusd = m_eurusd.sort_index()
m_eurusd.loc[row_number] = [t_eurusd_subset['datetime'].iloc[0], t_eurusd_subset['bid'].iloc[0], t_eurusd_subset['bid'].max(), t_eurusd_subset['bid'].min(), t_eurusd_subset['bid'].iloc[-1]]




#only need to do this for 2020 not any completed years prior to that- filling in values at beginning and end of each month
t1 = datetime.now()
#len(m_eurusd_20['datetime'].dt.month.unique())- # of months, if more than one year doesn't count those months though
#maybe use this function to fill missing values if faster? measure computation time
#if multiple months- 7 is number of months- add index k for years
row_number = len(m_eurusd)
from calendar import monthrange
num_months = 8
for i in range(1, num_months):
    #2nd one is close
    #row_number = len(m_eurusd_20[(m_eurusd_20['datetime'] >= datetime(2020, i, 1, 0, 0)) & (m_eurusd_20['datetime'] <= datetime(2020, i, monthrange(2020, i)[1], 23, 59))])    
    #row_number = row_number + i - 1 - len(m_eurusd_20[(m_eurusd_20['datetime'] >= datetime(2020, num_months + 1 - i, 1, 0, 0)) & (m_eurusd_20['datetime'] <= datetime(2020, num_months + 1 - i, monthrange(2020, num_months + 1 - i)[1], 23, 59))])
    row_number = row_number + 1 - len(m_eurusd[(m_eurusd['datetime'] >= datetime(2020, num_months + 1 - i, 1, 0, 0)) & (m_eurusd['datetime'] <= datetime(2020, num_months + 1 - i, monthrange(2020, num_months + 1 - i)[1], 23, 59))])
    for j in [1, 0]:
        #make sure this works- returns empty df
        if datetime(2020, num_months - i, monthrange(2020, num_months - i)[1]).weekday() == 4:
            t_eurusd_subset = t_eurusd[(t_eurusd['datetime'] >= datetime(2020, num_months - i, monthrange(2020, num_months - i)[1], 16, 59) + timedelta(minutes=j)) & (t_eurusd['datetime'] < datetime(2020, num_months + 1 - i, 2, 17, 0)  + timedelta(minutes=j))]
        elif datetime(2020, num_months - i, monthrange(2020, num_months - i)[1]).weekday() == 5:
            t_eurusd_subset = t_eurusd[(t_eurusd['datetime'] >= datetime(2020, num_months - i, monthrange(2020, num_months - i)[1]-1, 16, 59) + timedelta(minutes=j)) & (t_eurusd['datetime'] < datetime(2020, num_months + 1 - i, 1, 17, 0)  + timedelta(minutes=j))]            
        else:
            t_eurusd_subset = t_eurusd[(t_eurusd['datetime'] >= datetime(2020, num_months - i, monthrange(2020, num_months - i)[1], 23, 59) + timedelta(minutes=j)) & (t_eurusd['datetime'] < datetime(2020, num_months + 1 - i, 1, 0, 0)  + timedelta(minutes=j))]
        # Let's create a row which we want to insert- number of bar data points in the month df
        #row_number = row_number - len(m_eurusd[(m_eurusd['datetime'] >= datetime(2020, i, 1, 0, 0)) & (m_eurusd['datetime'] <= datetime(2020, i, monthrange(2020, i)[1], 23, 59))]) + j
        # Starting value of upper half 
        start_upper = 0
        # End value of upper half 
        end_upper = row_number 
        # Start value of lower half 
        start_lower = row_number 
        # End value of lower half 
        end_lower = m_eurusd.shape[0] 
        # Create a list of upper_half index 
        upper_half = range(start_upper, end_upper, 1) 
        # Create a list of lower_half index 
        lower_half = range(start_lower, end_lower, 1)
        # Increment the value of lower half by 1 
        lower_half = [x.__add__(1) for x in lower_half] 
        # Combine the two lists 
        index_ = upper_half + lower_half
        # Update the index of the dataframe 
        m_eurusd.index = index_ 
        # Insert a row at the end- taking mean of values for row above and row below
        m_eurusd.loc[row_number] = [t_eurusd_subset['datetime'].iloc[0], t_eurusd_subset['bid'].iloc[0], t_eurusd_subset['bid'].max(), t_eurusd_subset['bid'].min(), t_eurusd_subset['bid'].iloc[-1]]
        # Sort the index labels 
        m_eurusd = m_eurusd.sort_index()



# m_eurusd_20 = pd.concat([m_eurusd_20.iloc[31651:60354],
# m_eurusd_20.reindex([60361, 60362, 60355, 60356, 60357, 60358, 60359, 60360]),
# m_eurusd_20.iloc[60362:92359],
# m_eurusd_20.reindex([92363, 92364, 92360, 92361, 92362]),
# m_eurusd_20.iloc[92364:123973],
# m_eurusd_20.reindex([123975, 123976, 123974]), 
# m_eurusd_20.iloc[123976:]])

# m_eurusd_20 = m_eurusd_20.reset_index(drop=True)



#len(m_eurusd[(m_eurusd['datetime'] >= datetime(2020, i, 1, 0, 0)) & (m_eurusd['datetime'] < datetime(2020, i, monthrange(2020, i)[1], 23, 59))])
# d = 0, 2, 
# i = 1, 2, 3, 

# t1 = datetime.now()
# #len(m_eurusd['datetime'].dt.month.unique())- # of months, if more than one year doesn't count those months though
# #maybe use this function to fill missing values if faster? measure computation time
# #if multiple months- 7 is number of months- add index k for years
# for j in [0, 1]:
#     #make sure this works- returns empty df
#     t_eurusd_subset = t_eurusd[(t_eurusd['datetime'] >= datetime(2020, 6, 30, 23, 59) + timedelta(minutes=j)) & (t_eurusd['datetime'] < datetime(2020, 7, 1, 0, 0)  + timedelta(minutes=j))]
#     # Let's create a row which we want to insert- number of bar data points in the month df
#     row_number = len(m_eurusd_20_06) + j
#     # Starting value of upper half 
#     start_upper = 0
#     # End value of upper half 
#     end_upper = row_number 
#     # Start value of lower half 
#     start_lower = row_number
#     # End value of lower half 
#     end_lower = m_eurusd.shape[0] 
#     # Create a list of upper_half index 
#     upper_half = range(start_upper, end_upper, 1) 
#     # Create a list of lower_half index 
#     lower_half = range(start_lower, end_lower, 1)
#     # Increment the value of lower half by 1 
#     lower_half = [x.__add__(1) for x in lower_half] 
#     # Combine the two lists 
#     index_ = upper_half + lower_half
#     # Update the index of the dataframe 
#     m_eurusd.index = index_ 
#     # Insert a row at the end- taking mean of values for row above and row below
#     m_eurusd.loc[row_number] = [t_eurusd_subset['datetime'].iloc[0], t_eurusd_subset['bid'].iloc[0], t_eurusd_subset['bid'].max(), t_eurusd_subset['bid'].min(), t_eurusd_subset['bid'].iloc[-1]]
#     # Sort the index labels 
#     m_eurusd = m_eurusd.sort_index() 






#this you need to do for all years though- fills in missing values throughout dataframe where tick volume is down

## maybe you do this before converting to timestamp?
m_eurusd['timedelta'] = m_eurusd['datetime'].apply(lambda x: x.minute)
m_eurusd['timedelta'] = m_eurusd['timedelta'].diff() 
#pandas series.le() method also could work 
m_eurusd['timedelta'] = np.where(m_eurusd['timedelta'] < 0, m_eurusd['timedelta']+60, m_eurusd['timedelta'])
td = m_eurusd['timedelta'][m_eurusd['timedelta'] != 1][1:][::-1] 
m_eurusd = m_eurusd.drop('timedelta', axis=1)
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
end_lower = m_eurusd.shape[0] 
# Create a list of upper_half index 
upper_half = range(start_upper, end_upper, 1) 
# Create a list of lower_half index 
lower_half = range(start_lower, end_lower, 1)
# Increment the value of lower half by 1 
lower_half = [x.__add__(1) for x in lower_half] 
# Combine the two lists 
index_ = upper_half + lower_half
# Update the index of the dataframe 
m_eurusd.index = index_ 
# Insert a row at the end- taking mean of values for row above and row below
m_eurusd.loc[row_number] = [m_eurusd[row_number-1:row_number+1]['datetime'][row_number+1]-timedelta(minutes=1), m_eurusd[row_number-1:row_number+1]['open_bid'].mean(), m_eurusd[row_number-1:row_number+1]['high_bid'].mean(), m_eurusd[row_number-1:row_number+1]['low_bid'].mean(), m_eurusd[row_number-1:row_number+1]['close_bid'].mean()] 
# Sort the index labels 
m_eurusd = m_eurusd.sort_index()   
m_eurusd['timedelta'] = m_eurusd['datetime'].apply(lambda x: x.minute)
m_eurusd['timedelta'] = m_eurusd['timedelta'].diff()  
m_eurusd['timedelta'] = np.where(m_eurusd['timedelta'] < 0, m_eurusd['timedelta']+60, m_eurusd['timedelta'])
td = m_eurusd['timedelta'][m_eurusd['timedelta'] != 1][1:][::-1] 
m_eurusd = m_eurusd.drop('timedelta', axis=1)
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
        end_lower = m_eurusd.shape[0] 
        upper_half = range(start_upper, end_upper, 1) 
        lower_half = range(start_lower, end_lower, 1)
        lower_half = [x.__add__(1) for x in lower_half] 
        index_ = upper_half + lower_half
        m_eurusd.index = index_ 
        #this is the only row that is different from above
        m_eurusd.loc[row_number] = [m_eurusd[row_number-1:row_number+1]['datetime'][row_number+1]-timedelta(minutes=1), m_eurusd.loc[row_number+1]['open_bid'], m_eurusd.loc[row_number+1]['high_bid'], m_eurusd.loc[row_number+1]['low_bid'], m_eurusd.loc[row_number+1]['close_bid']]
        
        #this is one I am working on- just takes previous value
        #m_eurusd.loc[row_number] = [m_eurusd[row_number-1:row_number+1]['datetime'][row_number+1]-timedelta(minutes=1), m_eurusd.loc[row_number-1]['open_bid'], m_eurusd.loc[row_number-1]['open_bid'], m_eurusd_20.loc[row_number-1]['open_bid'], m_eurusd.loc[row_number-1]['open_bid']]
        m_eurusd = m_eurusd.sort_index()   
    m_eurusd['timedelta'] = m_eurusd['datetime'].apply(lambda x: x.minute)
    m_eurusd['timedelta'] = m_eurusd['timedelta'].diff()  
    m_eurusd['timedelta'] = np.where(m_eurusd['timedelta'] < 0, m_eurusd['timedelta']+60, m_eurusd['timedelta'])
    td = m_eurusd['timedelta'][m_eurusd['timedelta'] != 1][1:][::-1] 
    m_eurusd = m_eurusd.drop('timedelta', axis=1)
    td = td.to_frame()
    td = td.reset_index() 
t2 = datetime.now()
print('fill values script took ' + str(t2-t1) + ' seconds')
#fill values script took 0:00:14.230391 seconds