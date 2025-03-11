import json
import yfinance as yfin

WL = 'watchlist.json'

def save_watchlist(tickers):
    with open(WL, 'w') as f:
        json.dump(tickers,f)

def load_watchlists():
    try:
        with open(WL,'r') as f:
            tickers = json.load(f)
        return tickers
    except FileNotFoundError as err:
        return []
    

def fetch_tickers_data(ticker):
    
    try:
        stock = yfin.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            print(data)
            row = data.iloc[-1]
            price = row['Close']
            high = row['High']
            low = row['Low']
            vol = row['Volume']
            prev_close = stock.info.get('previousClose',price)
            change = price - prev_close
            change_pct =  (change/prev_close)*100 if prev_close else 0
            date_t = row.name.strftime("%d-%m-%Y, %H:%M:%S")
            #date = row.name.strftime("%Y-%m-%d")
            #print(f"Date: {date}")
            #closing_price = stock.history(period='5d')['Close'].get(date, 0)  
            market_cap = stock.info["marketCap"]
           
           
            
            return_data = { 
                        'ticker':ticker,
                        'price': f'${price:.2f}',
                        'date_time': date_t,
                        'change': change,
                        'change_pct': change_pct,
                        'high': f'${high:.2f}',
                        'low': f'${low:.2f}',
                        'volume': f'{vol:,}',
                        'market_cap': f'${market_cap:,}'
                        
               }
            return return_data
        else:
            return None
        
    except Exception:
        return None
            
        