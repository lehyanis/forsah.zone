from flask import Flask, render_template
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
engine = create_engine(
    "mysql+pymysql://root:RA2BkqTnxzsU20yp1Klr@containers-us-west-163.railway.app:6951/railway")

@app.route('/')
def index():
    '''Returns the homepage'''
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM avg_size")).fetchall()

        trade_data = conn.execute(text
            ('''SELECT symbol,date,DATE_FORMAT(time, '%H:%i:%s') AS time, close,price,size,conditions,Quote,`Signal`,QuoteCond, EMA
                FROM trades 
                where time between '16:00' and '23:00' 
                and date BETWEEN DATE_SUB((SELECT MAX(date) FROM trades), INTERVAL 3 DAY) AND (SELECT MAX(date) FROM trades)
                and conditions like '%Qualified%' or '%Sweep%' or '%Average Price%' or '%Derivatively%' or '%Out of Sequence%' 
                ''')
            ).fetchall()
        
        spy_only = conn.execute(text
            ('''SELECT symbol, date, time, close, price, size, conditions, Quote, QuoteCond, `Signal`, EMA FROM trades
                where size >= 200000 and symbol = 'SPY' 
                and date BETWEEN DATE_SUB((SELECT MAX(date) FROM trades), INTERVAL 5 DAY) AND (SELECT MAX(date) FROM trades)
                and conditions like '%Qualified%'
                order by size DESC; 
                ''')
            ).fetchall()
        
    return render_template('index.html', summary=results, trades=trade_data, spy=spy_only)


@app.route('/home')
def home():
    '''Returns the homepage'''
    return render_template('home.html')

@app.route('/summary')
def summary():
    '''Returns a list of trades from the database'''
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM avg_size")).fetchall()
    return render_template('summary.html', summary=results)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
