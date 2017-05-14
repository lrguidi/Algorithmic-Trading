import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')


def get_data_from_yahoo(stock_list, start, end):

    main_df = pd.DataFrame()

    for ticker in stock_list:
        df = web.DataReader(ticker, "yahoo", start, end)
        # df[ticker] = df["Adj Close"]
        df[ticker[:-3]] = df["Adj Close"].pct_change() * 100.0
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

    return main_df


def visualize_data(df):

    df_corr = df.corr()
    # print(df_corr.head())

    data1 = df_corr.values
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig1.colorbar(heatmap1)

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap1.set_clim(-1, 1)
    plt.tight_layout()
    plt.savefig("correlations.png", dpi = (300))
    plt.show()


if __name__ == "__main__":
    symbols_list = ["AGRO.BA","ALUA.BA","APBR.BA","AUSO.BA","BMA.BA","CECO2.BA","CELU.BA","CEPU.BA","COME.BA",
                    "CRES.BA","CTIO.BA","EDN.BA","ERAR.BA","FRAN.BA","GGAL.BA","JMIN.BA","MIRG.BA","PAMP.BA",
                    "PESA.BA","PETR.BA","SAMI.BA","TECO2.BA","TGNO4.BA","TGSU2.BA","TRAN.BA","TS.BA","YPFD.BA"]

    start_date = dt.datetime(2015, 4, 20)
    end_date = dt.datetime(2017, 4, 25)

    df_stocks = get_data_from_yahoo(symbols_list,start_date,end_date)
    visualize_data(df_stocks)