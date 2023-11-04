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
                                cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    with connection.cursor() as cursor:
        sql1 = "SELECT * FROM SelectedTrades"
        sql2 = "SELECT * FROM VolumeDeltaSummary"
        cursor.execute(sql1, sql2)
        data1, data2 = cursor.fetchall()
        
    return render_template('index.html', summary=data2, trades=data1)


@app.route('/home')
def home():
    '''Returns the homepage'''
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
