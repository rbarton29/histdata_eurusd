#create charts

#here is code to delete duplicates on 2019-10-27 19:00:00
m_eurusd = m_eurusd.drop_duplicates()


#run m_eurusd.head() for whichever year you are trying to run and see what minute it starts at, it varies by the year 
#and you need to adjust this to create charts so name adj whatever the minute is for the first row of year
adj = 3

##create new dataframe with 15 minute bars
t1 = datetime.now()
m_eurusd_15m = m_eurusd[m_eurusd.index % 15 == 14].copy() 
# I get length mismatch error when changing index if i use this one m_eurusd_15m = m_eurusd.iloc[14::15, :].copy()
close_bid_15m = m_eurusd[m_eurusd.index % 15 == 13]['close_bid'].copy()
close_bid_15m.index = (close_bid_15m.index - 13)/15
m_eurusd_15m.index = (m_eurusd_15m.index + 1)/15
m_eurusd_15m['close_bid_15m'] = close_bid_15m
##substitute max highs and min closes for each 15 minute bar
high_bid_15m = [max(m_eurusd[:14]['high_bid'])]
low_bid_15m = [min(m_eurusd[:14]['low_bid'])]
for i in range(1, len(m_eurusd_15m)):
    high_bid_15m.append(max(m_eurusd[i*15-1:i*15+14]['high_bid']))
    low_bid_15m.append(min(m_eurusd[i*15-1:i*15+14]['low_bid']))
m_eurusd_15m['high_bid_15m'] = high_bid_15m
m_eurusd_15m['low_bid_15m'] = low_bid_15m
m_eurusd_15m['high_bid_15m'] = m_eurusd_15m['high_bid_15m'].shift(-1)
m_eurusd_15m['low_bid_15m'] = m_eurusd_15m['low_bid_15m'].shift(-1)
m_eurusd_15m.index -= 1
m_eurusd_15m['open_bid_15m'] = m_eurusd_15m['open_bid']
m_eurusd_15m = m_eurusd_15m.drop(['open_bid', 'high_bid', 'low_bid', 'close_bid'], axis=1)
cols = list(m_eurusd_15m.columns)
cols = ['datetime', 'open_bid_15m', 'high_bid_15m', 'low_bid_15m', 'close_bid_15m']
#work on this
# cols = [cols[-1]] + cols[:-1]
m_eurusd_15m = m_eurusd_15m[cols]


##create new dataframe with 15 minute bars
t1 = datetime.now()
m_eurusd_15m = m_eurusd[m_eurusd.index % 15 == 15 - adj].copy() 
# I get length mismatch error when changing index if i use this one m_eurusd_15m = m_eurusd.iloc[14::15, :].copy()
close_bid_15m = m_eurusd[m_eurusd.index % 15 == (14 - adj)]['close_bid'].copy()
close_bid_15m.index = (close_bid_15m.index - (14 - adj))/15
m_eurusd_15m.index = (m_eurusd_15m.index + adj)/15
m_eurusd_15m['close_bid_15m'] = close_bid_15m
##substitute max highs and min closes for each 15 minute bar
high_bid_15m = [max(m_eurusd[:(15 - adj)]['high_bid'])]
low_bid_15m = [min(m_eurusd[:(15 - adj)]['low_bid'])]
for i in range(1, len(m_eurusd_15m)):
    high_bid_15m.append(max(m_eurusd[i*15-adj:i*15+(15-adj)]['high_bid']))
    low_bid_15m.append(min(m_eurusd[i*15-adj:i*15+(15-adj)]['low_bid']))
m_eurusd_15m['high_bid_15m'] = high_bid_15m
m_eurusd_15m['low_bid_15m'] = low_bid_15m
m_eurusd_15m['high_bid_15m'] = m_eurusd_15m['high_bid_15m'].shift(-1)
m_eurusd_15m['low_bid_15m'] = m_eurusd_15m['low_bid_15m'].shift(-1)
m_eurusd_15m.index -= 1
m_eurusd_15m['open_bid_15m'] = m_eurusd_15m['open_bid']
m_eurusd_15m = m_eurusd_15m.drop(['open_bid', 'high_bid', 'low_bid', 'close_bid'], axis=1)
cols = list(m_eurusd_15m.columns)
cols = ['datetime', 'open_bid_15m', 'high_bid_15m', 'low_bid_15m', 'close_bid_15m']
#work on this
# cols = [cols[-1]] + cols[:-1]
m_eurusd_15m = m_eurusd_15m[cols]




