from app import create_app, redis_store
from models import get_engine, get_db_class, session
from flask_socketio import SocketIO, emit
from flask_login import current_user
from datetime import datetime, timedelta
import subprocess

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

app = create_app()
socketio = SocketIO(app)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('response', {'data': 'Connected'}, broadcast=True)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    emit('response', {'data': 'Disconnected'}, broadcast=True)    

@socketio.on('change_period', namespace='/test')
def change_period(data):
    # изменение даты запрета редактирования    
    time = datetime.strptime('01.'+data['TIME'].replace('.2', '.4'), '%d.%m.%Y')
    if data['CHECKED'] == True:
        checked = b'\x01'
        PO      = '(v)'
    else:
        checked = b'\x00'
        PO      = '( )'
    connect_bases = []
    for base in data['BASES']:        
        host = redis_store.hmget(base[:3], ['host'])[0]
        try:
            subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            basename = redis_store.hmget(base[:3], ['name'])[0]
            emit('server_response', {'info': 'button', 'procedure': 'error', 'data': basename})            
            continue            
        connect_bases.append(base)
        
        # base = base+'_'+current_user.operating_mode
        engine = get_engine(base)
        InfoRg = get_db_class('_InfoRg2721', engine)        
        row = session.query(InfoRg).first()
        row._Fld2723 = time
        row._Fld2725 = time
        row._Fld2724 = checked
        row._Fld2726 = checked        
        redis_store.hmset(base, {'period': data['TIME'], 'PO': PO})
        
    if len(connect_bases) > 0:
        session.commit()
        emit('server_response', {'info': 'button', 'procedure': 'change_period', 'data': connect_bases}, broadcast=True)

@socketio.on('start_counting', namespace='/test')
def start_counting(data):
    # запуск расчета баз
    PNN = 'ПНН' if data['CHECKED'] == True else 'без ПНН'
    connect_bases = []
    for base in data['BASES']:        
        host = redis_store.hmget(base[:3], ['host'])[0]        
        try:
            subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)            
        except subprocess.TimeoutExpired:            
            basename = redis_store.hmget(base[:3], ['name'])[0]
            emit('server_response', {'info': 'button', 'procedure': 'error', 'data': basename})
            continue        
        # base = base+'_'+current_user.operating_mode
        connect_bases.append(base)
        # engine  = get_engine(base)
        # ShedJob = get_db_class('_ScheduledJobs3995', engine)
        # if PNN == 'ПНН':
        #     session.query(ShedJob).filter(ShedJob._Description == 'Запуск обработок: 2. Выполнить расчет с ПНН').update({ShedJob._Use: b'\x01', ShedJob._JobKey: '1'})
        # else:
        #     session.query(ShedJob).filter(ShedJob._Description == 'Запуск обработок: 1. Выполнить расчет без ПНН').update({ShedJob._Use: b'\x01', ShedJob._JobKey: '1'})        
        # minutes = redis_store.hmget(base, ['interval'])[0]
        # check_time = (datetime.now()+timedelta(minutes=int(minutes))).strftime('%d.%m.%Y %H:%M:%S')        
        check_time = (datetime.now()).strftime('%d.%m.%Y %H:%M:%S') # DELETE        
        redis_store.hmset(base, {'check_time': check_time, 'PNN': PNN, 'status': '1'})
    if len(connect_bases) > 0:
        # session.commit()
        emit('server_response', {'info': 'button', 'procedure': 'start_counting', 'data': connect_bases}, broadcast=True)

@socketio.on('remove_base', namespace='/test')
def remove_base(data):    
    # удаление базы из посчитанных
    redis_store.hmset(data['BASE'], {'check_time': '', 'PNN': '', 'status': '0'})    
    emit('server_response', {'info': 'bandge', 'data': data['BASE']}, broadcast=True)

@socketio.on('clean_cache', namespace='/test')
def clean_cache(data):    
    for key in redis_store.hkeys('users'):
        if key[-8:] == data['BASE']:
            redis_store.hdel('users', key)  # удаляет данные из таблицы users
            redis_store.delete(key)         # удаляет подробную информацию о настройках пользователе в базе 1С
    redis_store.hmset(data['BASE'], {'period': '', 'PO': '', 'check_time': '', 'PNN': '', 'status': '0', 'cache': ''})
    emit('server_response', {'info': 'cache', 'data': data['BASE']}, broadcast=True)

