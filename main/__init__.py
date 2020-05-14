# 檔案初始化模組
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '85ad229cd598f387664cd5f75dff022c'

# 資料庫組態參數
Env = 'PUB'
if Env == 'DEV':
    p_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(p_dir, 'database.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mklbufftqaeykj:1fd7bc07dd95cf44b356b1256426e75e649b22b6378f934f4ef7e26d1c30640b@ec2-54-165-36-134.compute-1.amazonaws.com:5432/dc028ot707bnjf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 登入系統
login_manager = LoginManager(app)

from main import routes