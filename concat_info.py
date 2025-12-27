import tqdm
from functions import *

def concat_info():
    with open("./data/infos.json", "r") as st_json:
        infos = json.load(st_json)

    price_path = "./data/price.csv"
    price = pd.read_csv(price_path)
    price.index = price['Date']
    price = price.drop('Date', axis = 1)

    volume_path = "./data/volume.csv"
    volume = pd.read_csv(volume_path)
    volume.index = volume['Date']
    volume = volume.drop('Date', axis = 1)

    df_price = price
    df_volume = volume

    factors = []
    current_factors = []
    for i, ticker in enumerate(tqdm(df_price.columns)):
        try:
            prices = df_price[ticker]
            so = infos['so'][ticker]
            so_year = so[next(iter(so))]
            so_val = so_year[next(iter(so_year))]['val'] # this does not reflect new stock issue
        except:
            continue
        for year in range(2008, 2026):
            try:
                seq = infos['seq'][ticker]
                nil = infos['nil'][ticker]

                ind = get_index_date(str(year)+"-01-01", prices = prices)

                date = datetime.datetime.strptime(str(year), '%Y')
                
                while date.year==year:    
                    fact_vals = [0,0]   #seq, nil
                    for j, fact in enumerate([seq, nil]):
                        if date < datetime.datetime.strptime(fact[str(year-1)]['Q4']['filed'] ,'%Y-%m-%d'):
                            fact_val = fact[str(year-1)]['Q3']['val']
                        elif date < datetime.datetime.strptime(fact[str(year)]['Q1']['filed'] ,'%Y-%m-%d'):
                            fact_val = fact[str(year-1)]['Q4']['val']
                        elif date < datetime.datetime.strptime(fact[str(year)]['Q2']['filed'] ,'%Y-%m-%d'):
                            fact_val = fact[str(year)]['Q1']['val']
                        elif date < datetime.datetime.strptime(fact[str(year)]['Q3']['filed'] ,'%Y-%m-%d'):
                            fact_val = fact[str(year)]['Q2']['val']
                        else:
                            fact_val = fact[str(year)]['Q3']['val']
                        fact_vals[j] = fact_val

                    price = prices.iloc[ind]
                    market_cap = so_val*price

                    pbr = market_cap / fact_vals[0]
                    per = market_cap / fact_vals[1]
                    if ind+250<len(prices):
                        Yield = prices.iloc[ind+250]/prices.iloc[ind]
                        factors.append((date, int(year), ticker, pbr, per, Yield, fact_vals[0], volume[ticker].iloc[ind+250], ind))
                    else:
                        current_factors.append((date, int(year), ticker, pbr, per, 0, fact_vals[0], 0, ind))
                    ind += 1
                    date = datetime.datetime.strptime(prices.index[ind+1], "%Y-%m-%d")

            except Exception as e:
                #tqdm.write(f"An unexpected error occurred: {e} {ticker} {year}")
                continue


    df_out = pd.DataFrame(factors)
    df_out.columns = ['date', 'year', 'ticker', 'pbr', 'per', 'yield', 'seq', 'volume', 'ind']
    df_out = df_out.sort_values(by = ['date', 'ticker'], ascending=[True, True])
    df_out = df_out.reset_index(drop=True)
    df_out.to_csv("./data/factors.csv", index=False)

    df_out_current = pd.DataFrame(current_factors)
    df_out_current.columns = ['date', 'year', 'ticker', 'pbr', 'per', 'yield', 'seq', 'volume', 'ind']
    df_out_current = df_out_current.sort_values(by = ['date', 'ticker'], ascending=[True, True])
    df_out_current = df_out_current.reset_index(drop=True)
    df_out_current.to_csv("./data/factors_current.csv", index=False)

if __name__ == "__main__":
    concat_info()