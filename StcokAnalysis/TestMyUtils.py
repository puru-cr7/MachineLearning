'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''
import GenericUtils as gu
import PlotUtils as pu
import StockDataUtils as sdu
import StockStatsUtils as ssu

import numpy as np
import pandas as pd
import scipy.optimize as opt


def con(t):
    return sum(t) - 1


def to_test_minimize(port_allocs, start_val, port_price):
    v1, v2, v3, v4 = ssu.get_port_stats(port_allocs, start_val, port_price)
    return v1 * -1;


def test_my_util():
    # fetching data
    pu.configure_plotly('puru_cr7', '#######')
    dates = pd.date_range('2016-03-14', '2018-03-13')
    symbols = ['ITC.NS', 'PNB.NS', 'TATAMOTORS.NS', 'NSE']  # SPY will be added in get_data()
    df = sdu.get_adjcls_data(symbols, dates, "data/trading")
    # pu.plot_data_plotly(sdu.normalize_data(df))
    
    # getting and plotting bolinger bands
    upper_band, lower_band = ssu.get_bollinger_bands(ssu.get_rolling_mean(df['ITC.NS'], window=20), ssu.get_rolling_std(df['ITC.NS'], window=20));
    df1 = pd.DataFrame({'upper':upper_band, 'lower':lower_band, 'val':df['ITC.NS']})
    gu.drop_rows_with_na(df1)
    # pu.plot_data_plotly(df1)
    print(df1.head(5))
    print()
    
    # comparing daily returns of stocks
    daily_returns = ssu.compute_daily_returns(df.loc[:, ['ITC.NS', 'NSE']])
    # pu.plot_data_plotly(daily_returns)
    print("correlation for ITC") 
    print(daily_returns.corr(method='pearson'))
    print()
    
    # get portfolio stats
    start_val = 30000;
    port_allocs = [0.33, 0.34, 0.33]
    port_price = df.loc[:, 'ITC.NS':'TATAMOTORS.NS']
    ashp, cr, mdr, stdr = ssu.get_port_stats(port_allocs, start_val, port_price)
    print('Sharpe ratio= {}'.format(ashp.value))
    print('Cumulative return= {}'.format(cr))
    print('Mean daily return=', mdr.value)
    print('Std of daily ret=', stdr.value)
    print()
    
    # Generating random data by applying functions along each row
    arr = np.random.dirichlet(np.ones(3), size=50)
    val = np.apply_along_axis(ssu.get_port_stats, 1, arr, start_val, port_price)
    columns = ['val1', 'val2', 'val3']
    df2 = pd.DataFrame(arr, columns=columns)
    df3 = pd.DataFrame(val[:, 0].astype('float64'), columns=['output'])
    df2 = df2.join(df3)
    print(df2)
    print()
    
    # Optimize portfolio allocation using scipy optimize
    start_val = 30000;
    port_price = df.loc[:, 'ITC.NS':'TATAMOTORS.NS']
    cons = [{'type':'eq', 'fun': con}]
    port_allocs = [0.33, 0.34, 0.33]
    res = opt.minimize(to_test_minimize, port_allocs, args=(start_val, port_price), method='SLSQP', bounds=[(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)], constraints=cons, options={"disp":True})
    print(res)
    print("Allocation for maximum sharpe ratio is {}".format(res.x))
    print("maximum sharpe ratio that can be achieved is {}".format(res.fun * -1))


if __name__ == "__main__":
    test_my_util()
    
