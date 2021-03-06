# 路徑模組
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from main import app, db
from main.forms import (CardForm, ClueForm, DomainForm, InfoForm, LoginForm,
                        ResetForm, TradeForm)
from main.models import BanCard, Domain, Event, Notice, Team, User
from main.db_initialization import db_init, db_create, db_drop
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time


# 計時器，檢查功能卡狀態
def checkStatus():
    teamList = Team.query.all()
    for index in teamList:  # 檢查我BAN我自己是否到期
        if index.selfBanCardTime != None and datetime.utcnow() > index.selfBanCardTime:
            index.selfBanCardStatus = 0
            db.session.add(index)
            db.session.commit()

    banCardList = BanCard.query.all()  # 檢查禁止闖關是否到期
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


# Jinja引擎 自訂模組
@app.template_filter('timestamp')
def datetime_to_timestamp(value):
    # TODO: 發布前停用
    value = value + timedelta(hours=8)  # 調整時差
    return value.timestamp()


# 系統分流
@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.team_id == 5:
            return redirect(url_for('staff_team', team_id=1))
        return redirect(url_for('team'))
    else:
        return redirect(url_for('login'))


@app.route('/team')
def team():
    if current_user.is_authenticated:

        userList = User.query.order_by('id').all()
        teamList = Team.query.order_by('id').all()
        banCardList = BanCard.query.order_by('id').all()
        eventList = Event.query.filter_by(
            team_id=current_user.team_id).order_by(Event.time.desc()).all()

        return render_template('team.html', title='隊伍資訊', user=current_user, userList=userList,
                               teamList=teamList, banCardList=banCardList, eventList=eventList)
    else:
        return redirect(url_for('login'))


@app.route('/info')
def info():
    if current_user.is_authenticated:
        return render_template('info.html', title='活動資訊', user=current_user)
    else:
        return redirect(url_for('login'))


