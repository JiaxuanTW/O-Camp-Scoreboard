#路徑模組
from flask import render_template
from main import app
from main.models import User, Staff, Event

@app.route('/')
def home():
    return render_template  ('layout.html', title='主頁面')

@app.route('/team')
def team():
    return render_template('team.html', title='積分系統')

@app.route('/rank')
def rank():
    return 'rank'

@app.route('/info')
def roommate():
    return render_template('info.html', title='活動資訊')

@app.route('/comment')
def chat():
    return 'comment'

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', title='銘謝')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return 'logout'