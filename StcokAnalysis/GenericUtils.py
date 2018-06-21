'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''


def drop_rows_with_na(df):
    # drops all rows with any column value as null
    df.dropna(axis=0, how='any', inplace=True)
    
