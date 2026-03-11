# 📈 Algorithmic Trading Backtesting Engine

A Python-based engine to evaluate algorithmic trading strategies 
on historical market data with performance analytics.

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Stack](https://img.shields.io/badge/Stack-Python-blue)

## ✨ Features
- Load historical stock data via yfinance
- Moving average crossover strategy
- Simulated trade execution (buy/sell signals)
- Performance metrics: cumulative return, max drawdown
- Equity curve visualization

## 🛠 Tech Stack
- Python
- Pandas
- Matplotlib
- yfinance

## ⚙️ Setup
```bash
pip install pandas yfinance matplotlib
python backtest.py
```

## 📊 Metrics Calculated
- Total Return (%)
- Maximum Drawdown
- Win Rate
- Equity Curve
