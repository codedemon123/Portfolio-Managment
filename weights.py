import pandas as pd
import yfinance
# Load your Excel file
df = pd.read_excel("midsmall_cap.xlsx")  # Replace with your filename

# Ensure CAGR and Volatility are in decimal (not percentage)
if df['CAGR (%)'].max() > 1:
    df['CAGR (%)'] = df['CAGR (%)'] / 100
if df['Volatility (%)'].max() > 1:
    df['Volatility (%)'] = df['Volatility (%)'] / 100

# Risk-free rate (6%)
risk_free_rate = 0.06

# Calculate Sharpe Ratio
df['Sharpe Ratio'] = (df['CAGR (%)'] - risk_free_rate) / df['Volatility (%)']

# Remove negative or NaN Sharpe Ratios (optional, if needed)
df = df[df['Sharpe Ratio'] > 0].copy()

# Calculate weights proportional to Sharpe Ratio
df['Weight %'] = df['Sharpe Ratio'] / df['Sharpe Ratio'].sum() * 100


# Save to new Excel file
df.to_excel("optimized_portfolio_midsmallcap.xlsx", index=False)

print("Portfolio optimization complete. File saved as 'optimized_portfolio.xlsx'")
