from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField,
                    StringField, SubmitField)
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[DataRequired(), Length(
        min=8, max=8)], render_kw={"placeholder": "帳號"})
    password = PasswordField('密碼', validators=[DataRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "密碼"})
    remember = BooleanField('保持登入')
    submit = SubmitField('登入')


class ResetForm(FlaskForm):
    nickname = StringField('暱稱', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "暱稱"})
    account = StringField('帳號', validators=[DataRequired(), Length(
        min=8, max=8)], render_kw={"placeholder": "帳號"})
    password = PasswordField('重設密碼', validators=[DataRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "新密碼"})
    submit = SubmitField('重設')


class TradeForm(FlaskForm):
    team_id = SelectField('選取小隊', choices=[
        (0, '請選擇'), 
        (1, '阿瑞斯小隊'), 
        (2, '雅典娜小隊'), 
        (3, '阿波羅小隊'), 
        (4, '波賽頓小隊')
    ],validators=[InputRequired(), DataRequired()], coerce=int)
    coins = IntegerField('交易款項', validators=[InputRequired(), DataRequired()], render_kw={
                        "placeholder": "請輸入金幣數量", "inputmode": "numeric"})
    submit = SubmitField('送出')


class ClueForm(FlaskForm):
    team_id = SelectField('選取小隊', choices=[
        (0, '請選擇'), 
        (1, '阿瑞斯小隊'), 
        (2, '雅典娜小隊'), 
        (3, '阿波羅小隊'), 
        (4, '波賽頓小隊')
    ],validators=[InputRequired(), DataRequired()], coerce=int)
    clues = IntegerField('變更數量', validators=[InputRequired(), DataRequired()], render_kw={
                        "placeholder": "請輸入變更數量", "inputmode": "numeric"})
    submit = SubmitField('送出')


class DomainForm(FlaskForm):
    team_id = SelectField('選取小隊', choices=[
        (0, '請選擇'), 
        (1, '阿瑞斯小隊'), 
        (2, '雅典娜小隊'), 
        (3, '阿波羅小隊'), 
        (4, '波賽頓小隊')
    ],validators=[InputRequired(), DataRequired()], coerce=int)
    stageSelect = SelectField('選取關卡', choices=[
        (0, '請選擇'),
        (1, '關卡A'),
        (2, '關卡B'),
        (3, '關卡C'),
        (4, '關卡D'),
        (5, '關卡E'),
        (6, '關卡F'),
        (7, '關卡G'),
        (8, '關卡H'),
    ], coerce=int)
    submit = SubmitField('送出')


class InfoForm(FlaskForm):
    text = StringField('訊息', validators=[DataRequired()], render_kw={
                        "placeholder": "輸入文字訊息"})
    submit = SubmitField('送出')


class CardForm(FlaskForm):
    card = SelectField('選取功能卡', choices=[
        (0, '請選取'),
        (1, '線索增益'),
        (2, '線索減益'),
        (3, '結束線索效益'),
        (4, '我BAN我自己'),
        (5, '禁止闖關'),
        (6, '不是減益是檢疫'),
        (7, '結束檢疫')
    ], validators=[DataRequired(), InputRequired()], coerce=int)
    team_sent = SelectField('選取使用卡片小隊', choices=[
        (0, '請選擇'), 
        (1, '阿瑞斯小隊'), 
        (2, '雅典娜小隊'), 
        (3, '阿波羅小隊'), 
        (4, '波賽頓小隊')
    ], coerce=int)
    team_receive = SelectField('選取卡片作用小隊', choices=[
        (0, '請選擇'), 
        (1, '阿瑞斯小隊'), 
        (2, '雅典娜小隊'), 
        (3, '阿波羅小隊'), 
        (4, '波賽頓小隊')
    ],validators=[InputRequired(), DataRequired()], coerce=int)
    stageSelect1 = SelectField('選取關卡', choices=[
        (0, '請選擇'),
        (1, '關卡A'),
        (2, '關卡B'),
        (3, '關卡C'),
        (4, '關卡D'),
        (5, '關卡E'),
        (6, '關卡F'),
        (7, '關卡G'),
        (8, '關卡H'),
    ], coerce=int)
    submitCardForm = SubmitField('送出')
