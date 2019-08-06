from config       import Config
from app          import login_manager, redis_store
from flask_login  import UserMixin
from pymssql      import connect

class User(UserMixin):    
    def __init__(self, user_id, username, password_hash, operating_mode, role):
        self.id             = user_id        
        self.username       = username
        # self.email          = email
        self.password_hash  = password_hash
        self.operating_mode = operating_mode
        self.role           = role


def get_connection(db):
    
    if db == 'elc_work':
        host     = Config.ELC_HOST
        database = 'YELETS'
    elif db == 'elc_test':
        host     = Config.ELC_HOST
        database = 'Otchet'
    elif db == 'bor_work':
        host     = Config.BOR_HOST
        database = 'borino'
    elif db == 'bor_test':
        host     = Config.BOR_HOST
        database = 'borino_test'
    elif db == 'vol_work':
        host     = Config.VOL_HOST
        database = 'volovo'
    elif db == 'vol_test':
        host     = Config.VOL_HOST
        database = 'vol_test'        
    elif db == 'grz_work':        
        host     = Config.GRZ_HOST
        database = 'gryazi'
    elif db == 'grz_test':        
        host     = Config.GRZ_HOST
        database = 'OTCHET'
    elif db == 'dan_work':
        host     = Config.DAN_HOST
        database = 'dankov'
    elif db == 'dan_test':
        host     = Config.DAN_HOST
        database = 'otchet'
    elif db == 'dbk_work':
        host     = Config.DBK_HOST
        database = 'Dobrinka'
    elif db == 'dbk_test':        
        host     = Config.DBK_HOST
        database = 'test'
    elif db == 'dbr_work':
        host     = Config.DBR_HOST
        database = 'dobroe'
    elif db == 'dbr_test':        
        host     = Config.DBR_HOST
        database = 'dobroe_test'
    elif db == 'dlk_work':
        host     = Config.DLK_HOST
        database = 'dolgorukovo'
    elif db == 'dlk_test':        
        host     = Config.DLK_HOST
        database = 'otchet'
    elif db == 'zdn_work':
        host     = Config.ZDN_HOST
        database = 'Zadonsk'
    elif db == 'zdn_test':        
        host     = Config.ZDN_HOST
        database = 'base1c'
    elif db == 'izm_work':
        host     = Config.IZM_HOST
        database = 'izmalkovo'
    elif db == 'izm_test':        
        host     = Config.IZM_HOST
        database = 'otchet'
    elif db == 'krs_work':
        host     = Config.KRS_HOST
        database = 'krasnoe'
    elif db == 'krs_test':        
        host     = Config.KRS_HOST
        database = 'otchet'
    elif db == 'lbd_work':
        host     = Config.LBD_HOST
        database = 'lebedan'
    elif db == 'lbd_test':        
        host     = Config.LBD_HOST
        database = 'otchet'
    elif db == 'lvt_work':
        host     = Config.LVT_HOST
        database = 'lt'
    elif db == 'lvt_test':        
        host     = Config.LVT_HOST
        database = 'otchet'    
    elif db == 'stn_work':
        host     = Config.STN_HOST
        database = 'stanovoe'
    elif db == 'stn_test':        
        host     = Config.STN_HOST
        database = 'otchet'    
    elif db == 'trb_work':
        host     = Config.TRB_HOST
        database = 'terbun'
    elif db == 'trb_test':        
        host     = Config.TRB_HOST
        database = 'test'
    elif db == 'usm_work':
        host     = Config.USM_HOST
        database = 'usman'
    elif db == 'usm_test':        
        host     = Config.USM_HOST
        database = 'test'
    elif db == 'hlv_work':
        host     = Config.HLV_HOST
        database = 'hlevnoe'
    elif db == 'hlv_test':        
        host     = Config.HLV_HOST
        database = 'OTCHET'
    elif db == 'cha_work':
        host     = Config.CHA_HOST
        database = 'chapligin'
    elif db == 'cha_test':        
        host     = Config.CHA_HOST
        database = 'chap_test'
    
    conn = connect(
            host    =host,
            user    =Config.MSSQL_USER,
            password=Config.MSSQL_PASSWORD,
            database=database,
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
        #email           = user_data['email']
        password_hash   = user_data['password_hash']
        operating_mode  = user_data['operating_mode']
        role            = user_data['role']        
        user = User(user_id=id,
                    username=username,
                    # email=email, 
                    password_hash=password_hash,
                    operating_mode=operating_mode,
                    role=role)
        return user    