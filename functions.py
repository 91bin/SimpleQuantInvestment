import yfinance as yf
import numpy as np
import datetime
import pandas as pd
import json
from tqdm import tqdm


def multiply_overflow(iterable):
    return np.exp(sum(np.log(iterable)))

def geo_mean_overflow(iterable):
    return np.exp(np.log(iterable).mean())

def get_index_date(date, prices):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    for i, e in enumerate(prices.index):
        if date <= datetime.datetime.strptime(e, '%Y-%m-%d'):
            return i
    return None


def get_price_date(date, prices):
    return prices.iloc[get_index_date(date, prices)]


def mean_yield(date, dur, prices):
    st = get_index_date(date, prices)
    yields = np.zeros(dur)
    cur_prices = prices[st:st+250].values
    after_prices = prices[st+dur:st+250+dur].values
    yields = after_prices/cur_prices
    return yields.mean(), yields[0]


def st_time():
    standards = [('02-20', '05-10'), ('05-20', '08-10'),('08-20', '11-10'),('11-20', '02-10')]
    standards_times = []
    year = 1900
    for e in standards:
        ds = datetime.datetime.strptime(e[0], '%m-%d')
        de = datetime.datetime.strptime(e[1], '%m-%d')
        p = datetime.datetime.strptime(str(year), '%Y')
        standards_times.append(((ds-p).days, (de-p).days))
    return standards_times

standards_times = st_time()


def YearQuarter(end):
    quarter =""
    d = datetime.datetime.strptime(end, '%Y-%m-%d')
    p = datetime.datetime.strptime(str(d.year), '%Y')
    days_from_first_date_of_year = (d-p).days
    year = str(d.year)
    if standards_times[0][0] < days_from_first_date_of_year and days_from_first_date_of_year<standards_times[0][1]:
        quarter = 'Q1'
    elif standards_times[1][0] < days_from_first_date_of_year and days_from_first_date_of_year<standards_times[1][1]:
        quarter = 'Q2'
    elif standards_times[2][0] < days_from_first_date_of_year and days_from_first_date_of_year<standards_times[2][1]:
        quarter = 'Q3'
    elif standards_times[3][0] < days_from_first_date_of_year:
        quarter = 'Q4'
    elif days_from_first_date_of_year<standards_times[3][1]:
        year = str(d.year-1)
        quarter = 'Q4'
    else:
        quarter = 'None'
    return year, quarter


def fill_init_stats(ticker, stat, stat_name, infos):
    comp_Stats = {}
    for i in range(len(stat)-1, 0, -1):
        e = stat[i]
        end = e['end']
        year, quarter = YearQuarter(end)
        if year not in comp_Stats:
            comp_Stats[year] = {}
        if quarter not in comp_Stats:
            comp_Stats[year][quarter] = {}
        comp_Stats[year][quarter]['val'] = e['val']
        comp_Stats[year][quarter]['end'] = e['end']
        comp_Stats[year][quarter]['filed'] = e['filed']
    infos[stat_name][ticker] = comp_Stats