@socketio.on('check_complite_base', namespace='/test')
def server_response():
    # проверка баз на окончание расчета    
    current_bases  = redis_store.smembers('current_bases')
    complite_bases = []
    
    grz = redis_store.hmget('grz', ['name', 'host', 'interval'])
    dbk = redis_store.hmget('dbk', ['name', 'host', 'interval'])
    lvt = redis_store.hmget('lvt', ['name', 'host', 'interval'])
    usm = redis_store.hmget('usm', ['name', 'host', 'interval'])

    grz_work = redis_store.hmget('grz_work', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])    
    grz_test = redis_store.hmget('grz_test', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])    
    dbk_work = redis_store.hmget('dbk_work', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])
    dbk_test = redis_store.hmget('dbk_test', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])
    lvt_work = redis_store.hmget('lvt_work', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])
    lvt_test = redis_store.hmget('lvt_test', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])
    usm_work = redis_store.hmget('usm_work', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])    
    usm_test = redis_store.hmget('usm_test', ['period', 'PO', 'check_time', 'PNN', 'status', 'cache'])    
    
    # for base in redis_store.smembers('bases'):
    for base in redis_store.smembers('current_bases'):
        for operating_mode in ['work', 'test']:        
            if redis_store.hmget(base+'_'+operating_mode, 'status')[0] == '1':
                str_date   = redis_store.hmget(base+'_'+operating_mode, ['check_time'])[0]
                check_time = datetime.strptime(str_date, '%d.%m.%Y %H:%M:%S')
                if check_time < datetime.now():                
                    str_date = redis_store.hmget(base+'_'+operating_mode, ['period'])[0]
                    date = datetime.strptime('01.'+str_date.replace('.2', '.4'), '%d.%m.%Y')
                    PNN  = redis_store.hmget(base+'_'+operating_mode, ['PNN'])[0]           
                    host = redis_store.hmget(base, ['host'])[0]        
                    try:
                        subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)                
                    except subprocess.TimeoutExpired:            
                        continue
                    # engine = get_engine(base+'_'+operating_mode)
                    # Doc_NS = get_db_class('_Document177', engine)
                    # Doc_RL = get_db_class('_Document188', engine)
                    # # получение результатов выполнения регламентного задания
                    # # # _Fld2115 - поле Описание в таблице "Начисление абонентам списком"
                    # # # _Fld2242 - поле Описание в таблице "Расчет льгот по абонентам"
                    # s  = session.query(Doc_NS).filter((Doc_NS._Fld2112 == date) & ((Doc_NS._Fld2115 == 'Абоненты с групповым измерительным оборудованием (создано обработкой)') | (Doc_NS._Fld2115 == 'Абоненты без групповых счетчиков (создано обработкой)'))).count()
                    # s1 = session.query(Doc_NS).filter(Doc_NS._Fld2112 == date, Doc_NS._Posted == b'\x01').count()
                    
                    # q  = session.query(Doc_RL).filter((Doc_RL._Fld2239 == date) & ((Doc_RL._Fld2242 == 'Абоненты с групповым измерительным оборудованием (создано обработкой)') | (Doc_RL._Fld2242 == 'Абоненты без групповых счетчиков (создано обработкой)'))).count()
                    # q1 = session.query(Doc_RL).filter(Doc_RL._Fld2239 == date, Doc_RL._Posted == b'\x01').count()

                    s = 0
                    s1 = 0
                    q = 0
                    q1 = 0

                    if s == s1 and q == q1: # количество проведенных = общему количеству за этот период            
                        # ShedJob = get_db_class('_ScheduledJobs3995', engine)
                        # # # завершение регламентного задания        
                        # if PNN == 'ПНН':
                        #     session.query(ShedJob).filter(ShedJob._Description == 'Запуск обработок: 2. Выполнить расчет с ПНН').update({ShedJob._Use: b'\x00', ShedJob._JobKey: '1'})
                        # else:
                        #     session.query(ShedJob).filter(ShedJob._Description == 'Запуск обработок: 1. Выполнить расчет без ПНН').update({ShedJob._Use: b'\x00', ShedJob._JobKey: '1'})                    
                        # session.commit()    
                        # redis_store.srem('bases', base)          # delete base from Redis            
                        redis_store.hmset(base+'_'+operating_mode, {'check_time': '', 'status': '2'})                        
                        # redis_store.sadd('complite_bases', base) # insert to Redis list of complited bases
            elif  redis_store.hmget(base+'_'+operating_mode, 'status')[0] == '2':                
                complite_bases.append(base+'_'+operating_mode)
    emit('server_response', {'info': 'server', 'data': complite_bases}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)