#create 1h bars
m_eurusd_1h = m_eurusd[m_eurusd.index % 60 == (60 - adj)].copy() 
close_bid_1h = m_eurusd[m_eurusd.index % 60 == (59 - adj)]['close_bid'].copy()
close_bid_1h.index = (close_bid_1h.index - (59 - adj))/60
m_eurusd_1h.index = (m_eurusd_1h.index + adj)/60
m_eurusd_1h['close_bid_1h'] = close_bid_1h
##substitute max highs and min closes for each 1h bar
high_bid_1h = [max(m_eurusd[:(60 - adj)]['high_bid'])]
low_bid_1h = [min(m_eurusd[:(60 - adj)]['low_bid'])]
for i in range(1, len(m_eurusd_1h)):
    high_bid_1h.append(max(m_eurusd[i*60-adj:i*60+(60 - adj)]['high_bid']))
    low_bid_1h.append(min(m_eurusd[i*60-adj:i*60+(60 - adj)]['low_bid']))
m_eurusd_1h['high_bid_1h'] = high_bid_1h
m_eurusd_1h['low_bid_1h'] = low_bid_1h
m_eurusd_1h['high_bid_1h'] = m_eurusd_1h['high_bid_1h'].shift(-1)
m_eurusd_1h['low_bid_1h'] = m_eurusd_1h['low_bid_1h'].shift(-1)
m_eurusd_1h.index -= 1
m_eurusd_1h['open_bid_1h'] = m_eurusd_1h['open_bid']
m_eurusd_1h = m_eurusd_1h.drop(['open_bid', 'high_bid', 'low_bid', 'close_bid'], axis=1)
cols = list(m_eurusd_1h.columns)
cols = ['datetime', 'open_bid_1h', 'high_bid_1h', 'low_bid_1h', 'close_bid_1h']
#cols = [cols[0]] + [cols[-1]] + cols[1:4]
m_eurusd_1h = m_eurusd_1h[cols]

m_eurusd_1h['hour'] = m_eurusd_1h['datetime'].apply(lambda x: x.hour)
m_eurusd_1h['timedelta'] = m_eurusd_1h['hour'].diff()
#m_eurusd_1h['hour'] = np.where(m_eurusd_1h['timedelta'] < 0, m_eurusd['timedelta']+60, m_eurusd['timedelta'])
m_eurusd_1h[m_eurusd_1h['timedelta'] == 0]
                datetime  open_bid_1h  high_bid_1h  low_bid_1h  close_bid_1h  \
1151 2019-03-10 16:00:00      1.12316      1.12360     1.12304       1.12336   
5098 2019-10-27 16:00:00      1.10800      1.10807     1.10774       1.10792   


#create 4h bars
#180 - adj not 240 - adj because it starts at 17th hour
#end of weeks sometimes switch the hours- screws up at row 288- it seems that on sunday 3/10/19 that the markets opened at 16:00 not 17:00
m_eurusd_4h = m_eurusd[m_eurusd.index % 240 == (180 - adj)].copy() 
close_bid_4h = m_eurusd[m_eurusd.index % 240 == (179 - adj)]['close_bid'].copy()
close_bid_4h.index = (close_bid_4h.index - (180 - adj))/240
m_eurusd_4h.index = (m_eurusd_4h.index + adj)/240
m_eurusd_4h['close_bid_4h'] = close_bid_4h
##substitute max highs and min closes for each 1h bar
high_bid_4h = [max(m_eurusd[:(180 - adj)]['high_bid'])]
low_bid_4h = [min(m_eurusd[:(180 - adj)]['low_bid'])]
for i in range(1, len(m_eurusd_4h)):
    high_bid_4h.append(max(m_eurusd[i*240-(60 + adj):i*240+(180 - adj)]['high_bid']))
    low_bid_4h.append(min(m_eurusd[i*240-(60 + adj):i*240+(180 - adj)]['low_bid']))
