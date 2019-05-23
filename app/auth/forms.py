from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app                import redis_store


class LoginForm(FlaskForm):
    username    = StringField('Пользователь', validators=[DataRequired()])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    # remember_me = BooleanField(_l('Remember Me'))
    submit      = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username    = StringField('Пользователь', validators=[DataRequired()])
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    password2   = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Сохранить')

    def validate_username(self, username):
        result = redis_store.exists(username.data)        
        if result == 1:
            raise ValidationError('Выберите другое имя пользователя!')

    def validate_email(self, email):        
        result = redis_store.sismember('emails', email.data)        
        if result == 1:
            raise ValidationError('Выберите другой email!')