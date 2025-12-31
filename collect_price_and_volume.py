import yfinance as yf
import numpy as np
import json
import datetime
import pandas as pd
import os
from tqdm import tqdm
from functions import *

def collect_price_and_volume():
    print("Collecting price and volume data... This will take long time...")
    with open('./data/ticker_cik_mapping.json', 'r', encoding='utf-8') as f:
        t_to_c = json.load(f)

    start = '2008-01-01'
    end = '2025-12-27'

    price_data = pd.DataFrame()
    volume_data = pd.DataFrame()
    for i, tic in enumerate(tqdm(t_to_c)):
        try:
            d = yf.download(tic, start = start, end = end, progress = False)
            price = d['Close']
            volume = d['Volume']
            if (len(price)>0):
                price.name = tic
                price_data = pd.concat((price_data, price), axis = 1)
                volume.name = tic
                volume_data = pd.concat((volume_data, volume), axis=1)
        except:
            tqdm.write("exception")
            continue

    price_data.to_csv('./data/price.csv')
    volume_data.to_csv('./data/volume.csv')
    print("Finished Collecting price and volume data...")


if __name__ == "__main__":
    collect_price_and_volume()