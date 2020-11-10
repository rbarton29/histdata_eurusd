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
# t_eurusd['datetime'] = t_eurusd['datetime'].apply(lambda x: f(x))
# t2 = datetime.now()
# print('nested function algo took ' + str(t2-t1) + ' seconds')
# #0:00:42.844325 seconds with 2 months

#only if you run secs column
# cols = list(t_eurusd.columns)
# cols = [cols[0]] + [cols[-1]] + cols[1:-1]
# t_eurusd = t_eurusd[cols]

# #measure times- slower
# t1 = datetime.now()
# m_eurusd['datetime'] =  m_eurusd[['date', 'time']].agg(''.join, axis=1)
# t2 = datetime.now()
# print('datetime took ' + str(t2-t1) + ' seconds')
# #0:00:02.575431 seconds with 2 months

# t1 = datetime.now()
# def f1(datestr):
#     return datetime(
#         int(datestr[:4]),
#         int(datestr[5:7]),
#         int(datestr[8:10]),
#         int(datestr[10:12]),
#         int(datestr[13:15]),
#     )
# m_eurusd['datetime'] = m_eurusd['datetime'].apply(lambda x: f1(x))
# t2 = datetime.now()
# print('nested function algo took ' + str(t2-t1) + ' seconds')
# #0:00:00.472427 seconds with 3 months




#convert to orders columns as opposed to print statements
#at end test speed of algo
t1 = datetime.now()
total_pips = 0
total_pips_list = [0]
pips_profit = [0]
pips_lost = [0]
capital_profit = [0]
capital_lost = [0]
winning_trades = 0
winning_trades_list = [0]
losing_trades = 0
losing_trades_list = [0]
winning_streak = [0]
losing_streak = [0]
longest_winning_streak = [0]
longest_losing_streak = [0]
account_value = 100000
account_value_list = [100000]
#is there an optimal risk_percentage/ a way to graph it?
risk_percentage = 0.2
amount_at_risk_per_trade = account_value * risk_percentage
# this just measures how much money is in market while multiple trades are going on
total_capital_at_risk = amount_at_risk_per_trade
pips_at_risk = 0.005
stops = []
take_profits = []
entries = []
exits = []
#when quoted in non USD denominated currency pair you multiply by exchange rate?
lots = amount_at_risk_per_trade/pips_at_risk/100000
commissions = 2.0

#must add 15 minute timedelta because close prices don't occur until the end of the 15 minute window
ask_subset = ask[(ask['datetime'] < orders['datetime'][1] + timedelta(minutes=15)) & (ask['datetime'] >= orders['datetime'][0] + timedelta(minutes=15))]

#entry = orders['close_bid_15m'][0]- b/c entry is a short
entry = ask_subset['ask'].iloc[0]

entries = entries.append(entry)
account_value -= commissions
account_value_list = account_value_list.append(account_value)
total_capital_at_risk -= commissions
#print('entering short at', str(round(entry, 5)))
#print(orders.loc[0])

