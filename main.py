from flask import Flask, render_template
import pymysql
import pymysql.cursors
import os

app = Flask(__name__)

def get_db_connection():
    if 'db_connection' not in g:
        g.db_connection = pymysql.connect(
            host='monorail.proxy.rlwy.net',
            port=55068,
            user='root',
            password='46f23AA--1Ga3h62GfcFGGF35GBcBEa2',
            database='railway',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
        )
    return g.db_connection

@app.before_request
def before_request():
    g.db = get_db_connection()

@app.teardown_request
def teardown_request(exception=None):
    db_connection = g.pop('db_connection', None)

    if db_connection is not None:
        db_connection.close()

@app.route('/')
def index():
    '''Returns the homepage'''
    cursor = g.db.cursor()
    sql = "SELECT * FROM SelectedTrades"
    cursor.execute(sql)
    SelectedTrades = cursor.fetchall()
    
    sql2 = "SELECT * FROM VolumeDeltaSummary"
    cursor.execute(sql2)
    VolumeDeltaSummary = cursor.fetchall()

    return render_template('index.html', summary=VolumeDeltaSummary, trades=SelectedTrades)

# ... rest of the app

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
