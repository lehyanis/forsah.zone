from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:RA2BkqTnxzsU20yp1Klr@containers-us-west-163.railway.app:6951/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    '''Returns the homepage'''
    data1 = db.session.execute(text("SELECT * FROM SelectedTrades")).fetchall()
    data2 = db.session.execute(text("SELECT * FROM VolumeDeltaSummary")).fetchall()
        
    return render_template('index.html', summary=data2, trades=data1)


@app.route('/home')
def home():
    '''Returns the homepage'''
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
