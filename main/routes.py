#路徑模組
from flask import render_template, url_for, flash, redirect, request
from main import app, db
from main.models import User, Event, Team
from main.forms import LoginForm, ResetForm, ScanForm
from flask_login import login_user, current_user, logout_user

'''
@app.route('/')
def init_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
'''
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('team'))
    else:
        return redirect(url_for('login'))

@app.route('/team')
def team():
    if current_user.is_authenticated:
        return render_template('team.html', title='積分系統', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/rank')
def rank():
    return 'rank'

@app.route('/info')
def info():
    if current_user.is_authenticated:
        return render_template('info.html', title='活動資訊', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/comment')
def chat():
    return 'comment'

@app.route('/thanks')
def thanks():
    if current_user.is_authenticated:
        return render_template('thanks.html', title='銘謝', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/scanner')
def scanner():
    if current_user.is_authenticated:
        return render_template('scanner_rework.html')
    else:
        return redirect(url_for('login'))

#帳號系統，在此login與reset都是使用同一個模板account.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        if user and user.account == user.password:
            login_user(user)
            flash('請設定新密碼', 'danger')
            return redirect(url_for('reset'))
        elif user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('帳號或密碼錯誤', 'danger')
    return render_template('account.html', form=form, title='登入系統')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        form = ResetForm()
        if form.validate_on_submit():
            user = User.query.filter_by(account=form.account.data).first()
            if current_user==user and form.account.data != form.password.data:
                user.password = form.password.data
                user.nickname = form.nickname.data
                db.session.commit()
                logout_user()
                return redirect(url_for('login'))
            elif current_user==user and form.account.data == form.password.data:
                flash('不可以與原始密碼相同', 'danger')
            else:
                flash('帳號錯誤', 'danger')
        return render_template('account.html', form=form, title='重設帳戶')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))