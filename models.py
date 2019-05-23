from sqlalchemy                 import Table, create_engine, MetaData, BINARY, Column, Unicode, Index
from sqlalchemy.dialects.mssql  import DATETIME2
from sqlalchemy.orm             import sessionmaker, scoped_session
from sqlalchemy.ext.automap     import automap_base
from config                     import Config
from app                        import login_manager, redis_store
from flask_login                import UserMixin


class User(UserMixin):    
    def __init__(self, user_id, email, password_hash, username='username', operating_mode='test'):
        self.id             = user_id        
        self.username       = username
        self.email          = email
        self.password_hash  = password_hash
        self.operating_mode = operating_mode

def get_engine(db):    
    if db == 'grz_work':        
        engine = create_engine(Config.GRZ_WORK, convert_unicode=True)
    elif db == 'grz_test':
        engine = create_engine(Config.GRZ_TEST, convert_unicode=True)
    elif db == 'dbk_work':
        engine = create_engine(Config.DBK_WORK, convert_unicode=True)
    elif db == 'dbk_test':
        engine = create_engine(Config.DBK_TEST, convert_unicode=True)
    elif db == 'lvt_work':
        engine = create_engine(Config.LVT_WORK, convert_unicode=True)
    elif db == 'lvt_test':
        engine = create_engine(Config.LVT_TEST, convert_unicode=True)
    elif db == 'usm_work':
        engine = create_engine(Config.USM_WORK, convert_unicode=True)
    elif db == 'usm_test':
        engine = create_engine(Config.USM_TEST, convert_unicode=True)
    return engine

def get_db_class(name, engine):    
    metadata = MetaData(bind=engine)
    metadata.reflect(engine, only=[name])

    if name == '_InfoRg4272': # режим исправления ошибок (РС НастройкиПользователей)
        Table('_InfoRg4272', metadata,
                Column('_Fld4273_TYPE',  BINARY(1),  nullable=False, primary_key=True),                
                Column('_Fld4273_RRRef', BINARY(16), nullable=False),                   # Пользователь
                Column('_Fld4274RRef',   BINARY(16), nullable=False),                   # Настройка              
                Column('_Fld4275_L',     BINARY(1),  nullable=False),                   # Значение L
                Index('_InfoRg4272_1', '_Fld4273_TYPE', '_Fld4273_RRRef', '_Fld4274RRef', unique=True),
                extend_existing=True
            )
    elif name == '_InfoRg2721': # дата запрета редактирования (РС ДатыЗапретаРедактирования)
        Table('_InfoRg2721', metadata,
                Column('_Fld2722RRef', BINARY(16), nullable=False, unique=True, primary_key=True),
                Column('_Fld2723', DATETIME2, nullable=False),
                Column('_Fld2724', BINARY(1), nullable=False),
                Column('_Fld2725', DATETIME2, nullable=False),
                Column('_Fld2726', BINARY(1), nullable=False),
                extend_existing=True
            )
    elif name == '_ScheduledJobs3995': # регламетные задания
        Table('_ScheduledJobs3995', metadata,
                Column('_ID',           BINARY(16),     nullable=False, primary_key=True),
                Column('_Description',  Unicode(128),   nullable=False),
                Column('_JobKey',       Unicode(128),   nullable=False),
                Column('_Use',          BINARY(1),      nullable=False),
                extend_existing=True
            )

    Base = automap_base(metadata=metadata)
    Base.prepare()        
    map_class = Base.classes._data[name]
    return map_class

session = scoped_session(sessionmaker())    

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