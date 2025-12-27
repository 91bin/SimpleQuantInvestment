import requests
import json
import pandas as pd

def create_mapper():
    url = "https://www.sec.gov/files/company_tickers.json"

    # SEC는 요청 시 반드시 이메일 주소나 식별자를 헤더에 포함해야 함
    headers = {
        'User-Agent': 'bins (nagnebin@gmail.com)' 
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # 데이터프레임으로 변환
        df = pd.DataFrame.from_dict(data, orient='index')
        # 보기 좋게 컬럼명 변경 (cik_str -> CIK, ticker -> Ticker)
        df = df.rename(columns={'cik_str': 'CIK', 'ticker': 'Ticker', 'title': 'Name'})
        
        # CIK를 10자리 문자열로 포맷팅 (예: 789019 -> 0000789019) - 파일명 매칭용
        df['CIK'] = df['CIK'].apply(lambda x: str(x).zfill(10))
    else:
        print(f"Error: {response.status_code}")

    # 실행
    df_sec = df

    if df_sec is not None:
        ticker_list = df_sec['Ticker'].tolist()
        t_to_c = dict(zip(df_sec['Ticker'], df_sec['CIK']))
        
        print("다운로드 및 매핑 완료")
        print(f"총 종목 수: {len(t_to_c)}")

        with open('./data/ticker_cik_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(t_to_c, f, indent=4) # indent는 보기 좋게 들여쓰기 옵션

if __name__ == "__main__":
    create_mapper()