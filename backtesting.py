##function to execute buy-sell orders? adjust risk%? optimal risk% amongst all correlated and uncorrelated active orders
    ##of course factors in cost of commissions as well as the spread
    ##enter buy or sell order when 'sentiment' rises above a certain level and exit when sentiment lowers a little below that level
    ## also know where to implement and move stop and (partial or full) take_profit orders
    ##assuming all GTC orders and no rollover fees (carry trade) with commission and spread costs
    ##need to factor in net effect of taxes


#2 new algos adding results to orders2 dataframe
##first doesn't move stop at all- second implements B/E stop (begins at ~line 240)

year = 2019
#first
t1 = datetime.now()
entries = []
exits = []
stops = []
take_profits = []
results = []
total_pips = 0
total_pips_list = []
pips_profit = 0
pips_profit_list = []
pips_lost = 0
pips_lost_list = []
capital_profit = 0
capital_profit_list = []
capital_lost = 0
capital_lost_list = []
winning_trades = 0
winning_trades_list = []
losing_trades = 0
account_value = 100000
account_value_list = []
#is there an optimal risk_percentage/ a way to graph it?
risk_percentage = 0.01
amount_at_risk_per_trade = account_value * risk_percentage
#this seems to be rougly the optimal constant for this past data
pips_at_risk = 0.007
#it seems that 1 is about the optimal constant w/o moving stops
took_profit_constant = 1
trail_stop_constant = 0.5
winning_percentage_list = []
reward_risk_list = []
max_drawdown = 0
#when quoted in non USD denominated currency pair you multiply by exchange rate?
lots = amount_at_risk_per_trade/pips_at_risk/100000
commissions = 2.0
for i in range(0, len(orders)):
    # this just measures how much money is in market while multiple trades are going on
    total_capital_at_risk = amount_at_risk_per_trade - commissions
    #must add 15 minute timedelta because close prices don't occur until the end of the 15 minute window
    if i == len(orders) - 1:
        t_subset = t_eurusd[t_eurusd['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
    else:
        t_subset = t_eurusd[(t_eurusd['datetime'] < (orders['datetime'][i+1] + timedelta(minutes=15))) & (t_eurusd['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15)))]
    if orders['trigger'][i] == 0:
        #this is because we alreay exited out in the other elif clauses- will need to change this somehow though 
        #if I start pyramiding
        pass
        #append each list again in here so we have duplicates? but alternate entries and exits?
    else:    
        if orders['trigger'][i] == 1:
            #simple 10 pip stop - not factoring in where is ideal stop based on volatility or when to move it
            #only need to rename stops and take_profits if entering new trade simultaneously
            #stops and take_profits must stay inside if-else statement though because they could vary based on whether long or short
            entry = t_subset['ask'].iloc[0]
            entries.append(entry)
            account_value -= commissions
            stop = entry - pips_at_risk
            take_profit = entry + took_profit_constant * pips_at_risk
            #trail_stop = entry + trail_stop_constant * pips_at_risk
            stops.append(stop)
            #refresh on order types
            take_profits.append(take_profit)
            if len(t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > take_profit)]) > 0:
                exit = t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > take_profit)]['bid'].iloc[0]
                exits.append(exit)
                if exit < stop:
                    results.append('stopped out')
                elif exit > take_profit:
                    results.append('took profit')
            else:
                #assuming no pyramiding so always 0s following a trade- else this part gets more complicated
                exit = t_subset['bid'].iloc[-1]
                exits.append(exit)
                results.append('exited')
            account_value -= commissions
            if (exit - entry) > 0:
                winning_trades += 1
                winning_trades_list.append(1)
                #this represents cumulative profit
                pips_profit += (exit - entry)
                #this represents individual profits
                pips_profit_list.append(exit - entry)
                pips_lost_list.append(0)
                #cumulative
                total_pips += (exit - entry)
                #cumulative
                total_pips_list.append(total_pips)
                #individual
                capital_profit = total_capital_at_risk * (exit - entry)/pips_at_risk
                capital_lost = (0)
                #individual
                capital_profit_list.append(capital_profit)
                capital_lost_list.append(0)
            elif (exit - entry) < 0:
                losing_trades += 1
                winning_trades_list.append(0)
                #pips_lost should be positive as well- cumulative
                pips_lost += (entry - exit)
                #individual
                pips_lost_list.append(entry - exit)
                pips_profit_list.append(0)
                #cumulative- is adding a negative here
                total_pips += (exit - entry)
                #cumulative
                total_pips_list.append(total_pips)
                #individual- positive
                capital_profit = 0
                capital_lost = (total_capital_at_risk * (entry - exit)/pips_at_risk)
                #individual- positive
                capital_profit_list.append(0)
                capital_lost_list.append(capital_lost)
            #if closing out and entering new trade simultaneously, there is no need to update the total_capital_at_risk variable
            total_capital_at_risk = 0
        elif orders['trigger'][i] == -1:
            entry = t_subset['bid'].iloc[0]
            entries.append(entry)
            account_value -= commissions
            stop = entry + pips_at_risk
            take_profit = entry - took_profit_constant * pips_at_risk
            #trail_stop = entry - trail_stop_constant * pips_at_risk
            stops.append(stop)
            take_profits.append(take_profit)
            #might save computing time by redefining t_subset
            if len(t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < take_profit)]) > 0:
                exit = t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < take_profit)]['ask'].iloc[0]
                exits.append(exit)
                if exit > stop:
                    results.append('stopped out')
                elif exit < take_profit:
                    results.append('took profit') 
            else:
                #assuming no pyramiding so always 0s following a trade- else this part gets more complicated
                exit = t_subset['ask'].iloc[-1]
                exits.append(exit)
                results.append('exited')
            account_value -= commissions
            if (exit - entry) < 0:
                winning_trades += 1
                winning_trades_list.append(1)
                #this represents cumulative profit
                pips_profit += (entry - exit)
                #this represents individual profits
                pips_profit_list.append(entry - exit)
                pips_lost_list.append(0)
                #cumulative
                total_pips += (entry - exit)
                #cumulative
                total_pips_list.append(total_pips)
                #individual
                capital_profit = total_capital_at_risk * (entry - exit)/pips_at_risk
                capital_lost = 0
                #individual
                capital_profit_list.append(capital_profit)
                capital_lost_list.append(0)
            elif (exit - entry) > 0:
                losing_trades += 1
                winning_trades_list.append(0)
                #pips_lost should be positive as well- cumulative
                pips_lost += (exit - entry)
                #individual
                pips_lost_list.append(exit - entry)
                pips_profit_list.append(0)
                #cumulative- is adding a negative here
                total_pips += (entry - exit)
                #cumulative
                total_pips_list.append(total_pips)
                #individual- positive
                capital_profit = 0
                capital_lost = (total_capital_at_risk * (exit - entry)/pips_at_risk)               
                #individual- positive
                capital_profit_list.append(0)
                capital_lost_list.append(capital_lost)
            #when implementing more complex algos, you will wait for better prices and pull from t_subset
            total_capital_at_risk = 0
        total_trades = (winning_trades + losing_trades)
        winning_percentage = str(round(100 * winning_trades/float(total_trades), 1)) + '%'
        winning_percentage_list.append(winning_percentage)
        if pips_lost == 0:
            reward_risk = 'div/0'
        else:
            reward_risk = (pips_profit/pips_lost)
            # reward_risk = (pips_profit/winning_trades)/(pips_lost/losing_trades)
        reward_risk_list.append(reward_risk)
        account_value += capital_profit
        account_value -= capital_lost
        account_value_list.append(account_value)
