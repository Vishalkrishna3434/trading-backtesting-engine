def compute_signals(df,short,long):
   df1=df.copy()
   df1['SMA_short']=df['Close'].rolling(short).mean()
   df1['SMA_long']=df['Close'].rolling(long).mean()
   df1.dropna(inplace=True)
   df1['Signal']=0
   df1.loc[df1['SMA_short']>df1['SMA_long'],'Signal'] =1
   df1.loc[df1['SMA_short']<df1['SMA_long'],'Signal'] =-1
   df1['Position']=df1['Signal'].shift(1) # to avoid look ahead bias
   return df1
 
   
     
