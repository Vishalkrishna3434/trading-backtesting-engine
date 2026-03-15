import yfinance as yf
import argparse
import os

DEFAULT_TICKERS = ["AAPL","MSFT","GOOGL","AMZN","TSLA","JPM","NVDA","META","NFLX","AMD"]

parser=argparse.ArgumentParser()

parser.add_argument("--ticker",type=str,nargs="+",default=DEFAULT_TICKERS)
parser.add_argument("--period",type=str,default="5y")

args=parser.parse_args()

os.makedirs("data",exist_ok=True)

for i,t in enumerate(args.ticker,1):
  df=yf.download(t,period=args.period,progress=False)
  df.dropna(inplace=True)
  df.to_csv(f"data/{t}.csv")
  print(f"[{i}/{len(args.ticker)}] -> {len(df)}rows saved") 

print("All data downloaded")