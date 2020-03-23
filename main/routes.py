#路徑模組
from flask import render_template, url_for, flash, redirect
from main import app
from main.models import User, Staff, Event
from main.forms import LoginForm, ResetForm

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

#帳號系統，在此login與reset都是使用同一個模板
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('account.html', form=form, title='登入系統')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('account.html', form=form, title='重設密碼')

@app.route('/logout')
def logout():
    return 'logout'