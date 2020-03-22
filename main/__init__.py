#檔案初始化模組
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#組態參數
p_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(p_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from main import routes