import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


def get_tickers_from_csv():
    """
    Read CSI 300 tickers from CSV file and convert to Yahoo Finance format.
    """
    try:
        df = pd.read_csv('CSI300tickers.csv')
        raw_tickers = df['Ticker'].tolist()
        yf_tickers = []
        
        for ticker in raw_tickers:
            if pd.isna(ticker) or ticker == 'Ticker':  # Skip header or NaN values
                continue
            if ':' in str(ticker):
                try:
                    # Handle both regular space and non-breaking space
                    if ':\xa0' in ticker:  # Non-breaking space
                        exchange, code = ticker.split(':\xa0')
                    elif ': ' in ticker:  # Regular space
                        exchange, code = ticker.split(': ')
                    else:
                        # Just colon, no space
                        exchange, code = ticker.split(':')
                    
                    code = code.strip()
                    if exchange == 'SSE':
                        yf_ticker = f"{code}.SS"  # Shanghai Stock Exchange
                    elif exchange == 'SZSE':
                        yf_ticker = f"{code}.SZ"  # Shenzhen Stock Exchange
                    else:
                        continue  # Skip unknown exchanges
                    yf_tickers.append(yf_ticker)
                except ValueError:
                    # Skip tickers that don't split properly
                    print(f"Skipping ticker with unexpected format: {ticker}")
                    continue
        print(f"Sample tickers: {yf_tickers[:10]}, total converted: {len(yf_tickers)}")
        
        return yf_tickers
        
    except FileNotFoundError:
        print("CSI300tickers.csv file not found!")
        return []



end_date = datetime.now().date()
start_date = end_date - timedelta(days = 365) # 1 year back from now
tickers = get_tickers_from_csv()

all_data = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date, progress=True)
    if 'Close' in data.columns:
        all_data[ticker] = data['Close']
    else:
        all_data[ticker] = data
all_data.to_csv('csi300_date_close_data.csv')


