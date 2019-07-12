from flask import Flask, render_template
from config import Config
from flask_bootstrap import Bootstrap
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail

# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_uploads import UploadSet, IMAGES, configure_uploads

import dash
import dash_core_components as dcc
import dash_html_components as html



bootstrap                                         = Bootstrap()
redis_store                                       = FlaskRedis()
socketio                                          = SocketIO()
mail                                              = Mail()
# db                                              = SQLAlchemy()
# migrate                                         = Migrate()
# images                                          = UploadSet('images', IMAGES)
login_manager                                     = LoginManager()
login_manager.login_view                          = 'auth.login'
login_manager.login_message                       = 'Пройдите регистрацию'
# login_manager.login_message_category            = 'alert-info'
# login_manager.refresh_view                      = 'auth.refresh'
# login_manager.needs_refresh_message             = 'Session is closed, please reauthenticate to access this page'
# login_manager.needs_refresh_message_category    = 'alert-info'

def page_not_found(e):
    return render_template('errors/404.html'), 404

def server_error(e):
    return render_template('errors/500.html', error=e), 500


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)        

    # initialization    
    bootstrap.init_app(app)    
    login_manager.init_app(app)
    redis_store.init_app(app, decode_responses=True)
    socketio.init_app(app)
    mail.init_app(app)
    # db.init_app(app)
    # migrate.init_app(app, db)
        
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # from app.manage import bp as manage_bp
    # app.register_blueprint(manage_bp, url_prefix='/manage')

    # from app.select import bp as select_bp
    # app.register_blueprint(select_bp, url_prefix='/select')
    
    #app1 = dash.Dash(__name__, server=app)
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app
    

# from app import models