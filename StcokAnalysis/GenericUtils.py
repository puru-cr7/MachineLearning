'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''
import os


def drop_rows_with_na(df):
    # drops all rows with any column value as null
    df.dropna(axis=0, how='any', inplace=True)

    
def symbol_to_path(sym, base_dir):
    # Return CSV file path given ticker symbol
    return os.path.join(base_dir, "{}.csv".format(str(sym)))
    