m_eurusd_4h['high_bid_4h'] = high_bid_4h
m_eurusd_4h['low_bid_4h'] = low_bid_4h
# m_eurusd_4h['high_bid_4h'] = m_eurusd_4h['high_bid_4h'].shift(-1)
# m_eurusd_4h['low_bid_4h'] = m_eurusd_4h['low_bid_4h'].shift(-1)


#finish this later- can't think right now- highs and lows you have to leave with 1m m_eurusd though
m_eurusd_4h = m_eurusd_1h[m_eurusd_1h['hour'] % 4 == 0].copy() 
#maybe delete rows 1151 and 5098 but still need to use closing prices from those rows?
#or leave it but insert those rows back
close_bid_4h = m_eurusd_1h[m_eurusd_1h['hour'] % 4 == 3]['close_bid_1h'].copy()
close_bid_4h.index = (close_bid_4h.index - 1)/4
m_eurusd_4h.index = (m_eurusd_4h.index + 2)/4
#ValueError: cannot reindex from a duplicate axis- I am just going to try deleting 3/8/16:00 and see what happens- 
# I don't know why still not working
m_eurusd_4h.drop(287, axis=0, inplace=True)
m_eurusd_4h.loc[287] = m_eurusd_1h.loc[1151]
m_eurusd_4h = m_eurusd_4h.reset_index()
m_eurusd_4h['close_bid_4h'] = close_bid_4h
##substitute max highs and min closes for each 1h bar
high_bid_4h = [max(m_eurusd_1h[:2]['high_bid'])]
low_bid_4h = [min(m_eurusd_1h[:2]['low_bid'])]
#or do range(1, 288)?
for i in range(1, len(m_eurusd_4h)):
    high_bid_4h.append(max(m_eurusd_1h[i*4-2:i*4+2]['high_bid']))
    low_bid_4h.append(min(m_eurusd_1h[i*4-2:i*4+2]['low_bid']))
m_eurusd_4h['high_bid_4h'] = high_bid_4h
m_eurusd_4h['low_bid_4h'] = low_bid_4h




#create 1d bars with midnight as closing price
#1020 - adj not 1440 - adj because it starts at 17th hour
m_eurusd_1d = m_eurusd[m_eurusd.index % 1440 == (1020 - adj)].copy() 
close_bid_1d = m_eurusd[m_eurusd.index % 1440 == (1019 - adj)]['close_bid'].copy()
close_bid_1d.index = (close_bid_1d.index - (1019 - adj))/1440
m_eurusd_1d.index = (m_eurusd_1d.index + adj)/1440
m_eurusd_1d['close_bid_1d'] = close_bid_1d
##substitute max highs and min closes for each 1h bar
high_bid_1d = [max(m_eurusd[:(1020 - adj)]['high_bid'])]
low_bid_1d = [min(m_eurusd[:(1020 - adj)]['low_bid'])]
for i in range(1, len(m_eurusd_1d)):
    high_bid_1d.append(max(m_eurusd[i*1440-(420 + adj):i*1440+(1020 - adj)]['high_bid']))
    low_bid_1d.append(min(m_eurusd[i*1440-(420 + adj):i*1440+(1020 - adj)]['low_bid']))
m_eurusd_1d['high_bid_1d'] = high_bid_1d
m_eurusd_1d['low_bid_1d'] = low_bid_1d
# m_eurusd_1d['high_bid_1d'] = m_eurusd_1d['high_bid_1d'].shift(-1)
# m_eurusd_1d['low_bid_1d'] = m_eurusd_1d['low_bid_1d'].shift(-1)
# m_eurusd_1d.index -= 1
t2 = datetime.now()
print('create 4 new bar dataframes script took ' + str(t2-t1) + ' seconds')
#create 4 new bar dataframes script took 0:00:03.180932 seconds with 2 months
#create 4 new bar dataframes script took 0:00:09.146252 seconds with 6 months