# TODO: 需移除
@app.route('/detail')
def detail():
    if current_user.is_authenticated:
        return render_template('detail.html', title='收支明細', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/notice')
def notice():
    messageList = Notice.query.order_by(Notice.time.desc()).all()

    if current_user.is_authenticated:
        return render_template('notice.html', title='通知', user=current_user, messageList=messageList)
    else:
        return redirect(url_for('login'))


@app.route('/domain')
def domain():
    if current_user.is_authenticated:
        domainList = Domain.query.order_by('id').all()

        return render_template('domain.html', title='占領戰', user=current_user, domainList=domainList)
    else:
        return redirect(url_for('login'))


# 已經移除，此介面停用
@app.route('/thanks')
def thanks():
    if current_user.is_authenticated:
        return render_template('thanks.html', title='銘謝', user=current_user)
    else:
        return redirect(url_for('login'))

# ====== 管理員系統 ====== #
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    teamNameList = [ '',
                     '阿瑞斯小隊',
                     '雅典娜小隊',
                     '阿波羅小隊',
                     '波賽頓小隊', ]

    if current_user.is_authenticated:
        tradeform = TradeForm()
        clueform = ClueForm()
        domainform = DomainForm()
        cardform = CardForm()
        infoform = InfoForm()

        userList = User.query.order_by('id').all()
        teamList = Team.query.order_by('id').all()
        eventList = Event.query.order_by(Event.time.desc()).all()
        banCardList = BanCard.query.order_by('id').all()
        domainList = Domain.query.order_by('id').all()
        messageList = Notice.query.order_by(Notice.time.desc()).all()

        if tradeform.validate_on_submit():
            newEvent = Event(coins=tradeform.coins.data,
                             sender_id=current_user.id, team_id=tradeform.team_id.data)
            targetTeam = Team.query.filter_by(
                id=tradeform.team_id.data).first()
            targetTeam.team_coins = targetTeam.team_coins + tradeform.coins.data
            db.session.add(newEvent)
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if cardform.validate_on_submit():
            targetTeam = Team.query.filter_by(
                id=cardform.team_receive.data).first()

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
                newMessage = Notice(time=datetime.utcnow(),
                    text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                    teamNameList[cardform.team_receive.data] + '使用了「線索增益」')
                db.session.add(newMessage)
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
                newMessage = Notice(time=datetime.utcnow(),
                    text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                    teamNameList[cardform.team_receive.data] + '使用了「線索減益」')
                db.session.add(newMessage)
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 3:
                targetTeam.clueCardStatus = 0
                targetTeam.clueCardContent = None
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 4:  # TODO: 更新發送小隊資訊
                targetTeam.selfBanCardStatus = 1
                targetTeam.selfBanCardTime = datetime.utcnow() + timedelta(minutes=15)
                newMessage = Notice(time=datetime.utcnow(),
                    text=teamNameList[cardform.team_receive.data] + ' 對自己使用了「我BAN我自己」')
                db.session.add(newMessage)
                db.session.add(targetTeam)
                db.session.commit()

            if cardform.card.data == 5:
                StageBanTeam = BanCard.query.filter_by(
                    id=cardform.team_receive.data).first()
                if cardform.stageSelect1.data == 1:
                    StageBanTeam.stage1_status = 1
                    StageBanTeam.stage1_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage1_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡A」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 2:
                    StageBanTeam.stage2_status = 1
                    StageBanTeam.stage2_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage2_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡B」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 3:
                    StageBanTeam.stage3_status = 1
                    StageBanTeam.stage3_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage3_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡C」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 4:
                    StageBanTeam.stage4_status = 1
                    StageBanTeam.stage4_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage4_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡D」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 5:
                    StageBanTeam.stage5_status = 1
                    StageBanTeam.stage5_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage5_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡E」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 6:
                    StageBanTeam.stage6_status = 1
                    StageBanTeam.stage6_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage6_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡F」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 7:
                    StageBanTeam.stage7_status = 1
                    StageBanTeam.stage7_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage7_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡G」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()
                if cardform.stageSelect1.data == 8:
                    StageBanTeam.stage8_status = 1
                    StageBanTeam.stage8_time = datetime.utcnow() + timedelta(minutes=15)
                    StageBanTeam.stage8_content = '停用'
                    newMessage = Notice(time=datetime.utcnow(),
                        text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                        teamNameList[cardform.team_receive.data] + '使用了「禁止闖關 - 關卡H」')
                    db.session.add(newMessage)
                    db.session.add(StageBanTeam)
                    db.session.commit()

            if cardform.card.data == 6:
                targetTeam.isolateCardStatus = 1
                targetTeam.isolateCardTime = datetime.utcnow() + timedelta(minutes=5)
                newMessage = Notice(time=datetime.utcnow(),
                    text=teamNameList[cardform.team_sent.data] + ' 對 ' + 
                    teamNameList[cardform.team_receive.data] + '使用了「不是減益是檢疫」')
                db.session.add(newMessage)
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

        if domainform.validate_on_submit():
            targetDomain = Domain.query.filter_by(
                id=domainform.stageSelect.data).first()
            targetDomain.time = datetime.utcnow()
            if domainform.team_id.data == 5:
                targetDomain.team_id = None
            else:
                targetDomain.team_id = domainform.team_id.data
            db.session.add(targetDomain)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if infoform.validate_on_submit():  # TODO: 訊息系統資料庫製作
            # print(infoform.text.data)
            newMessage = Notice(time=datetime.utcnow(),
                                text=infoform.text.data)
            db.session.add(newMessage)
            db.session.commit()
            return redirect(url_for('dashboard'))

        return render_template('dashboard.html', tradeform=tradeform, infoform=infoform,
                               clueform=clueform, domainform=domainform, cardform=cardform,
                               teamList=teamList, domainList=domainList, eventList=eventList,
                               userList=userList, banCardList=banCardList, messageList=messageList)
    else:
        return redirect(url_for('login'))


# QR code 功能已經移除，此介面停用
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


@app.route('/staff_team/<team_id>')
def staff_team(team_id):
    if current_user.is_authenticated:

        userList = User.query.order_by('id').all()
        teamList = Team.query.order_by('id').all()
        banCardList = BanCard.query.order_by('id').all()
        eventList = Event.query.filter_by(
            team_id=team_id).order_by(Event.time.desc()).all()

        return render_template('staff_team.html', title='隊伍資訊', user=current_user, userList=userList,
                               teamList=teamList, banCardList=banCardList, team_code=int(team_id)-1, eventList=eventList)
    else:
        return redirect(url_for('login'))


@app.route('/staff_trade', methods=['GET', 'POST'])
def staff_trade():
    if current_user.is_authenticated and current_user.team_id == 5:
        tradeform = TradeForm()

        if tradeform.validate_on_submit():
            newEvent = Event(coins=tradeform.coins.data,
                             sender_id=current_user.id, team_id=tradeform.team_id.data)
            targetTeam = Team.query.filter_by(
                id=tradeform.team_id.data).first()
            targetTeam.team_coins = targetTeam.team_coins + tradeform.coins.data
            db.session.add(newEvent)
            db.session.add(targetTeam)
            db.session.commit()
            return redirect(url_for('staff_team', team_id=tradeform.team_id.data))
        return render_template('staff_trade.html', title='隊伍資訊', user=current_user, tradeform=tradeform)
    elif current_user.team_id == 5:
        return redirect(url_for('staff_team', team_id=1))
    else:
        return redirect(url_for('team'))


@app.route('/staff_set_domain', methods=['GET', 'POST'])
def staff_set_domain():
    if current_user.is_authenticated and current_user.team_id == 5:

        domainform = DomainForm()

        if domainform.validate_on_submit():
            targetDomain = Domain.query.filter_by(
                id=domainform.stageSelect.data).first()
            targetDomain.time = datetime.utcnow()
            if domainform.team_id.data == 5:
                targetDomain.team_id = None
            else:
                targetDomain.team_id = domainform.team_id.data
            db.session.add(targetDomain)
            db.session.commit()
            return redirect(url_for('domain'))

        return render_template('staff_set_domain.html', title='關卡佔領', user=current_user, domainform=domainform)
    elif current_user.team_id == 5:
        return redirect(url_for('staff_team', team_id=1))
    else:
        return redirect(url_for('team'))


# ====== 帳號系統 ====== #
# 在此login與reset都是使用同一個模板 account.html
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


# ====== 資料庫操作 ====== #
# TODO: 檢查是否是管理員
@app.route('/db/create')
def db_create_route():
    db_create()
    return '資料庫建立完成'

@app.route('/db/drop')
def db_drop_route():
    logout_user()
    db_drop()
    return '資料庫刪除完成'


@app.route('/db/init')
def db_init_route():
    db_init()
    return '資料庫資料初始化完成'
