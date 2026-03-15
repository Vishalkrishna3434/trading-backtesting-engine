import numpy as np

def compute_metrics(d,bps=10):
     d=d.copy()
     
     d['Crossover'] = d['Signal'].diff().fillna(0)
     
     d['Market_Ret'] = d['Close'].pct_change()
     d['Strategy_Ret']=d['Position']*d['Market_Ret']
     
     crossovers=d['Signal'].diff().fillna(0).abs()
     d['Strategy_Ret'] -= crossovers*(bps/10000)
     
     d.dropna(inplace=True)
     
     d['Cum_Market']=(1+d['Market_Ret']).cumprod()
     d['Cum_Strategy']=(1+d['Strategy_Ret']).cumprod()
     
     sharpe= ( d['Strategy_Ret'].mean() / d['Strategy_Ret'].std() ) * np.sqrt(252)
     
     max_dd=( (d['Cum_Strategy']-d['Cum_Strategy'].cummax()) /d['Cum_Strategy'].cummax() ).min()
     
     return d,{
       'sharpe' : round(sharpe,2),
       'max_dd' : round(max_dd * 100 , 2),
       'strat_ret' : round((d['Cum_Strategy'].iloc[-1]-1) *100, 2),
       'market_ret' : round((d['Cum_Market'].iloc[-1]-1) *100, 2),
       'n_trades' : int(crossovers.sum() / 2)
     }