max_account_value = max(account_value_list)
min_account_value = min(account_value_list)
w_list=[]
l_list = []
w = 0
l = 0
for i in winning_trades_list:
    if i == 1:
        l_list.append(l)
        w += 1
        l = 0
    else:
        w_list.append(w)
        w = 0
        l += 1
longest_winning_streak = max(w_list)
longest_losing_streak = max(l_list)
#probably an oversimplification- look deper at this later
max_drawdown_1 = 1 - min(account_value_list[account_value_list.index(max_account_value):]) / max_account_value 
#min_account_value not defined
max_drawdown_2 = 1 - min_account_value / max(account_value_list[:account_value_list.index(min_account_value)])
max_drawdown = max(max_drawdown_1, max_drawdown_2)
#doesn't inlude exits so columns are same length
orders2 = orders[orders['trigger'] != 0]
#convert series to columns
orders2['capital_profit_list'] = capital_profit_list
orders2['capital_lost_list'] = capital_lost_list
orders2['entries'] = entries
orders2['exits'] = exits
orders2['winning_trades_list'] = winning_trades_list
orders2['total_pips'] = total_pips_list
orders2['winning_percentage'] = winning_percentage_list
orders2['reward_risk'] = reward_risk_list
orders2['results'] = results
orders2['account_value'] = account_value_list
final_account_value = {}
#computes by taking account value from last trade of month
final_account_value[1] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 2, 1)]['account_value'].iloc[-1]
final_account_value[2] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 3, 1)]['account_value'].iloc[-1]
final_account_value[3] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 4, 1)]['account_value'].iloc[-1]
final_account_value[4] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 5, 1)]['account_value'].iloc[-1]
final_account_value[5] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 6, 1)]['account_value'].iloc[-1]
final_account_value[6] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 7, 1)]['account_value'].iloc[-1]
final_account_value[7] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 8, 1)]['account_value'].iloc[-1]
final_account_value[8] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 9, 1)]['account_value'].iloc[-1]
final_account_value[9] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 10, 1)]['account_value'].iloc[-1]
final_account_value[10] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 11, 1)]['account_value'].iloc[-1]
final_account_value[11] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 12, 1)]['account_value'].iloc[-1]
final_account_value[12] = orders2[['datetime', 'account_value']]['account_value'].iloc[-1]
monthly_returns = {}
monthly_returns[1] = (final_account_value[1] - 100000)/100000
monthly_returns[2] = (final_account_value[2] - final_account_value[1])/100000
monthly_returns[3] = (final_account_value[3] - final_account_value[2])/100000
monthly_returns[4] = (final_account_value[4] - final_account_value[3])/100000
monthly_returns[5] = (final_account_value[5] - final_account_value[4])/100000
monthly_returns[6] = (final_account_value[6] - final_account_value[5])/100000
monthly_returns[7] = (final_account_value[7] - final_account_value[6])/100000
monthly_returns[8] = (final_account_value[8] - final_account_value[7])/100000
monthly_returns[9] = (final_account_value[9] - final_account_value[8])/100000
monthly_returns[10] = (final_account_value[10] - final_account_value[9])/100000
monthly_returns[11] = (final_account_value[11] - final_account_value[10])/100000
monthly_returns[12] = (final_account_value[12] - final_account_value[11])/100000
winning_months = dict((k, v) for k, v in monthly_returns.items() if v >= 0)
winning_months_percentage = float(len(winning_months))/len(monthly_returns)
print(orders2)
x = np.array(results)
unique, counts = np.unique(x, return_counts=True) 
print np.asarray((unique, counts)).T
t2 = datetime.now()
print('algo took ' + str(t2-t1) + ' seconds')







