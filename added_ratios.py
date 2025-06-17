import yfinance as yf
import pandas as pd

Data = pd.read_excel('optimized_portfolio_largecap.xlsx')

List = Data['Stock']

roa=[]
roe=[]
pe=[]

for ticker in List:
    stock = yf.Ticker(str(ticker)+".NS")
    info = stock.info

    roa.append(info.get("returnOnAssets", None))
    roe.append(info.get("returnOnEquity", None))
    pe.append(info.get("trailingPE", None))

Data['ROA'] = roa
Data['ROE'] = roe
Data['P/E'] = pe

Data.to_excel('final_largecap_with_ratios.xlsx',index = False)