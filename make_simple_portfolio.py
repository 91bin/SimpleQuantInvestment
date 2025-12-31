import numpy as np
import json
import datetime
import pandas as pd
import os
from tqdm import tqdm
from functions import *

def make_simple_portfolio(cur_date):
    print("Making Simple Portfolio...")
    # 특정 날짜 기준 PBR or PER 하위 10% 종목 찾기
    factor = 'pbr'
    df_factors_ = pd.read_csv("./data/factors_current.csv")
    df_factors_.columns = ['date', 'year', 'ticker', 'pbr', 'per', 'yield', 'seq', 'tradingvolume', 'ind']

    #전처리 -> 이상값 제거
    df_factors = df_factors_.dropna(subset=[factor])
    df_factors.replace(np.inf, 3e14, inplace=True)
    data_refined = df_factors[df_factors[factor]>0]
    data_refined = data_refined[(df_factors['seq'] > df_factors['seq'].quantile(0.05))].reset_index(drop=True)

    date_series = data_refined['date']
    idx = date_series.searchsorted(cur_date, side='right') - 1
    if idx >= 0:
        cur_date = date_series.iloc[idx]
    else:
        print("해당 날짜보다 작거나 같은 값을 찾지 못하였습니다")
        return None

    data_refined = data_refined[data_refined['date'] == cur_date]
    data_refined.reset_index(drop=True,inplace=True)

    df_sorted= data_refined.sort_values(by=[factor],axis=0)
    start_factor = df_sorted[factor].quantile(q=0)
    end_factor = df_sorted[factor].quantile(q=0.1)
    df_q = df_sorted[(df_sorted[factor]>start_factor) & (df_sorted[factor] <= end_factor)]
    with open("./data/ticker_list.txt", 'w') as f:
        f.write(str(df_q["ticker"].to_numpy()))
    print(df_q["ticker"].to_numpy())
    print("Finished Making Simple Portfolio!")


def __init__():
    make_simple_portfolio(cur_date = "2025-12-26")