import os
import argparse
import pandas as pd
from strategy import compute_signals 
from metrics import compute_metrics
from visualize import save_chart

DEFAULT_TICKERS = ["AAPL","MSFT","GOOGL","AMZN","TSLA","JPM","NVDA","META","NFLX","AMD"]

parser=argparse.ArgumentParser()
parser.add_argument("--ticker",type=str,nargs='+',default=DEFAULT_TICKERS)
parser.add_argument('--short',type=int,default=20)
parser.add_argument('--long',type=int,default=50)
parser.add_argument('--bps',default=10)
args=parser.parse_args()

results=[]
for t in args.ticker:
     path=f"data/{t}.csv"
     if not os.path.exists(path):
        print(f"SKIP {t} — run fetch_data.py first")
        continue
     
     df=pd.read_csv(path,index_col=0,parse_dates=True)
     df.index.name="Date"

     signals = compute_signals(df, short=args.short, long=args.long)
     d, m    = compute_metrics(signals, bps=args.bps)
     save_chart(d, t, m)

     results.append({'Ticker': t,**m})
     print(f"{t}: \n Sharpe={m['sharpe']} \n MaxDD={m['max_dd']}% \n Strategy={m['strat_ret']}% \n Market={m['market_ret']}% \n Trades={m['n_trades']}")

summary= pd.DataFrame(results).sort_values('sharpe',ascending=False)
summary.to_csv("results_summary.csv",index=False)
print("\n",summary.to_string(index=False))
