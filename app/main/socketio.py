from app            import socketio, redis_store
from models         import get_connection
from flask_socketio import emit
from datetime       import datetime, timedelta
from sys            import platform
from subprocess     import call, TimeoutExpired, DEVNULL 

import querySQL

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

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
        checked = 1
        PO      = '(v)'
    else:
        checked = 0
        PO      = '( )'
    connect_bases = []
    for base in data['BASES']:        
        host = redis_store.hmget(base[:3], ['host'])[0]
        try:            
            if platform == 'linux':
                call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
            else:
                call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
        except TimeoutExpired:
            basename = redis_store.hmget(base[:3], ['name'])[0]
            emit('server_response', {'info': 'button', 'procedure': 'error', 'data': basename})            
            continue            
        connect_bases.append(base)        
        
        conn = get_connection(base)
        cursor = conn.cursor()
        cursor.execute(querySQL.sql_update2, (time, checked))
        conn.commit()
        conn.close()

        redis_store.hmset(base, {'period': data['TIME'], 'PO': PO})
        
    if len(connect_bases) > 0:        
        emit('server_response', {'info': 'button', 'procedure': 'change_period', 'data': connect_bases}, broadcast=True)

@socketio.on('start_counting', namespace='/test')
def start_counting(data):
    # запуск расчета баз
    PNN = 'ПНН' if data['CHECKED'] == True else 'без ПНН'
    connect_bases = []
    for base in data['BASES']:
        host = redis_store.hmget(base[:3], ['host'])[0]
        try:            
            if platform == 'linux':
                call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
            else:
                call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
        except TimeoutExpired:
            basename = redis_store.hmget(base[:3], ['name'])[0]
            emit('server_response', {'info': 'button', 'procedure': 'error', 'data': basename})
            continue        
        connect_bases.append(base)
        
        conn = get_connection(base)
        cursor = conn.cursor()
        if PNN == 'ПНН':
            cursor.execute(querySQL.sql_update3, (1, 1, 'Запуск обработок: 2. Выполнить расчет с ПНН'))
        else:
            cursor.execute(querySQL.sql_update3, (1, 1, 'Запуск обработок: 1. Выполнить расчет без ПНН'))
        conn.commit()
        conn.close()        
        # minutes = redis_store.hmget(base, ['interval'])[0]
        # check_time = (datetime.now()+timedelta(minutes=int(minutes))).strftime('%d.%m.%Y %H:%M:%S')        
        check_time = (datetime.now()).strftime('%d.%m.%Y %H:%M:%S') # DELETE THIS ROW        
        redis_store.hmset(base, {'check_time': check_time, 'PNN': PNN, 'status': '1'}) # need to check 
    if len(connect_bases) > 0:        
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
    
    for base in redis_store.smembers('current_bases'):
        for operating_mode in ['work', 'test']:
            if redis_store.hmget(base+'_'+operating_mode, 'status')[0] == '1': # если у базы статус "идет расчет", то проверяем по документам начисления и льгот
                str_date   = redis_store.hmget(base+'_'+operating_mode, ['check_time'])[0]
                check_time = datetime.strptime(str_date, '%d.%m.%Y %H:%M:%S')
                if check_time < datetime.now():
                    str_date = redis_store.hmget(base+'_'+operating_mode, ['period'])[0]
                    date = datetime.strptime('01.'+str_date.replace('.2', '.4'), '%d.%m.%Y')
                    PNN  = redis_store.hmget(base+'_'+operating_mode, ['PNN'])[0]
                    host = redis_store.hmget(base, ['host'])[0]
                    try:                        
                        if platform == 'linux':
                            call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
                        else:
                            call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
                    except TimeoutExpired:
                        continue
                    conn = get_connection(base+'_'+operating_mode)
                    cursor = conn.cursor()
                    cursor.execute(querySQL.sql_select10, (date, 'Абоненты с групповым измерительным оборудованием (создано обработкой)', 'Абоненты без групповых счетчиков (создано обработкой)'))
                    result = cursor.fetchone()                    
                    if result['STATUS'] == 1: # если количество проведенных документов начислений равно общему количеству документов за установленный учетный месяц
                        if PNN == 'ПНН':
                            cursor.execute(querySQL.sql_update3, (0, 1, 'Запуск обработок: 2. Выполнить расчет с ПНН'))
                        else:
                            cursor.execute(querySQL.sql_update3, (0, 1, 'Запуск обработок: 1. Выполнить расчет без ПНН'))
                        conn.commit()
                        redis_store.hmset(base+'_'+operating_mode, {'check_time': '', 'status': '2'}) # меняем статус базы на "расчет завершен"
                    conn.close()
            elif  redis_store.hmget(base+'_'+operating_mode, 'status')[0] == '2': # если у базы "расчет завершен"
                complite_bases.append(base+'_'+operating_mode)
    emit('server_response', {'info': 'server', 'data': complite_bases}, broadcast=True)

# if __name__ == '__main__':
#     socketio.run(app)