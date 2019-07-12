from config       import Config
from app          import login_manager, redis_store
from flask_login  import UserMixin
from pymssql      import connect

class User(UserMixin):    
    def __init__(self, user_id, email, password_hash, username='username', operating_mode='test'):
        self.id             = user_id        
        self.username       = username
        self.email          = email
        self.password_hash  = password_hash
        self.operating_mode = operating_mode

def get_connection(db):    
    if db == 'grz_work':        
        engine = create_engine(Config.GRZ_WORK, convert_unicode=True)            
    elif db == 'grz_test':        
        conn = connect(
            host    =Config.GRZ_HOST,
            user    =Config.MSSQL_USER,
            password=Config.MSSQL_PASSWORD,
            database='OTCHET',
            as_dict =True
        )
    elif db == 'dbk_work':
        engine = create_engine(Config.DBK_WORK, convert_unicode=True)
    elif db == 'dbk_test':        
        conn = connect(
            host    =Config.DBK_HOST,
            user    =Config.MSSQL_USER,
            password=Config.MSSQL_PASSWORD,
            database='test',
            as_dict =True
        )
    elif db == 'lvt_work':
        engine = create_engine(Config.LVT_WORK, convert_unicode=True)
    elif db == 'lvt_test':        
        conn = connect(
            host    =Config.LVT_HOST,
            user    =Config.MSSQL_USER,
            password=Config.MSSQL_PASSWORD,
            database='otchet',
            as_dict =True
        )
    elif db == 'usm_work':
        engine = create_engine(Config.USM_WORK, convert_unicode=True)
    elif db == 'usm_test':        
        conn = connect(
            host    =Config.USM_HOST,
            user    =Config.MSSQL_USER,
            password=Config.MSSQL_PASSWORD,
            database='test',
            as_dict =True
        )
    return conn

# initialize 
@login_manager.user_loader
def load_user(id):
    user_data = redis_store.hgetall(id)    
    if user_data == {}:
        return None
    else:    
        username        = user_data['username']
        email           = user_data['email']
        password_hash   = user_data['password_hash']
        operating_mode  = user_data['operating_mode'] 
        user = User(user_id=id, username=username, email=email, password_hash=password_hash, operating_mode=operating_mode)
        return user    