#second

#implements B/E stop with trailing_stop trigger
###need to add pyramiding/trailing stop
#all entry orders are OTO for stops and take_profits- all of these are market orders

t1 = datetime.now()
entries = []
exits = []
stops = []
take_profits = []
results = []
total_pips = 0
total_pips_list = []
pips_profit = 0
pips_profit_list = []
pips_lost = 0
pips_lost_list = []
capital_profit = 0
capital_profit_list = []
capital_lost = 0
capital_lost_list = []
winning_trades = 0
winning_trades_list = []
losing_trades = 0
account_value = 100000
account_value_list = []
#is there an optimal risk_percentage/ a way to graph it?
risk_percentage = 0.01
amount_at_risk_per_trade = account_value * risk_percentage
#this seems to be rougly the optimal constant for this past data

pips_at_risk = 0.007
tick_volume_15m_list = []
t_spread_std_list = []
t_mid_std_list = []
min_tick_ask_list = []
min_tick_bid_list = []
max_tick_ask_list = []
max_tick_bid_list = []
time_elapsed_list = [0]
#it seems that 1 is about the optimal constant w/o moving stops- TBD what is with b/e stop
took_profit_constant = 2
trail_stop_constant = 1
winning_percentage_list = []
reward_risk_list = []
max_drawdown = 0
#when quoted in non USD denominated currency pair you multiply by exchange rate?
lots = amount_at_risk_per_trade/pips_at_risk/100000
commissions = 2.0
for i in range(0, len(orders)):
    # this just measures how much money is in market while multiple trades are going on
    total_capital_at_risk = amount_at_risk_per_trade - commissions
    #must add 15 minute timedelta because close prices don't occur until the end of the 15 minute window
    if i == len(orders) - 1:
        t_subset = t_eurusd[t_eurusd['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
    else:
        t_subset = t_eurusd[(t_eurusd['datetime'] < (orders['datetime'][i+1] + timedelta(minutes=15))) & (t_eurusd['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15)))]

    if orders['trigger'][i] == 0:
        #this is because we alreay exited out in the other elif clauses- will need to change this somehow though 
        #if I start pyramiding
        pass
        #append each list again in here so we have duplicates? but alternate entries and exits?
    else:
        #compute 15 minute rolling tick volume to find more optimal stops/take-profits
        rolling_15m_t_subset = t_eurusd[(t_eurusd['datetime'] >= orders['datetime'][i] - timedelta(minutes=15)) & (t_eurusd['datetime'] < orders['datetime'][i])]
        time_elapsed = orders['datetime'][i+1] - orders['datetime'][i]
        time_elapsed_list.append(time_elapsed)
        tick_volume_15m = len(rolling_15m_t_subset)
        tick_volume_15m_list.append(tick_volume_15m)
        min_tick_ask = min(t_subset['ask'])
        min_tick_ask_list.append(min_tick_ask)
        min_tick_bid = min(t_subset['bid'])
        min_tick_bid_list.append(min_tick_bid)
        max_tick_ask = max(t_subset['ask'])
        max_tick_ask_list.append(max_tick_ask)
        max_tick_bid = max(t_subset['bid'])
        max_tick_bid_list.append(max_tick_bid)            
        #distance from one t_eurusd tick to the next, to help measure volatility- maybe incorporate average between bid and ask
        # tick_delta = abs(rolling_15m_t_subset['ask'].diff())
        # tick_delta_list.append(tick_delta)
        #need to make sure you compute spreads on tick dataframes before you run this line
        t_spread_std = rolling_15m_t_subset['spread'].std()
        t_spread_std_list.append(t_spread_std)
        t_mid_std = rolling_15m_t_subset['mid'].std()
        t_mid_std_list.append(t_mid_std)
        if orders['trigger'][i] == 1:
            #simple x pip stop - not factoring in where is ideal stop based on volatility or when to move it
            #stops and take_profits must stay inside if-else statement though because they could vary based on whether long or short
            entry = t_subset['ask'].iloc[0]
            entries.append(entry)
            account_value -= commissions
            # pips_at_risk = (tick_volume_15m - .004)/
            stop = entry - pips_at_risk
            take_profit = entry + took_profit_constant * pips_at_risk
            trail_stop = entry + trail_stop_constant * pips_at_risk
            stops.append(stop)
            #refresh on order types
            take_profits.append(take_profit)
            if len(t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > trail_stop)]) > 0:
                if t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > trail_stop)]['bid'].iloc[0] > trail_stop:
                    stop = entry    #or += trail_stop_constant * pips_at_risk
                    #trail_stop += trail_stop_constant * pips_at_risk- only need to redefine if we might move it again
                    #redefines t_subset to include only the remaining ticks after the first trail_stop
                    #make sure below code works
                    t_subset = t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > take_profit)][1:]                    
                #if (len(t_subset[t_subset['bid'] < stop]) > 0) & (t_subset[t_subset['bid'] < stop]['bid'].iloc[0] < stop): or
                if len(t_subset) > 0:
                    exit = t_subset[(t_subset['bid'] < stop) | (t_subset['bid'] > take_profit)]['bid'].iloc[0]
                    exits.append(exit)
                    if exit < stop:
                        results.append('stopped out')
                    elif exit > take_profit:
                        results.append('took profit')
            else:
                #assuming no pyramiding so always 0s following a trade- else this part gets more complicated
                exit = t_subset['bid'].iloc[-1]
                exits.append(exit)
                results.append('exited')
            account_value -= commissions
            if (exit - entry) > 0:
                winning_trades += 1
                winning_trades_list.append(1)
                #this represents cumulative profit
                pips_profit += (exit - entry)
                #this represents individual profits
                pips_profit_list.append(exit - entry)
                pips_lost_list.append(0)
                #cumulative
                total_pips += (exit - entry)
                #cumulative
                total_pips_list.append(total_pips)
                #individual
                capital_profit = total_capital_at_risk * (exit - entry)/pips_at_risk
                capital_lost = (0)
                #individual
                capital_profit_list.append(capital_profit)
                capital_lost_list.append(0)
            elif (exit - entry) < 0:
                losing_trades += 1
                winning_trades_list.append(0)
                #pips_lost should be positive as well- cumulative
                pips_lost += (entry - exit)
                #individual
                pips_lost_list.append(entry - exit)
                pips_profit_list.append(0)
                #cumulative- is adding a negative here
                total_pips += (exit - entry)
                #cumulative
                total_pips_list.append(total_pips)
                #individual- positive
                capital_profit = 0
                capital_lost = (total_capital_at_risk * (entry - exit)/pips_at_risk)
                #individual- positive
                capital_profit_list.append(0)
                capital_lost_list.append(capital_lost)
            #if closing out and entering new trade simultaneously, there is no need to update the total_capital_at_risk variable
            total_capital_at_risk = 0
        elif orders['trigger'][i] == -1:
            entry = t_subset['bid'].iloc[0]
            entries.append(entry)
            account_value -= commissions
            stop = entry + pips_at_risk
            take_profit = entry - took_profit_constant * pips_at_risk
            trail_stop = entry - trail_stop_constant * pips_at_risk
            stops.append(stop)
            take_profits.append(take_profit)
            #might save computing time by redefining t_subset
            if len(t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < trail_stop)]) > 0:
                if t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < trail_stop)]['ask'].iloc[0] < trail_stop:
                    stop = entry    #or -= trail_stop_constant * pips_at_risk
                    #redefines t_subset to include only the remaining ticks after the first trail_stop
                    t_subset = t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < take_profit)][1:]
                if len(t_subset) > 0:
                    exit = t_subset[(t_subset['ask'] > stop) | (t_subset['ask'] < take_profit)]['ask'].iloc[0]
                    exits.append(exit)
                    if exit > stop:
                        results.append('stopped out')
                    elif exit < take_profit:
                        results.append('took profit')                 
            else:
                #assuming no pyramiding so always 0s following a trade- else this part gets more complicated
                exit = t_subset['ask'].iloc[-1]
                exits.append(exit)
                results.append('exited')
            account_value -= commissions
            if (exit - entry) < 0:
                winning_trades += 1
                winning_trades_list.append(1)
                #this represents cumulative profit
                pips_profit += (entry - exit)
                #this represents individual profits
                pips_profit_list.append(entry - exit)
                pips_lost_list.append(0)
                #cumulative
                total_pips += (entry - exit)
                #cumulative
                total_pips_list.append(total_pips)
                #individual
                capital_profit = total_capital_at_risk * (entry - exit)/pips_at_risk
                capital_lost = 0
                #individual
                capital_profit_list.append(capital_profit)
                capital_lost_list.append(0)
            elif (exit - entry) > 0:
                losing_trades += 1
                winning_trades_list.append(0)
                #pips_lost should be positive as well- cumulative
                pips_lost += (exit - entry)
                #individual
                pips_lost_list.append(exit - entry)
                pips_profit_list.append(0)
                #cumulative- is adding a negative here
                total_pips += (entry - exit)
                #cumulative
                total_pips_list.append(total_pips)
                #individual- positive
                capital_profit = 0
                capital_lost = (total_capital_at_risk * (exit - entry)/pips_at_risk)               
                #individual- positive
                capital_profit_list.append(0)
                capital_lost_list.append(capital_lost)
            #when implementing more complex algos, you will wait for better prices and pull from t_subset
            total_capital_at_risk = 0
        total_trades = (winning_trades + losing_trades)
        winning_percentage = str(round(100 * winning_trades/float(total_trades), 1)) + '%'
        winning_percentage_list.append(winning_percentage)
        if pips_lost == 0:
            reward_risk = 'div/0'
        else:
            reward_risk = pips_profit/pips_lost
        reward_risk_list.append(reward_risk)
        account_value = account_value + capital_profit - capital_lost
        account_value_list.append(account_value)
