'''
Created on Jun 19, 2018

@author: Purnendu Rath (puru_cr7)
'''

import fix_yahoo_finance as yf


# This method downloads a list of stock historical prices 
# and stores as csv files is mentioned directory
def downloadStockData(syms, start_date, end_date, direc):
    for sym in syms:
        data = yf.download(sym, start_date, end_date)
        data.to_csv(direc + sym + ".csv")

