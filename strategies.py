##for algo incorporate ML, linear, logistic, polynomial regression
##estimate volume based on tickgaps, price moves, and spreads
##write script to detect when news events are based on technicals
##arbitrage opportunity?
##import fundamentals from other data sources
##alternative data sources in forex markets?
##look at technicals from commodity charts and compute correlation/causations
##factor in price moves with large orders
##factor in economic data like interest rates and stuff
##weighted basket of currencies?
    ##generate heatmap with seaborn to see highly correlated assets

t1 = datetime.now()
import ciso8601
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

def convert_datetime_m(m_df):
    import ciso8601
    m_df['datetime'] =  m_df["date"] + m_df["time"]
    m_df['datetime'] = m_df['datetime'].str.replace('.', '-')
    m_df['datetime'] = m_df['datetime'].str[:10] + 'T' + m_df['datetime'].str[10:]
    m_df['datetime'] = m_df['datetime'].apply(lambda x: ciso8601.parse_datetime(x))
    #drop date and time string columns
    m_df = m_df.drop(['date', 'time'], axis=1)
    #move datetime column to first column
    cols = list(m_df.columns)
    cols = [cols[-1]] + cols[:-1]
    m_df = m_df[cols]
    return m_df

convert_datetime_m(m_eurusd_20_07)
convert_datetime_m(m_gbpusd_20_07)
convert_datetime_m(m_eurgbp_20_07)

def convert_datetime_t(t_df):
    t1 = datetime.now()
    import ciso8601
    t_df['secs'] = t_df['datetime'].str[13:15].str.cat(t_df['datetime'].str[15:], sep = '.') 
    #only necessary if using cisco algo, double check it saves time with extra step
    #t_df['datetime'] = t_df['datetime'].to_string()
    t_df['datetime'] = t_df['datetime'].str[:-5]
    ##import cisco8601 function even faster apparently
    t_df['datetime'] = t_df['datetime'].apply(lambda x: ciso8601.parse_datetime(x))
    cols = list(t_df.columns)
    cols = [cols[0]] + [cols[-1]] + cols[1:-1]
    t_df = t_df[cols]
    t2 = datetime.now()
    print('ciso algo took ' + str(t2-t1) + ' seconds')
    return t_df

convert_datetime_t(t_eurusd_20_07)
convert_datetime_t(t_gbpusd_20_07)
convert_datetime_t(t_eurgbp_20_07)

##triangulation
m_eurusd_20_07['close_bid']
m_gbpusd_20_07['close_bid']
m_eurusd_20_07['eurgbp_est'] = m_eurusd_20_07['close_bid']/m_gbpusd_20_07['close_bid']
m_eurusd_20_07 = m_eurgbp_20_07['close_bid']

#$/eur/($/gbp) = gbp/eur
#we need to know when the t_eurusd of the actual price < the bid of the estimate 
#or when the bid of the actual price < the t_eurusd of the estimate
m_eurusd_20_07[m_eurusd_20_07['eurgbp_est'] > m_eurusd_20_07['eurgbp_actual']] 

t_eurusd_20_07['eurgbp__bid_est'] = t_eurusd_20_07['bid']/t_gbpusd_20_07['bid']
t_eurgbp_20_07[:100][t_eurgbp_20_07['ask'] < 0.907387]

for i in range(0, len(m_eurusd_20_07)):
    if i == 0:
        t_eurusd_20_07_subset = t_eurusd_20_07[t_eurusd_20_07['datetime'] < (m_eurusd_20_07['datetime'][i+1] - timedelta(minutes=1))].copy()
    else:
        t_eurusd_20_07_subset = t_eurusd_20_07[(t_eurusd_20_07['datetime'] < (m_eurusd_20_07['datetime'][i+1] - timedelta(minutes=1))) & (t_eurusd_20_07['datetime'] >= (m_eurusd_20_07['datetime'][i] - timedelta(minutes=1)))].copy()
    m_eurusd_20_07['close_ask'].iloc[i] = t_eurusd_20_07_subset['ask'].iloc[-1]

# m_eurusd_20_07['open_ask'] = t_eurusd_20_07['ask'].iloc[0]
# for i in range(1, len(m_eurusd_20_07)):
#     counter = 0
#     if t_eurusd_20_07['datetime'].iloc[counter + 1].minute > t_eurusd_20_07['datetime'].iloc[counter].minute:
#         m_eurusd_20_07['open_ask'].iloc[i] = t_eurusd_20_07['ask'].iloc[counter + 1]
#     counter += 1

