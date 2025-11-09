'''
Implementation of a Mean Reversion Trading Strategy using Z-Score on historical price data:

1. calculate the 20-day moving average price
2. We calculate the 20-day standard deviation
3. We calculate the z-score as:

zscore = (Price- MovingAverage(20days))/StdDev(20days)

If the price crosses the upper band (the moving average 20 days + n_std standard deviation), a sell order is triggered. It means that the instrument is overbought.

If the price goes below the lower band (the moving average 20 days – n_std standard deviation), a buy order is triggered.'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_20_day_moving_average(price_series):
    return price_series.rolling(window=20).mean() # 20-day moving average

def calculate_20_day_std(price_series):
    return price_series.rolling(window=20).std() # 20-day standard deviation

# def calculate_z_score(price_series, moving_average, std_dev):
#     return (price_series - moving_average) / std_dev #zscore = (Price- MovingAverage(20days))/StdDev(20days)


def plot_z_score(ticker, price_series, moving_average, std_dev, n_std=1.5):
    fig = plt.figure(figsize=(12, 8))
    # Calculate upper and lower bands
    upper_band = moving_average + n_std * std_dev
    lower_band = moving_average - n_std * std_dev
    plt.plot(price_series.index, price_series, label='Price', color='black', linewidth=1)
    plt.plot(moving_average.index, moving_average, label='MA(20)', color='blue', linewidth=1.5)
    plt.plot(upper_band.index, upper_band, label=f'Upper Band (+{n_std}σ)', color='red', linestyle='--')
    plt.plot(lower_band.index, lower_band, label=f'Lower Band (-{n_std}σ)', color='green', linestyle='--')
    plt.fill_between(price_series.index, lower_band, upper_band, alpha=0.2, color='gray')
    plt.title(f'{ticker} - Mean Reversion Strategy')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    data = pd.read_csv('csi300_date_close_data.csv', index_col='Date', parse_dates=True)
    # Process only first few tickers to avoid too many plots
    tickers_to_plot = data.columns[:3] 
    for ticker in tickers_to_plot:
        price_series = data[ticker].dropna()  # Remove NaN values
        if len(price_series) < 20:  # Skip if not enough data
            print(f"Skipping {ticker} - insufficient data")
            continue
        # Calculate moving average and standard deviation
        moving_average = calculate_20_day_moving_average(price_series)
        std_dev = calculate_20_day_std(price_series)
        # Plot comprehensive mean reversion analysis
        plot_z_score(ticker, price_series, moving_average, std_dev, n_std=1.5)


if __name__ == "__main__":
    main()
