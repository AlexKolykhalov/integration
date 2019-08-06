import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):    
    #SECRET_KEY                       = 'erfqerf-895122-QWswsdx-xc34deawedf'#os.environ.get('SECRET_KEY')    
    #REDIS_URL                        = 'redis://'#os.environ.get('REDIS_URL')    
    # GRZ_WORK                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.105.1%3BDATABASE%3Dgryazi%3BTrusted_Connection%3Dyes%3B' #os.environ.get('GRZ_WORK')
    # GRZ_TEST                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.105.1%3BDATABASE%3DOTCHET%3BTrusted_Connection%3Dyes%3B' #os.environ.get('GRZ_TEST')
    # DBK_WORK                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.107.1%3BDATABASE%3DDobrinka%3BTrusted_Connection%3Dyes%3B' #os.environ.get('DBK_WORK')
    # DBK_TEST                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.107.1%3BDATABASE%3DTest%3BTrusted_Connection%3Dyes%3B' #os.environ.get('DBK_TEST')
    # LVT_WORK                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.114.1%3BDATABASE%3Dlt%3BTrusted_Connection%3Dyes%3B' #os.environ.get('LVT_WORK')
    # LVT_TEST                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.114.1%3BDATABASE%3DOTCHET%3BTrusted_Connection%3Dyes%3B' #os.environ.get('LVT_TEST')
    # USM_WORK                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.117.1%3BDATABASE%3Dusman%3BTrusted_Connection%3Dyes%3B ' #os.environ.get('USM_WORK')
    # USM_TEST                         = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server%7D%3BSERVER%3D192.168.117.1%3BDATABASE%3Dtest%3BTrusted_Connection%3Dyes%3B' #os.environ.get('USM_TEST')    
    #SQLALCHEMY_TRACK_MODIFICATIONS   = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    #UPLOADS_DEFAULT_DEST             = os.environ.get('UPLOADS_DEFAULT_DEST')    
    #UPLOADED_IMAGES_DEST             = os.environ.get('UPLOADED_IMAGES_DEST')

    # WTF-forms
    SECRET_KEY = 'erfqerf-895122-QWswsdx-xc34deawedf'#os.environ.get('SECRET_KEY')

    # redis    
    REDIS_URL = 'redis://'

    # mssql
    ELC_HOST        = '192.168.102.1'
    BOR_HOST        = '192.168.103.1'
    VOL_HOST        = '192.168.104.1'
    GRZ_HOST        = '192.168.105.1'
    DAN_HOST        = '192.168.106.1'
    DBK_HOST        = '192.168.107.1'
    DBR_HOST        = '192.168.108.1'
    DLK_HOST        = '192.168.109.1'
    ZDN_HOST        = '192.168.110.1'
    IZM_HOST        = '192.168.111.1'
    KRS_HOST        = '192.168.112.1'
    LBD_HOST        = '192.168.113.1'
    LVT_HOST        = '192.168.114.1'
    STN_HOST        = '192.168.115.1'
    TRB_HOST        = '192.168.116.1'
    USM_HOST        = '192.168.117.1'
    HLV_HOST        = '192.168.118.1'
    CHA_HOST        = '192.168.119.1'
    MSSQL_USER      = 'ABONENT\A.Kolihalov'
    MSSQL_PASSWORD  = 'edefis15'    
    
    # mail
    MAIL_SERVER     = 'smtp.rambler.ru'     #os.environ.get('MAIL_SERVER')
    MAIL_PORT       = 465                   #int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_SSL    = True                  #os.environ.get('MAIL_USE_SSL') is not None    
    MAIL_USE_TLS    = False                 #os.environ.get('MAIL_USE_TLS') is not None    
    MAIL_USERNAME   = 'ak8647'              #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD   = 'e2_e4_New_Champion'  #os.environ.get('MAIL_PASSWORD')    