##estimate trading volume with spread
t_eurusd['spread'] = t_eurusd['ask'] - t_eurusd['bid']
t_eurusd['mid'] = (t_eurusd['ask'] + t_eurusd['bid'])/2
t_eurusd['spread_volume'] = (t_eurusd['spread'] - t_eurusd['spread'].mean())/(t_eurusd['spread'].max() - t_eurusd['spread'].min())
t_eurusd['norm_volume'] = (t_eurusd['spread'] - t_eurusd['spread'].mean())/t_eurusd['spread'].std()

# of ticks in that minute- error 'Series' object has no attribute 'year' and using lambda functions too slow
unique_dts = pd.Series(t_eurusd['datetime'].unique())

num_unique_dts = []
for i in range(0, len(unique_dts)):
    num_unique_dts.append(len(t_eurusd['datetime'][t_eurusd['datetime'] == unique_dts[i]]))

#maybe use groupby function
# t_eurusd['tick_volume'] = len(t_eurusd[t_eurusd['datetime'] == datetime(t_eurusd['datetime'].year, t_eurusd['datetime'].month, t_eurusd['datetime'].day, t_eurusd['datetime'].hour, t_eurusd['datetime'].minute, t_eurusd['datetime'].second)])

#distance from one t_eurusd tick to the next, to help measure volatility- maybe incorporate average between bid and ask
t_eurusd['tick_delta'] = abs(t_eurusd['ask'].diff())



# t_eurusd['price_volume'] = #total price movement per minute (counting retraces) in past 15 minutes?
#abs(t_eurusd.groupby('datetime')['t_eurusd'].diff())
#if sudden movement though and on the hour maybe in just past minute and trigger news event


#create column called market sentiment that estimates current market sentiment (where market is estimated to go)
    #based on the general direction of the market over the past 24 hours or so?
#no movement or reverse direction would be 0 where avg positive is 1, avg negative is -1
#t_eurusd['market_sentiment'] = 

#create column that predicts probability of upside move, similar to market sentiment

#create column called 'weekday' that returns the day of week in EDT from Sunday-Friday
t_eurusd['weekday'] = t_eurusd['datetime'].dt.dayofweek

# In [63]: t_eurusd['spread'][t_eurusd['weekday'] == 0].mean()
# Out[63]: 3.292005667843843e-05
# In [64]: t_eurusd['spread'][t_eurusd['weekday'] == 1].mean()
# Out[64]: 3.323179781270987e-05
# In [65]: t_eurusd['spread'][t_eurusd['weekday'] == 2].mean()
# Out[65]: 3.311703651282675e-05
# In [66]: t_eurusd['spread'][t_eurusd['weekday'] == 3].mean()
# Out[66]: 3.410373132674375e-05
# In [67]: t_eurusd['spread'][t_eurusd['weekday'] == 4].mean()
# Out[67]: 3.882244618283315e-05
# In [69]: t_eurusd['spread'][t_eurusd['weekday'] == 6].mean()
# Out[69]: 4.329351262902321e-05

# create column called 'market open' where it returns 0 if both markets closed, 1 if one is open and 2 if both markets are open
t_eurusd['market_open'] = np.where(t_eurusd['datetime'].dt.hour>16, 0, np.where(t_eurusd['datetime'].dt.hour>11, 1, np.where(t_eurusd['datetime'].dt.hour>7, 2, np.where(t_eurusd['datetime'].dt.hour>2, 1, 0))))

# In [55]: t_eurusd['spread'][t_eurusd['market_open'] == 2].mean()
# Out[55]: 3.139443428447379e-05
# In [56]: t_eurusd['spread'][t_eurusd['market_open'] == 1].mean()
# Out[56]: 3.4161425250751734e-05
# In [57]: t_eurusd['spread'][t_eurusd['market_open'] == 0].mean()
# Out[57]: 3.9635800820128725e-05

#combine above with weekday but look at other volatility measures than spread as well

#create column called 'news event' where a news event is (likely) taking place
# most news events have high volume initially that trails off
# at least one market must be open if it is a scheduled event
#every now and then a global sudden event can trigger volatility across all markets
#some news events are speaking and others are economic releases so maybe two columns then?

#t_eurusd['news event'] = 




#m_eurusd_15m['sma_20' + '_1h'] = newdf['sma_20']

##double check this works and try to find a faster algo
# for j in [0, 1, 2]
#     for i in range(0, len(m_eurusd_15m)):    
#         if newdf.index % 4 == j:
#             newdf['open_bid' + '_1h'][i] = m_eurusd_15m['open_bid'][i]

