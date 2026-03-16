import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def save_chart(d,ticker,metrics,out="charts"):
   os.makedirs(out,exist_ok=True)

   fig,(ax1,ax2,ax3) = plt.subplots(3,1,figsize=(14,10),gridspec_kw={'height_ratios : ' [2,1,1]})

   fig.suptitle(f"{ticker} | sharpe {metrics['sharpe']} | Max DrawDown {metrics['max_dd']} | Total Trades {metrics['n_trades']}",fontsize=12,fontweight='bold')

   # ── Panel 1: Price + SMAs + buy/sell markers ─────────────────────────

   ax1.plot(d.index, d['Close'],     color='#333333', lw=1,   label='Close')
   ax1.plot(d.index, d['SMA_short'], color='#2196F3', lw=1.2, label='SMA 20')
   ax1.plot(d.index, d['SMA_long'],  color='#FF9800', lw=1.2, label='SMA 50')

   ax1.fill_between(d.index, d['SMA_short'], d['SMA_long'],where=d['SMA_short'] >= d['SMA_long'],alpha=0.15, color='green')
   ax1.fill_between(d.index, d['SMA_short'], d['SMA_long'],where=d['SMA_short'] < d['SMA_long'],alpha=0.15, color='red')

   # Crossover column from metrics.py: 2=buy, -2=sell
   buys  = d[d['Crossover'] ==  2]
   sells = d[d['Crossover'] == -2]
   ax1.scatter(buys.index,  buys['Close'],  marker='^', color='#4CAF50',s=70, zorder=5, label=f'Buy ({len(buys)})')
   ax1.scatter(sells.index, sells['Close'], marker='v', color='#F44336',s=70, zorder=5, label=f'Sell ({len(sells)})')

   ax1.set_ylabel("Price (USD)")
   ax1.legend(fontsize=0.8)
   ax1.plot()

   # ── Panel 2: Equity curve vs buy-and-hold ────────────────────────────

   ax2.plot(d.index, d['Cum_Strategy'], color='#2196F3', lw=1.5,label=f"Strategy {metrics['strat_ret']:+.1f}%")
   ax2.plot(d.index, d['Cum_Market'],   color='#999999', lw=1.5, ls='--',label=f"Buy & Hold {metrics['market_ret']:+.1f}%")

   ax2.axhline(1,color='black',lw=0.5,ls=':')

   ax2.set_ylabel('Cumulative Return')
   ax2.legend(fontsize=8)
   ax2.grid(alpha=0.3)

   # ── Panel 3: Drawdown ─────────────────────────────────────────────────

   dd=((d['Cum_Strategy']-d['Cum_Strategy'].cummax()) / d['Cum_Strategy'].cummax()*100)
   
   ax3.fill_between(d.index, dd, 0, color='#F44336', alpha=0.35)
   ax3.axhline(metrics['max_dd'], color='#B71C1C', lw=1, ls='--',label=f"Max DrawDown {metrics['max_dd']}%")
  
   ax3.set_ylabel('Drawdown (%)')
   ax3.set_xlabel('Date')
   ax3.legend(fontsize=8)
   ax3.grid(alpha=0.3)

   # ── Date formatting on all panels ───────────────────────────

   for ax in (ax1,ax2,ax3):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
   
   plt.gcf().autofmt_xdate()
   plt.tight_layout()
   plt.savefig(f"{out}/{ticker}.png",dpi=150,bbox_inches='tight')
   plt.close()
   print(f" Chart Saved -> {out}/{ticker}.png ")
