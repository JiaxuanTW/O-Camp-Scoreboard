#數據庫模組
from main import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20), unique=True, nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recieve_event = db.relationship('Event', backref='reciever', lazy=True)

    def __repr__(self):
        return f"User('{self.account}', '{self.nickname}', '{self.password}')"

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20), unique=True, nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    sent_event = db.relationship('Event', backref='sender', lazy=True)

    def __repr__(self):
        return f"Staff('{self.account}', '{self.nickname}', '{self.password}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.time}', '{self.points}')"