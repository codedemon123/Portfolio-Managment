import yfinance as yf
import pandas as pd

stocks = [
"3MINDIA.NS","AARTIIND.NS","ABB.NS","ABBOTINDIA.NS","ABCAPITAL.NS","ABFRL.NS","ACC.NS","ADANIENT.NS",
"ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS","ADANITRANS.NS","AIAENG.NS","AIRTEL.NS","ALKEM.NS",
"AMBUJACEM.NS","APOLLOHOSP.NS","APOLLOTYRE.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTRAL.NS","ATGL.NS",
"AUBANK.NS","AUROPHARMA.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJAJHLDNG.NS","BAJAJFINANCE.NS",
"BALKRISIND.NS","BALRAMCHIN.NS","BANDHANBNK.NS","BANKBARODA.NS","BANKINDIA.NS","BERGEPAINT.NS","BEL.NS",
"BHEL.NS","BIOCON.NS","BOSCHLTD.NS","BPCL.NS","BRITANNIA.NS","CADILAHC.NS","CANBK.NS","CANFINHOME.NS",
"CHOLAFIN.NS","CIPLA.NS","COALINDIA.NS","COFORGE.NS","COLPAL.NS","CONCOR.NS","COROMANDEL.NS","CROMPTON.NS",
"CUB.NS","CUMMINSIND.NS","DABUR.NS","DALBHARAT.NS","DEEPAKNTR.NS","DIVISLAB.NS","DLF.NS","DRREDDY.NS",
"EICHERMOT.NS","ESCORTS.NS","EXIDEIND.NS","FEDERALBNK.NS","GAIL.NS","GLAND.NS","GMRINFRA.NS","GODREJCP.NS",
"GODREJPROP.NS","GRANULES.NS","GRASIM.NS","GUJGASLTD.NS","HAVELLS.NS","HCLTECH.NS","HDFC.NS",
"HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDPETRO.NS","HINDUNILVR.NS",
"ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS","IDEA.NS","IDFCFIRSTB.NS","IEX.NS","IGL.NS","INDHOTEL.NS",
"INDIGO.NS","INDUSINDBK.NS","INDUSTOWER.NS","INFY.NS","IOC.NS","IPCALAB.NS","IRCTC.NS","ITC.NS",
"JINDALSTEL.NS","JSWSTEEL.NS","JUBLFOOD.NS","KOTAKBANK.NS","LALPATHLAB.NS","LAURUSLABS.NS","LICHSGFIN.NS",
"LT.NS","LTTS.NS","LTI.NS","LUPIN.NS","M&M.NS","M&MFIN.NS","MANAPPURAM.NS","MARICO.NS","MARUTI.NS",
"MGL.NS","MINDTREE.NS","MPHASIS.NS","MRF.NS","MUTHOOTFIN.NS","NATIONALUM.NS","NAUKRI.NS","NAVINFLUOR.NS",
"NESTLEIND.NS","NMDC.NS","NTPC.NS","OBEROIRLTY.NS","OFSS.NS","ONGC.NS","PAGEIND.NS","PEL.NS","PETRONET.NS",
"PFC.NS","PIDILITIND.NS","PIIND.NS","PNB.NS","POLYCAB.NS","POWERGRID.NS","PVR.NS","RBLBANK.NS","RECLTD.NS",
"RELAXO.NS","RELIANCE.NS","SAIL.NS","SBICARD.NS","SBILIFE.NS","SBIN.NS","SHREECEM.NS","SIEMENS.NS",
"SRF.NS","SRTRANSFIN.NS","SUNPHARMA.NS","SYNGENE.NS","TATACHEM.NS","TATACONSUM.NS","TATAMOTORS.NS",
"TATAPOWER.NS","TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS",
"TVSMOTOR.NS","UBL.NS","ULTRACEMCO.NS","UPL.NS","VBL.NS","VEDL.NS","VOLTAS.NS","WIPRO.NS","ZEEL.NS",
"ZYDUSLIFE.NS"
]

results = []

def get_current_price(symbol):
          ticker_obj = yf.Ticker(symbol)
          todays_data = ticker_obj.history(period='1d')
          return todays_data['Close'][0]

for ticker in stocks:
    try:
        df = yf.download(ticker, start='2015-01-01', end='2025-01-01', progress=False)
        
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
        
        
        if cagr > 10:
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
    df_out.to_excel("bluechip_filtered.xlsx", index=False)
    print("Results saved to bluechip_filtered.xlsx")
else:
    print("No stocks met the CAGR > 10 percent criterion.")
