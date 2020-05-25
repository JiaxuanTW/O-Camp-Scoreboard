# 數據庫模組
import time
from datetime import datetime
from flask_login import UserMixin
from main import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False, default='NULL')
    account = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.account}', '{self.nickname}', '{self.password}')"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_coins = db.Column(db.Integer, nullable=False, default=0)
    members = db.relationship('User', backref='member', lazy=True)
    clues = db.Column(db.Integer, nullable=False, default=0)
    clueCardStatus = db.Column(db.Integer, nullable=False, default=0)
    clueCardContent = db.Column(db.String(10))  # 表示從哪個小隊發送的
    isolateCardStatus = db.Column(db.Integer, nullable=False, default=0)
    isolateCardTime = db.Column(db.DateTime)
    #isolateCardContent = db.Column(db.String(10))  # TODO:表示從哪個小隊發送的
    selfBanCardStatus = db.Column(db.Integer, nullable=False, default=0)
    selfBanCardTime = db.Column(db.DateTime)
    #selfBanCardContent = db.Column(db.String(10))  # 表示從哪個小隊發送的

    # id = 1 : 阿瑞斯(R)
    # id = 2 : 雅典娜(G)
    # id = 3 : 阿波羅(Y)
    # id = 4 : 波賽頓(B)
    # id = 5 : 工作人員

    def __repr__(self):
        return f"Team(代號'{self.id}',目前金幣'{self.team_coins}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, nullable=False)


class BanCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage1_status = db.Column(db.Integer, nullable=False, default=0)
    stage1_time = db.Column(db.DateTime)
    stage1_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage2_status = db.Column(db.Integer, nullable=False, default=0)
    stage2_time = db.Column(db.DateTime)
    stage2_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage3_status = db.Column(db.Integer, nullable=False, default=0)
    stage3_time = db.Column(db.DateTime)
    stage3_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage4_status = db.Column(db.Integer, nullable=False, default=0)
    stage4_time = db.Column(db.DateTime)
    stage4_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage5_status = db.Column(db.Integer, nullable=False, default=0)
    stage5_time = db.Column(db.DateTime)
    stage5_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage6_status = db.Column(db.Integer, nullable=False, default=0)
    stage6_time = db.Column(db.DateTime)
    stage6_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage7_status = db.Column(db.Integer, nullable=False, default=0)
    stage7_time = db.Column(db.DateTime)
    stage7_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    stage8_status = db.Column(db.Integer, nullable=False, default=0)
    stage8_time = db.Column(db.DateTime)
    stage8_content = db.Column(db.String(10))  # 表示從哪個小隊發送的線索卡

    # id = 1 : 阿瑞斯(R)
    # id = 2 : 雅典娜(G)
    # id = 3 : 阿波羅(Y)
    # id = 4 : 波賽頓(B)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, default=0)

    # id = 1 : 關卡A
    # id = 2 : 關卡B
    # id = 3 : 關卡C
    # id = 4 : 關卡D
    # id = 5 : 關卡E
    # id = 6 : 關卡F
    # id = 7 : 關卡G
    # id = 8 : 關卡H


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(20), nullable=False, default='NULL')
