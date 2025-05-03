# README

## Overview

This repository contains four Python scripts designed for backtesting trading strategies using historical stock data from the S&P 500. Each script implements different strategies and analyses, allowing users to evaluate stock performance against various metrics.

## Files
When executing the following scripts, make sure that the folder strategy is in the same directory.

1. **backtest.py**
   - This script allows users to select a trading strategy from the available options. After running the script, users are prompted to choose a strategy.
   - It implements a simple trading strategy, with details available in the `strategy.py` file.
   - Upon execution, the script plots the best and worst excess return performing stocks under the selected strategy, comparing them to the return of a simple buy-and-hold strategy.

   **Usage**:
   ```bash
   python backtest.py
   ```

2. **backtest_AFopt.py**
   - This program optimizes the acceleration factor (AF) for the `SpotGreatTrend` strategy, which uses the Parabolic SAR indicator.
   - After running, it displays a plot showing the return against the selected AF values.
   - The implementation details of the `SpotGreatTrend` strategy can be found in the `SpotGreatTrend` class within the `multidataframe.py` file.
   
   **Usage**:
   ```bash
   python backtest_AFopt.py
   ```
3. **backtest_optimize.py**

   - This script performs a grid search to optimize the short and long Simple Moving Average (SMA) combinations for a golden cross strategy.
   - By default, it plots the performance chart for Amazon. Users can modify the stock by changing the input area in lines 16 to 25 of the code.
   - Refer to the list of stocks available for testing in the `sp500_sample` variable located on line 12.
     
   **Usage**:
   ```bash
   python backtest_optimize.py
   ```
4. **backtest_sharpe.py**
   - This script applies the `SpotGreatTrend` strategy to the top 100 S&P 500 companies.
   - By default, it plots the performance for Amazon and outputs the average return of the buy-and-hold strategy compared with the expected return, variance, Sharpe ratio, average trades count, and average win rate of the strategy.
     
    **Usage**:
   ```bash
   python backtest_sharpe.py
   ```
## Dependencies
To run the programs, ensure you have the following dependencies installed:
   ```bash
  pip install lxml tkinter backtrader
   ```
## Important Note
If the programs are run too frequently, you may encounter errors from the yfinance library due to too many requests. It is advisable to space out your requests or implement rate limiting.


   
