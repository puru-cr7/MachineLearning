'''
Created on Jun 21, 2018

@author: Purnendu Rath (puru_cr7)
'''
# cufflinks import mandatory for plotly
import cufflinks as cf
import matplotlib.pyplot as plt
import plotly.tools as ptools


def configure_plotly(user_name, api_key):
    ptools.set_credentials_file(username=user_name, api_key=api_key)
    ptools.set_config_file(world_readable=True, sharing='public')


def plot_data_plotly(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    # needs cufflinks library
    # plots scatter plot for xlabel v/s ylabel
    df.iplot(kind='scatter', title=title, xTitle=xlabel, yTitle=ylabel, filename='stcks')


def plot_data_matplotlib(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    # plots scatter plot for xlabel v/s ylabel
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

