from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app                import redis_store


class LoginForm(FlaskForm):
    username    = SelectField('Пользователь', choices=[('-', '')])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    submit      = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username    = StringField('Пользователь', validators=[DataRequired()])
    #email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    password2   = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Сохранить')

    # def validate_username(self, username):
    #     result = redis_store.exists(username.data)
    #     if result == 1:
    #         raise ValidationError('Выберите другое имя пользователя!')

    # def validate_email(self, email):
    #     result = redis_store.sismember('emails', email.data)
    #     if result == 1:
    #         raise ValidationError('Выберите другой email!')
            
class ProfileForm(FlaskForm):
    username    = StringField('Пользователь', validators=[DataRequired()])
    role        = SelectField('Роль', choices=[('admin', 'admin'), ('user', 'user')])
    submit      = SubmitField('Сохранить')