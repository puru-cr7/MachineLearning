'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''

from StockDataUtils import normalize_data
import pandas as pd


def get_rolling_mean(values, window):
    # Returns rolling mean of given values (is a series e.g-df['test]), using specified window size.
    return values.rolling(window=window, center=False).mean()


def get_rolling_weighted_mean(values, window):
    # Returns rolling weighted mean of given values (is a series e.g-df['test]), using specified window size.
    return values.ewm(span=window).mean()


def get_rolling_std(values, window):
    # Returns rolling standard deviation of given values, using specified window size.
    return values.rolling(window=window, center=False).std()


def get_macd(data):
    # returns macd for given data which is a series, can pass smthng like df['test']
    return get_rolling_weighted_mean(data, 12) - get_rolling_weighted_mean(data, 26)


def get_bollinger_bands(rm, rstd):
    # Return upper and lower Bollinger Bands, given rolling mean and rolling std dev
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band


def compute_daily_returns(df):
    # Compute and return the daily return values.
    daily_returns = df.copy() 
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.iloc[0, :] = 0
    return daily_returns


def get_port_stats(port_allocs, start_val, port_price):
    # Given initial allocations, initial investment and port_price(closing prices of all members in columns)
    # Returns annualised sharpe ratio, cumulative return, avg daily ret and std of daily ret
    # 1-2 is a good sharpe ratio, 2+ is a very good sharpe ratio
    port_val, port_val_df = _compute_port_val(port_price, start_val, port_allocs)
    port_daily_ret = compute_daily_returns(port_val_df)
    port_daily_ret = port_daily_ret[1:]
    port_cumulative_ret = (port_val[-1] / port_val[0]) - 1
    port_avg_daily_ret = port_daily_ret.mean();
    port_std_daily_ret = port_daily_ret.std();
    # 1.07=1 + 0.07 (current fd rate)
    daily_risk_free_rate = (1.07 ** (1 / 252)) - 1
    expected_val = (port_daily_ret - daily_risk_free_rate).mean()
    port_sharpe_ratio = expected_val / port_std_daily_ret
    port_sharpe_ratio_annualised = (252 ** (1 / 2)) * port_sharpe_ratio
    return port_sharpe_ratio_annualised , port_cumulative_ret, port_avg_daily_ret, port_std_daily_ret


def _compute_port_val(port_price, start_val, port_allocs):
    # Given portfolio price, inititla investement and allocations(sum of which is one)
    # returns port_val which is Series and port_val_df the dataframe version of the series 
    # these series and data frame represent the portfolio values
    normed_port_price = normalize_data(port_price)
    alloced_port_price = normed_port_price * port_allocs;
    pos_vals = start_val * alloced_port_price
    port_val = pos_vals.sum(axis=1)
    port_val_df = pd.DataFrame({'value':port_val})
    return port_val, port_val_df

