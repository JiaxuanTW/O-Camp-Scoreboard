#這裡是數據庫模組
from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20), unique=True, nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.account}', '{self.nickname}', '{self.password}')"

    