max_account_value = max(account_value_list)
min_account_value = min(account_value_list)
w_list=[]
l_list = []
w = 0
l = 0
for i in winning_trades_list:
    if i == 1:
        l_list.append(l)
        w += 1
        l = 0
    else:
        w_list.append(w)
        w = 0
        l += 1
longest_winning_streak = max(w_list)
longest_losing_streak = max(l_list)
#probably an oversimplification- look deper at this later
max_drawdown_1 = 1 - min(account_value_list[account_value_list.index(max_account_value):]) / max_account_value 
max_drawdown_2 = 1 - min_account_value / max(account_value_list[:account_value_list.index(min_account_value)])
max_drawdown = max(max_drawdown_1, max_drawdown_2)
#doesn't inlude exits so columns are same length
orders2 = orders[orders['trigger'] != 0]
#convert series to columns
orders2['capital_profit_list'] = capital_profit_list
orders2['capital_lost_list'] = capital_lost_list
orders2['entries'] = entries
orders2['exits'] = exits
orders2['winning_trades_list'] = winning_trades_list
orders2['total_pips'] = total_pips_list
orders2['winning_percentage'] = winning_percentage_list
orders2['reward_risk'] = reward_risk_list
orders2['results'] = results
orders2['account_value'] = account_value_list
orders2['tick_volume_15m_list'] = tick_volume_15m_list
orders2['t_spread_std_list'] = t_spread_std_list
orders2['t_mid_std_list'] = t_mid_std_list
#just added this haven't added to first script
orders2['min_tick_ask_list'] = min_tick_ask_list
orders2['min_tick_bid_list'] = min_tick_bid_list
orders2['max_tick_ask_list'] = max_tick_ask_list
orders2['max_tick_bid_list'] = max_tick_bid_list

