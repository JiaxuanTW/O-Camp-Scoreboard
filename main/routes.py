# 路徑模組
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from main import app, db
from main.forms import (CardForm, ClueForm, DomainForm, InfoForm, LoginForm,
                        ResetForm, TradeForm)
from main.models import BanCard, Domain, Event, Notice, Team, User
from apscheduler.schedulers.background import BackgroundScheduler


# 計時器，檢查功能卡狀態
import time
def checkStatus():
    print(time.strftime('%A, %d. %B %Y %I:%M:%S %p'))

scheduler = BackgroundScheduler() 
# scheduler.add_job(func=checkStatus, trigger="interval", seconds=3)
# scheduler.start()


# 系統分流
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('team'))
    else:
        return redirect(url_for('login'))


@app.route('/team')
def team():
    if current_user.is_authenticated:
        return render_template('team.html', title='隊伍資訊', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/rank')
def rank():
    if current_user.is_authenticated:
        return render_template('rank.html', title='個人排名', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/info')
def info():
    if current_user.is_authenticated:
        return render_template('info.html', title='活動資訊', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/detail')
def detail():
    if current_user.is_authenticated:
        return render_template('detail.html', title='收支明細', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/notice')
def notice():
    if current_user.is_authenticated:
        return render_template('notice.html', title='通知', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/domain')
def domain():
    if current_user.is_authenticated:
        return render_template('domain.html', title='占領戰', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        tradeform = TradeForm()
        clueform = ClueForm()
        domainform = DomainForm()
        cardform = CardForm()
        infoform = InfoForm()

        teamList = Team.query.all()

        if tradeform.validate_on_submit():
            # print(tradeform.team_id.data)
            # print(tradeform.coins.data)
            newEvent = Event(coins=tradeform.coins.data, 
                            sender_id=current_user.id, team_id=tradeform.team_id.data)
            targetTeam = Team.query.filter_by(id=tradeform.team_id.data).first()
            targetTeam.team_coins = targetTeam.team_coins + tradeform.coins.data
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('dashboard'))
        '''驗證錯誤輸入
        else:
            if 'team_id' in tradeform.errors.keys():
                flash('請選取小隊', 'danger')
            if 'coins' in tradeform.errors.keys():
                flash('請勿輸入非整數字元', 'danger')
        '''
        if cardform.validate_on_submit():
            print(cardform.card.data)
            print(cardform.team_sent.data)
            print(cardform.team_recieve.data)
            print(cardform.stageSelect1.data)
            return redirect(url_for('dashboard'))

        if clueform.validate_on_submit():
            print(clueform.team_id.data)
            print(clueform.clues.data)
            targetTeam = Team.query.filter_by(id=clueform.team_id.data).first()
            targetTeam.clues += clueform.clues.data
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if domainform.validate_on_submit():
            print(domainform.stageSelect.data)
            print(domainform.team_id.data)
            return redirect(url_for('dashboard'))

        if infoform.validate_on_submit():
            print(infoform.text.data)
            return redirect(url_for('dashboard'))

        return render_template('dashboard.html', tradeform=tradeform, infoform=infoform,
                            clueform=clueform, domainform=domainform, cardform=cardform, teamList=teamList)
    else:
        return redirect(url_for('login'))


@app.route('/manual')
def manual():
    if current_user.is_authenticated:
        return render_template('manual.html', title='手動模式', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/thanks')
def thanks():
    if current_user.is_authenticated:
        return render_template('thanks.html', title='銘謝', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if current_user.is_authenticated:
        form = TradeForm()
        if form.validate_on_submit():
            print('Scanner Page: Form submitted')
            user = User.query.filter_by(account=form.team_id.data).first()
            if user:
                event = Event(coins=form.coins.data,
                              reciever_id=user.id, team_event_id=user.team_id)
                db.session.add(event)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                return render_template('scanner.html', form=form, warn='查無此人')
        return render_template('scanner.html', form=form, warn='')
    else:
        return redirect(url_for('login'))


# 帳號系統，在此login與reset都是使用同一個模板 account.html
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
            if current_user == user and form.account.data != form.password.data:
                user.password = form.password.data
                user.nickname = form.nickname.data
                db.session.commit()
                logout_user()
                return redirect(url_for('login'))
            elif current_user == user and form.account.data == form.password.data:
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
