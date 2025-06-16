import yfinance as yf
import pandas as pd
from nifty_50 import not_taken



results = []

def get_current_price(symbol):
          ticker_obj = yf.Ticker(symbol)
          todays_data = ticker_obj.history(period='1d')
          return todays_data['Close'][0]

for ticker in not_taken:
    try:
        df = yf.download(ticker, start='2020-01-01', end='2025-01-01', progress=False)
        
        # Fix MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty or 'Close' not in df.columns:
            print(f"Skipping {ticker}: No valid data")
            continue

        df['Year'] = df.index.year
        yearly = df.groupby('Year')['Close'].agg(['first', 'last'])

        if yearly.empty or yearly.isnull().any().any():
            print(f"Skipping {ticker}: Incomplete yearly data")
            continue

        annual_returns = ((yearly['last'] - yearly['first']) / yearly['first']) * 100
        cagr = ((yearly['last'].iloc[-1] / yearly['first'].iloc[0]) ** (1 / len(yearly)) - 1) * 100
        volatility = annual_returns.std()
        
        
        if cagr > 15:
            current_price = get_current_price(ticker)
            results.append({
                'Stock': ticker.replace('.NS', '').upper(),
                'CMP': round(current_price, 2) if current_price else 'N/A',
                'CAGR (%)': round(cagr, 2),
                'Volatility (%)': round(volatility, 2)
            })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# Save to Excel
if results:
    df_out = pd.DataFrame(results)
    df_out.to_excel("midsmall_cap.xlsx", index=False)
    print("Results saved to midsmall_cap.xlsx")
else:
    print("No stocks met the CAGR > 15 percent criterion.")
