# SimpleQuantInvestment
Simple portfolio maker using financial statements.

**Note:** 현재 버전은 데이터가 자동으로 갱신되지 않고 직접 재무제표를 사이트에서 다운받아 업데이트 해줘야 하는 버전입니다. 자동 갱신 버전 코드도 있었는데 어디론가 날라갔네요... [SEC API 사이트](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)에 접속해서 찾아보면 관련 방법으로 하는 방법도 알 수 있습니다.

## 사용 방법

### 1. 파이썬 설치

### 2. 가상환경 만들기
현재 폴더에서 마우스 우클릭으로 **Windows PowerShell**을 열고 다음 명령어 입력

```powershell
python -m venv portfolio_maker  
```

### 3. 가상환경 활성화  
powershell에 다음 명령어 입력
```powershell
.\portfolio_maker\Scripts\Activate.ps1  
```

안될 시 powershell에 다음 권한 활성화 명령어 입력 후 입력  
```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process  
```

### 4. requirements 패키지 설치  
powershell에 다음 명령어 입력  
```powershell
pip install -r requirements.txt  
```

### 5. 재무 데이터 준비  
아래 사이트 접속  
https://www.sec.gov/search-filings/edgar-application-programming-interfaces  

![사이트 접속 후 클릭](./site_desc.png)  

https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip 클릭하여 bulk data 다운로드  

압축 해제 후 현재 작업중인 폴더에 있는 data 폴더 안에 companyfacts 붙여넣기  

결과적으로 다음과 같은 경로가 되어야 합니다. 이름도 같아야 오류가 나지 않습니다.  
```plain text
현재 디렉토리
  └─ data
      └─ companyfacts
          ├─ CIK0000001750.json
          └─ ...
  ├─ portfolio_maker
  ├─ .gitignore
  ├─ all.ipynb
  ├─ collect_financial_data.py
  ├─ ...
  ├─ main.py
  ├─ exe.ps1
  └─ ...
```

### 6. 전체 실행 코드 실행  
인터넷이 연결된 환경에서 powershell에 아래 명령어를 입력합니다. 약 4시간 정도 소요됩니다.
```powershell
.\exe.ps1   
```

오류 메세지가 뜰 경우 다음과 같은 명령어를 입력하고 다시 시도합니다.
```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process  
```

대부분의 소요 시간은 yahoo finance 에서 가격과 거래량 데이터를 다운받는데 소요가 됩니다. 해당 데이터를 이미 가지고 있다면 main.py 파일의  collect_price_and_volume() 앞에 #하나를 붙여 관련 부분을 주석처리 하면 됩니다.  

```python
if __name__ == "__main__":
    create_mapper()
    collect_financial_data()
    #collect_price_and_volume()  <- 다음과 같이 변경
    concat_info()
    make_simple_portfolio(cur_date="2025-12-26")
```
단 이렇게 할 경우 제가 만들었던 형식(행: 날짜,  열: 종목)과 다르게 데이터가 들어온다면 아래 부분에서 오류가 발생할 수 있습니다.  

단순히 재무 데이터만 얻고 싶은 거라면 아래를 다 주석 처리하면 됩니다.  


추후에 다시 실행하고자 할 때는 가상환경만 활성화 한 후에 .\exe.sh1을 실행하면 됩니다.
