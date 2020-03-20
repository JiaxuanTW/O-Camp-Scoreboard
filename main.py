from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

p_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(p_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return 'team'

@app.route('/rank')
def rank():
    return 'rank'

@app.route('/info/roommate')
def roommate():
    return 'roommate'

@app.route('/info/teammate')
def teammate():
    return 'teammate'

@app.route('/info/timetable')
def timetable():
    return 'timetable'

@app.route('/bulletinboard')
def bulletin_board():
    return 'bulletin board'

@app.route('/chat')
def chat():
    return 'chat'

@app.route('/thanks')
def thanks():
    return 'thanks'

if __name__ == '__main__':
    app.run(debug=True)
