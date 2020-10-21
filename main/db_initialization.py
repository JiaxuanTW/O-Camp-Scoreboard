from main import db
from main.models import BanCard, Domain, Event, Notice, Team, User


user_list = {
    'T1085501': 1,  # 隊員端測試帳號
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
}

team_account_list = [
    'Aresssss',
    'Athenaaa',
    'Apollooo',
    'Poseidon',
]

team_password_list = [
    '02teamARESR',
    'TEAM04athenaG',
    'APPOLLOteam01Y',
    'poseidon03teamB',
]

team_nickname_list = [
    '阿瑞斯小隊員',
    '雅典娜小隊員',
    '阿波羅小隊員',
    '波賽頓小隊員',
]


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

    # 小隊帳號
    for i in range(4):
        client = User(
            nickname=team_nickname_list[i], account=team_account_list[i],
            password=team_password_list[i], team_id=i+1)
        db.session.add(client)
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
