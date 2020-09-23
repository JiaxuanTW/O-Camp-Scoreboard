from main import db
from main.models import BanCard, Domain, Event, Notice, Team, User


user_list = {'A1085512': 5}


def db_init():
    # 建立小組
    for i in range(5):
        team = Team()
        db.session.add(team)
        db.session.commit()

    # 建立使用者
    for key, value in user_list.items():
        user = User(nickname=key, account=key, password=key, team_id=value)
        db.session.add(user)
        db.session.commit()

    # 建立 BanCard 資料
    ban_card = BanCard()
    db.session.add(ban_card)
    db.session.commit()

    # 建立 Domain 資料
    for i in range(8):
        domain = Domain()
        db.session.add(domain)
        db.session.commit()


def db_create():
    db.create_all()


def db_drop():
    db.drop_all()
