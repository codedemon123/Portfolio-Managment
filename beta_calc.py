import yfinance as yf
import pandas as pd

Data = pd.read_excel('optimized_portfolio_largecap.xlsx')

List = Data['Stock']

beta = []

for ticker in List:
    yoo = yf.Ticker(str(ticker)+".NS")
    b = yoo.info.get("beta3Year") or yoo.info.get("beta")
    beta.append(b)



Data['Beta'] = beta
Data.to_excel('final_largecap_with_ratios_and_beta.xlsx',index = False)