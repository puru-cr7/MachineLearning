'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''
import os
import fix_yahoo_finance as yf 
import pandas as pd 


def symbol_to_path(sym, base_dir):
    # Return CSV file path given ticker symbol
    return os.path.join(base_dir, "{}.csv".format(str(sym)))


def download_stock_data(syms, start_date, end_date, base_dir):
    # This method downloads historical prices for a list of stocks(given by syms) 
    # and stores as csv files is mentioned base dir
    for sym in syms:
        data = yf.download(sym, start_date, end_date)
        data.to_csv(symbol_to_path(sym, base_dir))


def get_adjcls_data(symbols, dates, base_dir):
    # Read stock data (adjusted close) for given symbols from CSV files.
    df = pd.DataFrame(index=dates)

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol, base_dir), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'] , na_values=['null'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        df = df.dropna(axis=0, how='any')
    return df


def normalize_data(df):
    # normalize data stock data in accordance with its initial value
    return df / df.iloc[0, :]