for i in range(1, len(orders)):
    if orders['trigger'][i] == 1:
        #simple 10 pip stop - not factoring in where is ideal stop based on volatility or when to move it
        #only need to rename stops and take_profits if entering new trade simultaneously
        #stops and take_profits must stay inside if-else statement though because they could vary based on whether long or short
        stops = stops.append(entry - pips_at_risk)
        #refresh on order types
        take_profits = take_profits.append(entry + 2 * pips_at_risk)
        #buy current order 2x to exit short and enter long trade
        if len(ask_subset[(ask_subset['ask'] > stops[i]) | (ask_subset['ask'] < take_profits[i])]) > 0:
            exit = ask_subset[(ask_subset['ask'] > stops[i]) | (ask_subset['ask'] < take_profits[i])]['ask'].iloc[0]
            exits = exits.append(exit)
            #print('stopped out at', + exit))
            account_value -= commissions
        else:
            exit = ask_subset['ask'].iloc[-1]
            exits = exits.append(exit)
        if (exit - entry) < 0:
            winning_trades += 1
            winning_trades_list = winning_trades_list.append(1)
            losing_trades = losing_trades.append(0)
            pips_profit += (entry - exit)
            pips_profit_list = pips_profit_list.append(pips_profit)
            total_pips += (entry - exit)
            total_pips_list = total_pips_list.append(total_pips)
            capital_profit = total_capital_at_risk * (entry - exit)/pips_at_risk
            capital_profit_list = capital_profit_list.append(total_capital_at_risk * (entry - exit)/pips_at_risk)
            # winning_streak = winning_streak.append(winning_streak + 1)
            # losing_streak = losing_streak.append(0)
        elif (exit - entry) > 0:
            losing_trades += 1
            losing_trades = losing_trades.append(1)
            winning_trades_list = winning_trades_list.append(0)
            pips_lost += (exit - entry)
            pips_lost_list = pips_lost_list.append(pips_lost)
            total_pips += (entry - exit)
            total_pips = pips.append(pips[i - 1] - (exit - entry))
            capital_lost = capital_lost.append(total_capital_at_risk * (exit - entry)/pips_at_risk)
            # losing_streak = losing_streak.append(losing_streak + 1)
            # winning_streak = winning_streak.append(0)
        #if closing out and entering new trade simultaneously, there is no need to update the total_capital_at_risk variable
        #but I don't think I am subtracting commission charges properly
        #print('exited short at', str(round(exit, 5)))
        #print(orders.loc[i])
        if i == len(orders) - 1:
            ask_subset = ask[ask['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
        else:
            ask_subset = ask[(ask['datetime'] < orders['datetime'][i+1] + timedelta(minutes=60)) & (ask['datetime'] >= orders['datetime'][i] + timedelta(minutes=15))]
        #print('entering long', round(10000 * (entry - exit), 1), 'pips gained')
        # is this the corresponding ask for entry = orders['close_bid'][i]?
        entry = ask_subset['ask'].iloc[0]
        entries = entries.append(entry)
    elif orders['trigger'][i] == -1:
        stops = stops.append(entry + pips_at_risk)
        take_profits = take_profits.append(entry - 2 * pips_at_risk)
        #sell current order 2x to exit long and enter short trade
        #might save computing time by redefining ask_subset
        if len(ask_subset[(ask_subset['bid'] > stops[i]) | (ask_subset['bid'] < take_profits[i])]) > 0:
            exit = ask_subset[(ask_subset['bid'] > stops[i]) | (ask_subset['bid'] < take_profits[i])]['bid'].iloc[0]
            #print('stopped out at ' + str(exit))
            exits = exits.append(exit)
            account_value -= commissions
        else:
            exit = orders['close_bid'][i]
            exits = exits.append(exit)
        if (exit - entry) > 0:
            winning_trades += 1
            winning_trades_list = winning_trades_list.append(1)
            losing_trades_list = losing_trades_list.append(0)
            pips_profit += (exit - entry)
            pips_profit_list = pips_profit_list.append(pips_profit)
            pips = pips.append(pips[i - 1] + exit - entry)
            capital_profit += total_capital_at_risk * (exit - entry)/pips_at_risk
            # winning_streak += 1
            # losing_streak = 0
        elif (exit - entry) < 0:
            losing_trades += 1
            losing_trades_list = losing_trades_list.append(1)
            winning_trades_list = winning_trades_list.append(0)
            pips_lost += (entry - exit)
            pips_lost_list = pips_lost_list.append(pips_lost)
            pips -= (entry - exit)
            capital_lost += total_capital_at_risk * (entry - exit)/pips_at_risk
            # losing_streak += 1
            # winning_streak = 0
        #print('exited long at', str(round(exit, 5)))
        #print(orders.loc[i])
        if i == len(orders) - 1:
            ask_subset = ask[ask['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
        else:
            ask_subset = ask[(ask['datetime'] < orders['datetime'][i+1] + timedelta(minutes=60)) & (ask['datetime'] >= orders['datetime'][i] + timedelta(minutes=15))]
        #print('entering short', round(10000 * (exit - entry), 1), 'pips gained')
        #when implementing more commplex algos, you will wait for better prices and pull from ask_subset
        entry = orders['close_bid'][i]
        entries = entries.append(entry)
    total_trades = (winning_trades + losing_trades)
    winning_percentage = str(round(100 * winning_trades/float(total_trades), 1)) + '%'
    winning_percentage_list = winning_percentage_list.append(winning_percentage)
    reward_risk = pips_profit/pips_lost
    reward_risk_list = reward_risk_list.append(reward_risk)
    #only seems to subtract account value once
    account_value = 100000 + capital_profit - capital_lost
    #subtract commissions cost from account value at the beginning of each trade; in this strategy we are assuming when you
    #close a trade you start a new trade so I tried avoiding double counting unless you get stopsped out
    account_value_list = account_value_list.append(account_value - commissions)
    #change to exited long or short at and put inside if/else conditionals
    #print('total pips', str(round(10000 * pips, 1)), 'winning_percentage', winning_percentage, 'R/R Ratio', str(round(reward_risk, 2)), 'account value', '$'+str(round(account_value, 2)), 'ROI = ', str(round((account_value - 100000)/1000, 2)) + '%')
    


account_value += commissions
#convert series to columns
orders['entries'] = entries
orders['exits'] = exits
orders['winning_trades'] = winning_trades
orders['total_pips'] = total_pips_list
orders['winning_percentage'] = winning_percentage_list
orders['reward_risk'] = reward_risk_list
orders['account_value'] = account_value_list


print(orders)

print('just kidding, that last one was the end- so unless you got stopsped out add the last commission charges back so account value is really: $' + str(round(account_value, 2)))
print('longest_winning_streak was ', longest_winning_streak)
print('longest_losing_streak was ', longest_losing_streak)

t2 = datetime.now()
print('algo took ' + str(t2-t1) + ' seconds')











##old algo printing results
#you'll need to store all current orders in dicts when you are looking at several pairs at once
entries = {}


t1 = datetime.now()

pips = 0
pips_profit = 0
pips_lost = 0
capital_profit = 0
capital_lost = 0
winning_trades = 0
losing_trades = 0
winning_streak = 0
losing_streak = 0
longest_winning_streak = 0
longest_losing_streak = 0
account_value = 100000
#is there an optimal risk_percentage/ a way to graph it?
risk_percentage = 0.2
amount_at_risk_per_trade = account_value * risk_percentage
# this just measures how much money is in market while multiple trades are going on
total_capital_at_risk = amount_at_risk_per_trade
pips_at_risk = 0.005
#when quoted in non USD denominated currency pair you multiply by exchange rate?
lots = amount_at_risk_per_trade/pips_at_risk/100000
commissions = 2.0
#must add 15 minute timedelta because close prices don't occur until the end of the 15 minute window
ask_subset = ask[(ask['datetime'] < orders['datetime'][1] + timedelta(minutes=15)) & (ask['datetime'] >= orders['datetime'][0] + timedelta(minutes=15))]

entry = orders['close_bid_15m'][0]
#entry = ask_subset['ask'].iloc[0]

account_value -= commissions
total_capital_at_risk -= commissions
print('entering short at', str(round(entry, 5)))
print(orders.loc[0])


#next you implement trailing stops and pulling orders from separate column
#look at better ways to display results than print statements- this is where ML comes in handy


for i in range(2, len(orders)):
    if orders['trigger'][i] == 1:
        #simple 10 pip stop - not factoring in where is ideal stop based on volatility or when to move it
        #only need to rename stops and take_profits if entering new trade simultaneously
        #stops and take_profits must stay inside if-else statement though because they could vary based on whether long or short
        stop = entry + pips_at_risk
        #refresh on order types
        take_profit = entry - 2 * pips_at_risk
        #buy current order 2x to exit short and enter long trade
        if len(ask_subset[(ask_subset['ask'] > stop) | (ask_subset['ask'] < take_profit)]) > 0:
            exit = ask_subset[(ask_subset['ask'] > stop) | (ask_subset['ask'] < take_profit)]['ask'].iloc[0]
            print('stopped out at ' + str(round(exit, 2)))
            account_value -= commissions
        else:
            exit = ask_subset['ask'].iloc[-1]
        if (exit - entry) < 0:
            winning_trades += 1
            pips_profit += (entry - exit)
            pips += (entry - exit)
            capital_profit += total_capital_at_risk * (entry - exit)/pips_at_risk
            winning_streak += 1
            if losing_streak > longest_losing_streak:
                longest_losing_streak = losing_streak
            losing_streak = 0
        elif (exit - entry) > 0:
            losing_trades += 1
            pips_lost += (exit - entry)
            pips -= (exit - entry)
            capital_lost += total_capital_at_risk * (exit - entry)/pips_at_risk
            losing_streak += 1
            if winning_streak > longest_winning_streak:
                longest_winning_streak = winning_streak
            winning_streak = 0
        #if closing out and entering new trade simultaneously, there is no need to update the total_capital_at_risk variable
        #but I don't think I am subtracting commission charges properly
        print('exited short at', str(round(exit, 5)))
        print(orders.loc[i])
        if i == len(orders) - 1:
            ask_subset = ask[ask['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
        else:
            ask_subset = ask[(ask['datetime'] < orders['datetime'][i+1] + timedelta(minutes=60)) & (ask['datetime'] >= orders['datetime'][i] + timedelta(minutes=15))]
        print('entering long', round(10000 * (entry - exit), 1), 'pips gained')
        # is this the corresponding ask for entry = orders['close_bid'][i]?
        entry = ask_subset['ask'].iloc[0]
    elif orders['trigger'][i] == -1:
        stop = entry - pips_at_risk
        take_profit = entry + 2 * pips_at_risk
        #sell current order 2x to exit long and enter short trade
        #might save computing time by redefining ask_subset
        if len(ask_subset[(ask_subset['bid'] > stop) | (ask_subset['bid'] < take_profit)]) > 0:
            exit = ask_subset[(ask_subset['bid'] > stop) | (ask_subset['bid'] < take_profit)]['bid'].iloc[0]
            print('stopped out at ' + str(round(exit, 2)))
            account_value -= commissions
        else:
            exit = orders['close_bid_15m'][i]
        if (exit - entry) > 0:
            winning_trades += 1
            pips_profit += (exit - entry)
            pips += (exit - entry)
            capital_profit += total_capital_at_risk * (exit - entry)/pips_at_risk
            winning_streak += 1
            if losing_streak > longest_losing_streak:
                longest_losing_streak = losing_streak
            losing_streak = 0
        elif (exit - entry) < 0:
            losing_trades += 1
            pips_lost += (entry - exit)
            pips -= (entry - exit)
            capital_lost += total_capital_at_risk * (entry - exit)/pips_at_risk
            losing_streak += 1
            if winning_streak > longest_winning_streak:
                longest_winning_streak = winning_streak
            winning_streak = 0
        print('exited long at', str(round(exit, 5)))
        print(orders.loc[i])
        if i == len(orders) - 1:
            ask_subset = ask[ask['datetime'] >= (orders['datetime'][i] + timedelta(minutes=15))]
        else:
            ask_subset = ask[(ask['datetime'] < orders['datetime'][i+1] + timedelta(minutes=60)) & (ask['datetime'] >= orders['datetime'][i] + timedelta(minutes=15))]
        print('entering short', round(10000 * (exit - entry), 1), 'pips gained') 
        #when implementing more commplex algos, you will wait for better prices and pull from ask_subset
        entry = orders['close_bid_15m'][i]
    total_trades = (winning_trades + losing_trades)
    winning_percentage = str(round(100 * winning_trades/float(total_trades), 1)) + '%'
    reward_risk = pips_profit/pips_lost
    #only seems to subtract account value once
    account_value = 100000 + capital_profit - capital_lost
    #subtract commissions cost from account value at the beginning of each trade; in this strategy we are assuming when you
    #close a trade you start a new trade so I tried avoiding double counting unless you get stopped out
    account_value -= commissions
    #change to exited long or short at and put inside if/else conditionals
    print('total pips', str(round(10000 * pips, 1)), 'winning_percentage', winning_percentage, 'R/R Ratio', str(round(reward_risk, 2)), 'account value', '$'+str(round(account_value, 2)), 'ROI = ', str(round((account_value - 100000)/1000, 2)) + '%')
    ##only run this if entering new trade simultaneously
    #entry = exit; entry != exit when factoring in spread    
    print('entered at', str(round(entry, 5)))
account_value += commissions
print('just kidding, that last one was the end- so unless you got stopped out add the last commission charges back so account value is really: $' + str(round(account_value, 2)))
print('longest_winning_streak was ', longest_winning_streak)
print('longest_losing_streak was ', longest_losing_streak)

t2 = datetime.now()
print('algo took ' + str(t2-t1) + ' seconds')