# m_eurusd_15m['sma_20_50_crossover'] = np.where(m_eurusd_15m['sma_20_15m'] > m_eurusd_15m['sma_50_15m'], np.where(m_eurusd_15m['sma_20_15m'] < m_eurusd_15m['sma_50_15m'], -1, 0))
# m_eurusd_15m[50:].where(m_eurusd_15m['sma_20_15m']>m_eurusd_15m['sma_50_15m'], m_eurusd_15m['sma_20_50_crossover'] = 1, m_eurusd_15m['sma_20_50_crossover'] = -1)




##need to convert pandas timestamps back to string also plot won't show again
# y = m_eurusd_4h['close_bid']
# x = m_eurusd_4h['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
# # or x = range(0, len(y))

# plt.scatter(x, y)
# plt.show()

##Machine Learning Algorithms- create new tab
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_absolute_error
model = LinearRegression()


##compute slopes of SMAs (linear regression on closing prices)
from scipy import stats

#x = m_eurusd_15m['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
y = m_eurusd_15m['close_bid']
x = range(0, len(y))

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))
##figure out how to answer: what does a better job of predicting the next y for given x: mymodel or past y

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

##compute other indicators as well
## build ML model to find best indicators and maybe when to use which

#because 1st 50 rows are NAN
train = m_eurusd_15m[50:][m_eurusd_15m['datetime'] < datetime(2020, 07, 18)]
test = m_eurusd_15m[m_eurusd_15m['datetime'] > datetime(2020, 07, 18)]

model.fit(train[['sma_20_15m']], train['close_bid'])
predictions = model.predict(test[['sma_20_15m']])
mae = mean_absolute_error(test['close_bid'], predictions)
mse = np.sqrt(mae)




##STRATEGY SECTION
##once I combine charts of different time frames, I may need to convert back to one minute charts and get rid of timedelta
#I changed m_eurusd_15m chart to m_eurusd_1h

##Indicators
##compute SMAs 20, 50, 200?
m_eurusd_15m['sma_20_15m'] = m_eurusd_15m['close_bid_15m'].rolling(window=20).mean().shift(1, axis=0)
m_eurusd_15m['sma_50_15m'] = m_eurusd_15m['close_bid_15m'].rolling(window=50).mean().shift(1, axis=0)
m_eurusd_15m['sma_200_15m'] = m_eurusd_15m['close_bid_15m'].rolling(window=200).mean().shift(1, axis=0)

#what if set to 0 not np.nan?
m_eurusd_15m['sma_20_50_co_15m'] = np.nan
m_eurusd_15m['sma_20_50_co_15m'] = m_eurusd_15m['sma_20_50_co_15m'].mask(m_eurusd_15m['sma_20_15m'] > m_eurusd_15m['sma_50_15m'], 1)
m_eurusd_15m['sma_20_50_co_15m'] = m_eurusd_15m['sma_20_50_co_15m'].mask(m_eurusd_15m['sma_20_15m'] < m_eurusd_15m['sma_50_15m'], -1)

m_eurusd_1h['sma_20_1h'] = m_eurusd_1h['close_bid_1h'].rolling(window=20).mean().shift(1, axis=0)
m_eurusd_1h['sma_50_1h'] = m_eurusd_1h['close_bid_1h'].rolling(window=50).mean().shift(1, axis=0)
m_eurusd_1h['sma_200_1h'] = m_eurusd_1h['close_bid_1h'].rolling(window=200).mean().shift(1, axis=0)
m_eurusd_1h['sma_20_50_co_1h'] = np.nan
m_eurusd_1h['sma_20_50_co_1h'] = m_eurusd_1h['sma_20_50_co_1h'].mask(m_eurusd_1h['sma_20_1h'] > m_eurusd_1h['sma_50_1h'], 1)
m_eurusd_1h['sma_20_50_co_1h'] = m_eurusd_1h['sma_20_50_co_1h'].mask(m_eurusd_1h['sma_20_1h'] < m_eurusd_1h['sma_50_1h'], -1)

