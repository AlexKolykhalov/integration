from flask import Blueprint
from models import session

bp = Blueprint('main', __name__)

# важно 
# очистка запросов
@bp.teardown_request
def cleanup(resp_or_exc):
    session.remove()

from app.main import forms, routes