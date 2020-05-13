# 數據庫模組
from main import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False, default='NULL')
    account = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    coins = db.Column(db.Integer, nullable=False, default=0)
    events = db.relationship('Event', backref='events', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.account}', '{self.nickname}', '{self.password}')"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_coins = db.Column(db.Integer, nullable=False, default=0)
    members = db.relationship('User', backref='member', lazy=True)
    events = db.relationship('Event', backref='team_events', lazy=True)
    cards = db.relationship('Card', backref='team_cards', lazy=True)
    domain = db.relationship('Domain', backref='team_domain', lazy=True)
    
    # team_id 1 : 阿波羅(Y)
    # team_id 2 : 阿瑞斯(R)
    # team_id 3 : 波賽頓(B)
    # team_id 4 : 雅典娜(G)
    # team_id 5 : 工作人員

    def __repr__(self):
        return f"Team('{self.members}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_event_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.time}', '{self.coins}')"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer, nullable=False, default=0)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=0)
    send_team_id = db.Column(db.Integer, nullable=False, default=0)
    recieve_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    team_domain_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(20), nullable=False, default='NULL')