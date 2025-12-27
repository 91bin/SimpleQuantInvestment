import json
import datetime
import pandas as pd
import os
from tqdm import tqdm
from functions import *


def collect_financial_data():
    with open('./data/ticker_cik_mapping.json', 'r', encoding='utf-8') as f:
        t_to_c = json.load(f)

    #여기에다가 원하는 재무재표 항목 추가
    infos = {"seq":{}, "so":{}, "nil":{}}
    exceptioncount = 0
    base_path = "./data/companyfacts/" 

    for i, ticker in enumerate(tqdm(t_to_c)):
        try:
            financials = financial_file_open(ticker, t_to_c, base_path)

            # 여기에서 원하는 재무제표값 key 찾아서 입력...
            # EX) 총자본 & 당기순이익
            # 총자본 - PBR 계산에 사용
            if 'StockholdersEquity' in financials.keys():
                seq = financials['StockholdersEquity']['units']['USD']
            elif 'Equity' in financials:
                seq = financials['Equity']['units']['USD']
            else:
                seq = financials['StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest']['unit']['USD']
                
            # 당기순이익 - PER 계산에 사용
            if 'NetIncomeLoss' in financials:
                nil = financials['NetIncomeLoss']['units']['USD']
            else:
                nil = financials['ProfitLoss']['units']['USD']

            # 발행 주식수
            stock_outs = []
            if 'CommonStockSharesOutstanding' in financials:
                stock_outs.append(financials['CommonStockSharesOutstanding']['units']['shares'])
            if 'CommonStockSharesIssued' in financials:
                stock_outs.append(financials['CommonStockSharesIssued']['units']['shares'])
            if 'WeightedAverageNumberOfSharesOutstandingBasic' in financials:
                stock_outs.append(financials['WeightedAverageNumberOfSharesOutstandingBasic']['units']['shares'])
            if 'WeightedAverageNumberOfDilutedSharesOutstanding' in financials:
                stock_outs.append(financials['WeightedAverageNumberOfDilutedSharesOutstanding']['units']['shares'])

            # 총자본같이 기간이 필요없고 end_date만 있는 값들 전용 함수
            fill_init_stats(ticker, seq, 'seq', infos=infos)

            # 당기순이익같이 특정 기간동안 구해야 하는 값들 전용 함수 -> 1분기 즉 3개월 단위 처리
            fill_dur_stats(ticker, nil, 'nil', infos=infos)
            fill_empty_quarter(infos['nil'][ticker])

            # 발행 주식수 전용 함수
            fill_shares(ticker, stock_outs, 'so', infos=infos)

        except Exception as e:
            #tqdm.write(f"[{ticker}] 에러 발생: {type(e).__name__} - {e}")
            exceptioncount += 1
            continue
    print("exceptioncount: ", exceptioncount)
   
    with open("./data/infos.json", "w") as json_file:
        json.dump(infos, json_file)

if __name__ == "__main__":
    collect_financial_data()