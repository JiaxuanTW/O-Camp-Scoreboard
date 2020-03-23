#數據庫模組
from main import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False, default='nickname')
    account = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    recieve_event = db.relationship('Event', backref='reciever', lazy=True)

    def __repr__(self):
        return f"User('{self.account}', '{self.nickname}', '{self.password}')"

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False, default='staff')
    account = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    sent_event = db.relationship('Event', backref='sender', lazy=True) #關主送出事件

    def __repr__(self):
        return f"Staff('{self.account}', '{self.nickname}', '{self.password}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    team_event_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.time}', '{self.points}')"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    members = db.relationship('User', backref='member', lazy=True)
    events = db.relationship('Event', backref='member', lazy=True)

    def __repr__(self):
        return f"Team('{self.members}')"
               