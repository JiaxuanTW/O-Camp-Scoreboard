# 路徑模組
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from main import app, db
from main.forms import (CardForm, ClueForm, DomainForm, InfoForm, LoginForm,
                        ResetForm, TradeForm)
from main.models import BanCard, Domain, Event, Notice, Team, User
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


# 計時器，檢查功能卡狀態
def checkStatus():
    teamList = Team.query.all()
    for index in teamList: # 檢查我BAN我自己是否到期
        if index.selfBanCardTime != None and datetime.utcnow() > index.selfBanCardTime:
            index.selfBanCardStatus = 0
            db.session.add(index)
            db.session.commit() 

    banCardList = BanCard.query.all() # 檢查禁止闖關是否到期
    for index in banCardList:
        if index.stage1_time != None and datetime.utcnow() > index.stage1_time:
            index.stage1_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage2_time != None and datetime.utcnow() > index.stage2_time:
            index.stage2_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage3_time != None and datetime.utcnow() > index.stage3_time:
            index.stage3_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage4_time != None and datetime.utcnow() > index.stage4_time:
            index.stage4_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage5_time != None and datetime.utcnow() > index.stage5_time:
            index.stage5_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage6_time != None and datetime.utcnow() > index.stage6_time:
            index.stage6_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage7_time != None and datetime.utcnow() > index.stage7_time:
            index.stage7_status = 0
            db.session.add(index)
            db.session.commit()
        if index.stage8_time != None and datetime.utcnow() > index.stage8_time:
            index.stage8_status = 0
            db.session.add(index)
            db.session.commit()

scheduler = BackgroundScheduler() 
scheduler.add_job(func=checkStatus, trigger="interval", seconds=60)
scheduler.start()


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

        userList = User.query.all()
        teamList = Team.query.all()
        eventList = Event.query.all() # TODO: 設定順序
        banCardList = BanCard.query.all()
        domainList = Domain.query.all()
        noticeList = Notice.query.all()

        if tradeform.validate_on_submit():
            newEvent = Event(coins=tradeform.coins.data, 
                            sender_id=current_user.id, team_id=tradeform.team_id.data)
            targetTeam = Team.query.filter_by(id=tradeform.team_id.data).first()
            targetTeam.team_coins = targetTeam.team_coins + tradeform.coins.data
            db.session.add(newEvent)
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('dashboard'))
        
        if cardform.validate_on_submit():
            targetTeam = Team.query.filter_by(id=cardform.team_receive.data).first()

            if cardform.card.data == 1:
                targetTeam.clueCardStatus += 1
                db.session.add(targetTeam)
                db.session.commit()
                if targetTeam.clueCardStatus > 1:
                    targetTeam.clueCardStatus = 1
                if cardform.team_sent.data == 1:
                    targetTeam.clueCardContent = '阿瑞斯小隊'
                if cardform.team_sent.data == 2:
                    targetTeam.clueCardContent = '雅典娜小隊'
                if cardform.team_sent.data == 3:
                    targetTeam.clueCardContent = '阿波羅小隊'
                if cardform.team_sent.data == 4:
                    targetTeam.clueCardContent = '波賽頓小隊'
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 2:
                targetTeam.clueCardStatus -= 1
                db.session.add(targetTeam)
                db.session.commit()
                if targetTeam.clueCardStatus < 1:
                    targetTeam.clueCardStatus = -1
                if cardform.team_sent.data == 1:
                    targetTeam.clueCardContent = '阿瑞斯小隊'
                if cardform.team_sent.data == 2:
                    targetTeam.clueCardContent = '雅典娜小隊'
                if cardform.team_sent.data == 3:
                    targetTeam.clueCardContent = '阿波羅小隊'
                if cardform.team_sent.data == 4:
                    targetTeam.clueCardContent = '波賽頓小隊'
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 3:
                targetTeam.clueCardStatus = 0
                targetTeam.clueCardContent = None
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 4: # TODO: 更新發送小隊資訊
                targetTeam.selfBanCardStatus = 1
                targetTeam.selfBanCardTime = datetime.utcnow() + timedelta(minutes=15)
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 5:
                StageBanTeam = BanCard.query.filter_by(id=cardform.team_receive.data).first()
                if cardform.stageSelect1.data == 1:
                    StageBanTeam.stage1_status = 1
                    StageBanTeam.stage1_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage1_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 2:
                    StageBanTeam.stage2_status = 1
                    StageBanTeam.stage2_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage2_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 3:
                    StageBanTeam.stage3_status = 1
                    StageBanTeam.stage3_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage3_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 4:
                    StageBanTeam.stage4_status = 1
                    StageBanTeam.stage4_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage4_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 5:
                    StageBanTeam.stage5_status = 1
                    StageBanTeam.stage5_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage5_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 6:
                    StageBanTeam.stage6_status = 1
                    StageBanTeam.stage6_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage6_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 7:
                    StageBanTeam.stage7_status = 1
                    StageBanTeam.stage7_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage7_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 8:
                    StageBanTeam.stage8_status = 1
                    StageBanTeam.stage8_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage8_content = '停用'
                    db.session.add(StageBanTeam)
                    db.session.commit()

            if cardform.card.data == 6:
                targetTeam.isolateCardStatus = 1
                targetTeam.isolateCardTime = datetime.utcnow()
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 7:
                targetTeam.isolateCardStatus = 0
                targetTeam.isolateCardTime = None
                db.session.add(targetTeam)
                db.session.commit()

            return redirect(url_for('dashboard'))

        if clueform.validate_on_submit():
            targetTeam = Team.query.filter_by(id=clueform.team_id.data).first()
            targetTeam.clues += clueform.clues.data
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if domainform.validate_on_submit(): # TODO: 設定刪除狀態清單
            targetDomain = Domain.query.filter_by(id=domainform.stageSelect.data).first()
            targetDomain.time = datetime.utcnow()
            targetDomain.team_id = domainform.team_id.data
            db.session.add(targetDomain)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if infoform.validate_on_submit():
            print(infoform.text.data)
            return redirect(url_for('dashboard'))

        return render_template('dashboard.html', tradeform=tradeform, infoform=infoform,
                            clueform=clueform, domainform=domainform, cardform=cardform, 
                            teamList=teamList, domainList=domainList, eventList=eventList,
                            userList=userList, banCardList=banCardList)
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
                            sender_id=user.id, team_event_id=user.team_id)
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