def fill_dur_stats(ticker, stat, stat_name, infos):
    comp_Stats = {}
    for i in range(len(stat)-1, 0, -1):
        e = stat[i]
        start_date = datetime.datetime.strptime(e['start'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(e['end'], '%Y-%m-%d')
        days_diff = (end_date - start_date).days
        if days_diff>300:
            year = str(end_date.year)
            quarter = 'Y'
        elif 60 < days_diff and days_diff < 120:
            year, quarter = YearQuarter(e['end'])
        else:
            continue
        if year not in comp_Stats:
            comp_Stats[year] = {}
        if quarter not in comp_Stats:
            comp_Stats[year][quarter] = {}
        comp_Stats[year][quarter]['val'] = e['val']
        comp_Stats[year][quarter]['start'] = e['start']
        comp_Stats[year][quarter]['end'] = e['end']
        comp_Stats[year][quarter]['filed'] = e['filed']
    infos[stat_name][ticker] = comp_Stats


def fill_shares(ticker, stats, stat_name, infos):
    comp_Stats = {}
    for j in range(len(stats)):
        for i in range(len(stats[j])-1, 0, -1):
            e = stats[j][i]
            end = e['end']
            actual_val = stats[j][-1]['val']
            year, quarter = YearQuarter(end)
            if year not in comp_Stats:
                comp_Stats[year] = {}
            if quarter not in comp_Stats[year]:
                comp_Stats[year][quarter] = {'val':0}
                
            if comp_Stats[year][quarter]['val']<actual_val:
                comp_Stats[year][quarter]['val']= actual_val
            comp_Stats[year][quarter]['end'] = e['end']
            comp_Stats[year][quarter]['filed'] = e['filed']
    infos[stat_name][ticker] = comp_Stats



def find_quarters(s, e, y):
    result_quarters = []
    start_months = [[12, 1,2], [3, 4, 5], [6, 7, 8], [9, 10,11]]
    s = datetime.datetime.strptime(s, '%Y-%m-%d')
    e = datetime.datetime.strptime(e, '%Y-%m-%d')
    dur = int((e-s).days/99)+1
    #if dur!=4:
    #    print("this is something strange!", s, e)
    if s.month==11 or s.month == 2 or s.month ==5 or s.month ==8 and s.day>25:
        s = s+datetime.timedelta(days=30)
    for q in range(4):
        if s.month in start_months[q]:    #재정신이면 3월 31일에 시작해놓고 2쿼터라고 하지는 않겠지? ㅋㅋㅋㅋ
            i=q
            n=0
            while i<4:
                if int(y)==s.year+1 and s.month!=12:
                    result_quarters.append('PQ'+str(i+1))
                else:
                    result_quarters.append('Q'+str(i+1))
                i=i+1
                n=n+1
            i = 0
            while n<dur:
                if int(y)==s.year+1 and s.month!=12:
                    result_quarters.append('Q'+str(i+1))
                else:
                    result_quarters.append('NQ'+str(i+1))
                i=i+1
                n=n+1
    return result_quarters



def financial_file_open(ticker, Ticker_CIK_dict, base_path, verbose=False):
    ticker = ticker.upper()
    
    # 딕셔너리에 티커가 있는지 먼저 확인 (KeyError 방지)
    if ticker not in Ticker_CIK_dict:
        print(f"[{ticker}] 딕셔너리에 해당 티커의 CIK 정보가 없습니다.")
        return None

    cik_file_name = "CIK" + Ticker_CIK_dict[ticker] + ".json"
    filepath = base_path + cik_file_name
    
    try:
        # 파일 열기 시도
        with open(filepath, 'r') as f:
            json_data = json.load(f)
            if 'us-gaap' in json_data['facts'].keys():
                financials = json_data['facts']['us-gaap']
            elif 'ifrs-full' in json_data['facts'].keys():
                financials = json_data['facts']['ifrs-full']
            else:
                return None
            return financials
            
    except FileNotFoundError:
        # 파일이 존재하지 않을 시 실행
        if verbose:
            tqdm.write(f"[{ticker}] 파일이 존재하지 않습니다: {filepath}")
        return None
        
    except KeyError:
        # 파일은 있으나 us-gaap 키가 없을 시 실행 (데이터 손상 등)
        if verbose:
            tqdm.write(f"[{ticker}] 데이터 형식이 올바르지 않습니다 (us-gaap or ifrs-full 키 부재).")
        return None



quarters = ['Q1', 'Q2', 'Q3', 'Q4']

def fill_empty_quarter(data):
    for year in data:
        try:
            if all([q in data[year] for q in quarters]):
                continue

            #Y가 Q몇부터 Q몇인지 확인(전년도p, 내년도 n붙이기)(Y가 1~12일시 그냥 사용?)
            this_year = year
            last_year = str(int(year)-1)
            next_year = str(int(year)+1)
            quarters_included_in_annualdata = find_quarters(data[this_year]['Y']['start'], data[this_year]['Y']['end'], this_year)
            
            #Q몇이 비어있는지 확인
            no = None
            no_val = None
            for q in quarters:
                if q not in data[this_year]:
                    no = q

            #이번년도 start, end 사이에 해당 Q가 있을 경우
            if no in quarters_included_in_annualdata:
                sumval = 0
                for q in quarters_included_in_annualdata:
                    if q[0]=='Q':
                        appropriate_year = this_year
                    elif q[0]=='N':
                        appropriate_year = next_year
                    else:
                        appropriate_year = last_year
                    q = q[-2]+q[-1]
                    if q !=no:
                        #if appropriate_year not in data or q not in data[appropriate_year]: ->key error, continue
                        sumval+=data[appropriate_year][q]['val']
                no_val  = data[this_year]['Y']['val'] - sumval

            #annual_result = Q1+Q2+Q3+Q4        
            data[this_year][no] = {'val': no_val, 'end': data[this_year]['Y']['end'], 'filed': data[this_year]['Y']['filed']}
        except:
            continue