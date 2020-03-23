from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[DataRequired(), Length(min=8, max=8)], render_kw={"placeholder": "帳號"})
    password = PasswordField('密碼', validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "密碼"})
    remember = BooleanField('保持登入')
    submit = SubmitField('登入')

class ResetForm(FlaskForm):
    account = StringField('帳號', validators=[DataRequired(), Length(min=8, max=8)], render_kw={"placeholder": "原密碼"})
    password = PasswordField('重設密碼', validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "新密碼"})
    submit = SubmitField('重設')

