from main import db
from main.models import BanCard, Domain, Event, Notice, Team, User


user_list = {   'T1085501': 1,  # 隊員端測試帳號
                'T1085502': 2,
                'T1085503': 3,
                'T1085504': 4,
                'T1085505': 5,  # 工作人員端測試帳號

                'A1085505': 5,  # 機動
                'A1085507': 5,  # 主控台人員
                'A1085511': 5,

                'A1085534': 5,  # 小隊工作人員
                'A1085541': 5,
                'A1085521': 5,
                'A1085516': 5,
                'A1085518': 5,
                'A1085538': 5,
                'A1085510': 5,
                'A1085524': 5,
                'A1085512': 5,
                'A1085503': 5,
                'A1085513': 5,
                'A1085536': 5,
                
                'A1085527': 5,  # 占領戰關主
                'A1085539': 5,
                'A1085537': 5,
                'A1085520': 5,
                'A1085523': 5,
                'A1085528': 5,
                'A1085529': 5,

                'A1095524': 1,
                'A1095509': 1,
                'A1095502': 1,
                'A1095530': 1,
                'A1095557': 1,
                'A1095550': 1,
                'A1095517': 1,

                'A1095504': 2,
                'A1095516': 2,
                'A1095549': 2,
                'A1095518': 2,
                'A1095552': 2,
                'A1095514': 2,
                'A1095529': 2,

                'A1095532': 3,
                'A1095501': 3,
                'A1095553': 3,
                'A1095546': 3,
                'A1095511': 3,
                'A1095533': 3,
                'A1095510': 3,

                'A1095556': 4,
                'A1095513': 4,
                'A1095506': 4,
                'A1095551': 4,
                'A1095505': 4,
                                }


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
    for i in range(4):
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