orders2['furthest_reverse'] = orders2['entries'] - orders2['min_tick_bid_list']
orders2['furthest_reverse'] = orders2['furthest_reverse'].mask(orders2['trigger'] == -1, orders2['max_tick_ask_list'] - orders2['entries'])

time_elapsed_list.pop()
orders2['time_elapsed_list'] = time_elapsed_list

final_account_value = {}
#computes by taking account value from last trade of month
final_account_value[1] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 2, 1)]['account_value'].iloc[-1]
final_account_value[2] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 3, 1)]['account_value'].iloc[-1]
final_account_value[3] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 4, 1)]['account_value'].iloc[-1]
final_account_value[4] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 5, 1)]['account_value'].iloc[-1]
final_account_value[5] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 6, 1)]['account_value'].iloc[-1]
final_account_value[6] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 7, 1)]['account_value'].iloc[-1]
final_account_value[7] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 8, 1)]['account_value'].iloc[-1]
final_account_value[8] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 9, 1)]['account_value'].iloc[-1]
final_account_value[9] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 10, 1)]['account_value'].iloc[-1]
final_account_value[10] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 11, 1)]['account_value'].iloc[-1]
final_account_value[11] = orders2[['datetime', 'account_value']][orders2['datetime'] < datetime(year, 12, 1)]['account_value'].iloc[-1]
final_account_value[12] = orders2[['datetime', 'account_value']]['account_value'].iloc[-1]
monthly_returns = {}
monthly_returns[1] = (final_account_value[1] - 100000)/100000
monthly_returns[2] = (final_account_value[2] - final_account_value[1])/100000
monthly_returns[3] = (final_account_value[3] - final_account_value[2])/100000
monthly_returns[4] = (final_account_value[4] - final_account_value[3])/100000
monthly_returns[5] = (final_account_value[5] - final_account_value[4])/100000
monthly_returns[6] = (final_account_value[6] - final_account_value[5])/100000
monthly_returns[7] = (final_account_value[7] - final_account_value[6])/100000
monthly_returns[8] = (final_account_value[8] - final_account_value[7])/100000
monthly_returns[9] = (final_account_value[9] - final_account_value[8])/100000
monthly_returns[10] = (final_account_value[10] - final_account_value[9])/100000
monthly_returns[11] = (final_account_value[11] - final_account_value[10])/100000
monthly_returns[12] = (final_account_value[12] - final_account_value[11])/100000
winning_months = dict((k, v) for k, v in monthly_returns.items() if v >= 0)
winning_months_percentage = len(winning_months)/len(monthly_returns)
print(orders2)
x = np.array(results)
unique, counts = np.unique(x, return_counts=True) 
print np.asarray((unique, counts)).T
t2 = datetime.now()
print('algo took ' + str(t2-t1) + ' seconds')


#use this information and run corrleations to find optimal stop using tick volume data
# orders2['tick_volume_15m_list'][orders2['results'] == 'exited'].mean()
# 1550.3867924528302
# orders2['tick_volume_15m_list'][orders2['results'] == 'stopped out'].mean()
# 2292.590909090909
# both STDs 1169.7798536945375 and 1132.5029027226926, and 2292.590909090909/1550.3867924528302 ~ 1.5 so use this as constant
# orders2['t_spread_std_list'][orders2['results'] == 'exited'].mean()
# 1.3150264036555562e-05
# orders2['t_spread_std_list'][orders2['results'] == 'stopped out'].mean()
# 1.4254562265162838e-05
# orders2['t_mid_std_list'][orders2['results'] == 'exited'].mean()
# 0.00024199602786062303
# orders2['t_mid_std_list'][orders2['results'] == 'stopped out'].mean()
# 0.00041057810814404703



#(1+monthly_returns[2])*(1+monthly_returns[3])*(1+monthly_returns[4])*(1+monthly_returns[5])*(1+monthly_returns[6])*(1+monthly_returns[7])*