m_eurusd_4h['sma_20_4h'] = m_eurusd_4h['close_bid_4h'].rolling(window=20).mean().shift(1, axis=0)
m_eurusd_4h['sma_50_4h'] = m_eurusd_4h['close_bid_4h'].rolling(window=50).mean().shift(1, axis=0)
m_eurusd_4h['sma_200_4h'] = m_eurusd_4h['close_bid_4h'].rolling(window=200).mean().shift(1, axis=0)
m_eurusd_4h['sma_20_50_co_4h'] = np.nan
m_eurusd_4h['sma_20_50_co_4h'] = m_eurusd_4h['sma_20_50_co_4h'].mask(m_eurusd_4h['sma_20_4h'] > m_eurusd_4h['sma_50_4h'], 1)
m_eurusd_4h['sma_20_50_co_4h'] = m_eurusd_4h['sma_20_50_co_4h'].mask(m_eurusd_4h['sma_20_4h'] < m_eurusd_4h['sma_50_4h'], -1)

m_eurusd_1d['sma_20_1d'] = m_eurusd_1d['close_bid_1d'].rolling(window=20).mean().shift(1, axis=0)
m_eurusd_1d['sma_50_1d'] = m_eurusd_1d['close_bid_1d'].rolling(window=50).mean().shift(1, axis=0)
m_eurusd_1d['sma_200_1d'] = m_eurusd_1d['close_bid_1d'].rolling(window=200).mean().shift(1, axis=0)
m_eurusd_1d['sma_20_50_co_1d'] = np.nan
m_eurusd_1d['sma_20_50_co_1d'] = m_eurusd_1d['sma_20_50_co_1d'].mask(m_eurusd_1d['sma_20_1d'] > m_eurusd_1d['sma_50_1d'], 1)
m_eurusd_1d['sma_20_50_co_1d'] = m_eurusd_1d['sma_20_50_co_1d'].mask(m_eurusd_1d['sma_20_1d'] < m_eurusd_1d['sma_50_1d'], -1)

#m_eurusd['sma_20' + '_15m'] = m_eurusd_15m['sma_20']
#indexing error
# t_eurusd['sma_20' + '_15m'] = 0
# i = 21
# t_eurusd_subset = t_eurusd[(t_eurusd['datetime'] < m_eurusd_15m['datetime'][i + 1]) & (t_eurusd['datetime'] >= m_eurusd_15m['datetime'][i])]
# t_eurusd_subset['sma_20' + '_15m'] = m_eurusd_15m['sma_20']

#better to pull tick data to bar charts than other way around- figure out how to pull 1h data to 15m charts 
#run this after you run indicators
#change this if adding 4h and 1d charts
newdf = pd.DataFrame(np.repeat(m_eurusd_1h.values, 4, axis=0))
newdf.columns = m_eurusd_1h.columns
newdf = newdf.shift(3)
newdf['datetime'] = m_eurusd_15m['datetime']



# is this how I do it?
newdf = pd.DataFrame(np.repeat(m_eurusd_1d.values, 96, axis=0))
newdf.columns = m_eurusd_1d.columns
newdf = newdf.shift(69)
newdf['datetime'] = m_eurusd_15m['datetime']



##probably don't need these
# newdf['open_bid_15m'] = m_eurusd_15m['open_bid']
# newdf['high_bid_15m'] = m_eurusd_15m['high_bid']
# newdf['low_bid_15m'] = m_eurusd_15m['low_bid']
# newdf['close_bid_15m'] = m_eurusd_15m['close_bid']
newdf['sma_20_15m'] = m_eurusd_15m['sma_20_15m']
newdf['sma_50_15m'] = m_eurusd_15m['sma_50_15m']
newdf['sma_200_15m'] = m_eurusd_15m['sma_200_15m']
newdf['sma_20_50_co_15m'] = m_eurusd_15m['sma_20_50_co_15m']




##improve on this to include other trades
#only when 15m 20/50 CO changes
orders = newdf[200:][newdf['sma_20_50_co_15m'].diff() != 0]

#orders = orders[orders['sma_20_50_co_15m'] == orders['sma_20_50_co_1h']].reset_index(drop=True)

#renaming column is to avoid confusion when more complex strategies are implemented
orders['trigger'] = -1*orders['sma_20_50_co_15m']
#when the SMA COs don't agree replace with 0 and get rid of the row
orders['trigger'] = orders['trigger'].mask(orders['sma_20_50_co_15m'] != orders['sma_20_50_co_1h'], 0)
#delete every consecutive 0 in trigger column- if pyramiding need to change this- not necessary with pass clause
#delete the first one because that is when the data opens up not necessarilly a trade trigger
orders = orders[orders['trigger'].diff() != 0][1:].reset_index(drop=True)

orders.columns = ['datetime', 'open_bid', 'high_bid', 'low_bid', 'close_bid']
