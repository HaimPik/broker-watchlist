from flask import Flask, request ,redirect, url_for, render_template, flash 
from utils import load_watchlists,save_watchlist,fetch_tickers_data

app = Flask(__name__)
app.secret_key = 'qwerty'

@app.route('/', methods=['GET','POST'])
def index():
    tickers = load_watchlists()
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper().strip()
        if not ticker:
            flash('Enter a legal ticker', 'error')
        else:
            data = fetch_tickers_data(ticker)
            if data:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)
                    flash(f'{ticker} added succesfully','success')
                else:
                    flash(f'{ticker} already added','info')
            else:
                flash(f'{ticker} is problamtic','error')
            return redirect(url_for('index'))
    else:
        stonks= []
        for ticker in tickers:
            data = fetch_tickers_data(ticker)
            if data:
                stonks.append(data)
        return render_template('index.html',stocks=stonks)
                        

@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlists()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f'{ticker} removed succesfully','success')
    else: 
        flash(f'{ticker} is not in list','error')
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
    