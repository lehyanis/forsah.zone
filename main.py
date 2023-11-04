from flask import Flask, render_template
import pymysql
import pymysql.cursors
import os

app = Flask(__name__)
connection = pymysql.connect(host='monorail.proxy.rlwy.net',
                                port=55068,
                                user='root',
                                password='46f23AA--1Ga3h62GfcFGGF35GBcBEa2',
                                database='railway',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor,
                                client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)

@app.route('/')
def index():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM SelectedTrades"
        cursor.execute(sql)
        SelectedTrades = cursor.fetchall()
        
        sql2 = "SELECT * FROM VolumeDeltaSummary"
        cursor.execute(sql2)
        VolumeDeltaSummary = cursor.fetchall()
   
    return render_template('index.html', summary=VolumeDeltaSummary, trades=SelectedTrades)


@app.route('/home')
def home():
    '''Returns the homepage'''
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
