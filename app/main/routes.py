from app        import redis_store
from app.main   import bp
from app.email  import send_email
from models     import get_connection

from flask          import render_template, g, request, jsonify, redirect, url_for, abort
from flask_login    import login_required, current_user
from datetime       import datetime, timedelta
from decimal        import Decimal
from pymssql        import ProgrammingError, OperationalError 
from sys            import platform
from subprocess     import call, TimeoutExpired, DEVNULL


import querySQL


@bp.before_app_request
def before_request():
    current_bases       = redis_store.smembers('current_bases')
    bases_1_2           = [] # посчитанные базы и базы, в которых идет расчет
    bases_1             = [] # базы, в которых идет расчет
    bases_2             = [] # посчитанные базы
    unspecified_periods = [] # базы, в которых не установлен период
    statuses            = {}

    for base in current_bases:
        for operating_mode in ['work', 'test']:
            if redis_store.hmget(base+'_'+operating_mode, ['period'])[0] == redis_store.hmget(base+'_'+operating_mode, ['PO'])[0]:
                unspecified_periods.append(base+'_'+operating_mode)
            status = redis_store.hmget(base+'_'+operating_mode, ['status'])[0]
            if status != '0':
                period = redis_store.hmget(base+'_'+operating_mode, ['period'])[0]
                PO     = redis_store.hmget(base+'_'+operating_mode, ['PO'])[0]
                PNN    = redis_store.hmget(base+'_'+operating_mode, ['PNN'])[0]
                statuses[base+'_'+operating_mode] = period + PO +' '+ PNN
                bases_1_2.append(base+'_'+operating_mode)
                if status == '1': # базы, по которым идет расчет
                    bases_1.append(base+'_'+operating_mode)
                if status == '2': # посчитанные базы
                    bases_2.append(base+'_'+operating_mode)    
    g.bases_1_2           = bases_1_2
    g.bases_1             = bases_1
    g.bases_2             = bases_2
    g.unspecified_periods = unspecified_periods
    g.statuses            = statuses    

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if len(redis_store.smembers('current_bases')) == 0:
        return redirect(url_for('main.admin'))    
    return render_template('index.html')

@bp.route('/reports', defaults={'db':''})
@bp.route('/reports/<string:db>')
@login_required
def reports(db):
    name = ''
    if db:
        name = redis_store.hmget(db, ['name'])[0]    
    return render_template('reports.html', base=name, db=db)

@bp.route('/manage', defaults={'db':''})
@bp.route('/manage/<string:db>')
@login_required
def manage(db):
    data   = {}    
    if db:        
        name = redis_store.hmget(db, ['name'])[0]
        db   = db+'_'+current_user.operating_mode
        if redis_store.hmget(db, ['period'])[0] == redis_store.hmget(db, ['PO'])[0]:
            db = 'Установите период!'
        else:
            period = redis_store.hmget(db, ['period'])[0]
            PO     = redis_store.hmget(db, ['PO'])[0]            
            db     = name+' '+period+' '+PO        
    else:        
        # сортировка при выводе
        order = {'bor': 'a',
                 'vol': 'b',
                 'grz': 'c',
                 'dan': 'd',
                 'dbk': 'e',
                 'dbr': 'f',
                 'dlk': 'g',
                 'elc': 'h',
                 'zdn': 'i',
                 'izm': 'j',
                 'krs': 'k',
                 'lbd': 'l',
                 'lvt': 'm',
                 'stn': 'n',
                 'trb': 'o',
                 'usm': 'p',
                 'hlv': 'q',
                 'cha': 'r'}
        
        for base in redis_store.smembers('current_bases'):
            num = order[base]
            data[num+base] = {'basename': redis_store.hmget(base, ['name'])[0]}

    return render_template('manage.html', base=db, data=data)

@bp.route('/admin', defaults={'db':''})
@bp.route('/admin/<string:db>')
@login_required
def admin(db):
    if db == '':
        # первоначальное заполнение по умолчанию
        if redis_store.sismember('current_bases', 'elc') == 0:
            redis_store.hmset('elc', {'name': 'Елец', 'host': '192.168.102.1', 'interval': '10'})
            redis_store.hmset('elc_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('elc_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'elc')
        
        if redis_store.sismember('current_bases', 'bor') == 0:
            redis_store.hmset('bor', {'name': 'Борино', 'host': '192.168.103.1', 'interval': '10'})
            redis_store.hmset('bor_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('bor_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'bor')

        if redis_store.sismember('current_bases', 'vol') == 0:
            redis_store.hmset('vol', {'name': 'Волово', 'host': '192.168.104.1', 'interval': '10'})
            redis_store.hmset('vol_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('vol_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'vol')
        
        if redis_store.sismember('current_bases', 'grz') == 0:
            redis_store.hmset('grz', {'name': 'Грязи', 'host': '192.168.105.1', 'interval': '10'})
            redis_store.hmset('grz_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('grz_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'grz')

        if redis_store.sismember('current_bases', 'dan') == 0:
            redis_store.hmset('dan', {'name': 'Данков', 'host': '192.168.106.1', 'interval': '10'})
            redis_store.hmset('dan_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('dan_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'dan')
        
        if redis_store.sismember('current_bases', 'dbk') == 0:
            redis_store.hmset('dbk', {'name': 'Добринка', 'host': '192.168.107.1', 'interval': '10'})
            redis_store.hmset('dbk_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('dbk_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'dbk')

        if redis_store.sismember('current_bases', 'dbr') == 0:
            redis_store.hmset('dbr', {'name': 'Доброе', 'host': '192.168.108.1', 'interval': '10'})
            redis_store.hmset('dbr_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('dbr_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'dbr')

        if redis_store.sismember('current_bases', 'dlk') == 0:
            redis_store.hmset('dlk', {'name': 'Долгоруково', 'host': '192.168.109.1', 'interval': '10'})
            redis_store.hmset('dlk_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('dlk_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'dlk')

        if redis_store.sismember('current_bases', 'zdn') == 0:
            redis_store.hmset('zdn', {'name': 'Задонск', 'host': '192.168.110.1', 'interval': '10'})
            redis_store.hmset('zdn_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('zdn_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'zdn')
        
        if redis_store.sismember('current_bases', 'izm') == 0:
            redis_store.hmset('izm', {'name': 'Измалково', 'host': '192.168.111.1', 'interval': '10'})
            redis_store.hmset('izm_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('izm_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'izm')
        
        if redis_store.sismember('current_bases', 'krs') == 0:
            redis_store.hmset('krs', {'name': 'Красное', 'host': '192.168.112.1', 'interval': '10'})
            redis_store.hmset('krs_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('krs_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'krs')
        
        if redis_store.sismember('current_bases', 'lbd') == 0:
            redis_store.hmset('lbd', {'name': 'Лебедянь', 'host': '192.168.113.1', 'interval': '10'})
            redis_store.hmset('lbd_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('lbd_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'lbd')
        
        if redis_store.sismember('current_bases', 'lvt') == 0:
            redis_store.hmset('lvt', {'name': 'Лев Толстой', 'host': '192.168.114.1', 'interval': '10'})
            redis_store.hmset('lvt_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('lvt_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'lvt')

        if redis_store.sismember('current_bases', 'stn') == 0:
            redis_store.hmset('stn', {'name': 'Становое', 'host': '192.168.115.1', 'interval': '10'})
            redis_store.hmset('stn_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('stn_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'stn')
        
        if redis_store.sismember('current_bases', 'trb') == 0:
            redis_store.hmset('trb', {'name': 'Тербуны', 'host': '192.168.116.1', 'interval': '10'})
            redis_store.hmset('trb_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('trb_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'trb')

        if redis_store.sismember('current_bases', 'usm') == 0:
            redis_store.hmset('usm', {'name': 'Усмань', 'host': '192.168.117.1', 'interval': '10'})
            redis_store.hmset('usm_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('usm_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'usm')

        if redis_store.sismember('current_bases', 'hlv') == 0:
            redis_store.hmset('hlv', {'name': 'Хлевное', 'host': '192.168.118.1', 'interval': '10'})
            redis_store.hmset('hlv_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('hlv_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'hlv')
                
        if redis_store.sismember('current_bases', 'cha') == 0:
            redis_store.hmset('cha', {'name': 'Чаплыгин', 'host': '192.168.119.1', 'interval': '10'})
            redis_store.hmset('cha_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('cha_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'cha')
        
        order = {'bor': 'a',
                 'vol': 'b',
                 'grz': 'c',
                 'dan': 'd',
                 'dbk': 'e',
                 'dbr': 'f',
                 'dlk': 'g',
                 'elc': 'h',
                 'zdn': 'i',
                 'izm': 'j',
                 'krs': 'k',
                 'lbd': 'l',
                 'lvt': 'm',
                 'stn': 'n',
                 'trb': 'o',
                 'usm': 'p',
                 'hlv': 'q',
                 'cha': 'r'}
        
        # список баз с их интервалами проверки
        data = {}        
        for base in redis_store.smembers('current_bases'):
            num = order[base]
            data[num+base] = {
                            'basename': redis_store.hmget(base, ['name'])[0],                             
                            'interval': redis_store.hmget(base, ['interval'])[0]                            
                            }

        # список пользователей сайта
        users = [(key, redis_store.hgetall(key)['username'], redis_store.hgetall(key)['role']) for key in redis_store.hkeys('site_users')]
        
        # список баз, по которым идет расчет
        count_bases = []
        for base in redis_store.smembers('current_bases'):
            for operating_mode in ['work', 'test']:
                if redis_store.hmget(base+'_'+operating_mode, 'status')[0] == '1':
                    count_bases.append(base+'_'+operating_mode)

        return render_template('settings.html', data=data, users=users, count_bases=count_bases)
    
    host     = redis_store.hmget(db, ['host'])[0]
    basename = redis_store.hmget(db, ['name'])[0]    
    try:
        if platform == 'linux':
            call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
        else:
            call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
    except TimeoutExpired:
        return render_template('/errors/503.html', basename=basename)

    # cache()
    
    users      = []
    bad_num_ls = []
    empty_grs  = []
    base = db+'_'+current_user.operating_mode

    try:
        conn = get_connection(base)
        cursor = conn.cursor()
    except OperationalError as err:
        html_body='<p><b>Район:</b> '+basename+'</p><p><b>Действие:</b> Подключение к базе '+base+'</p><p><b>Текст ошибки: </b>'+str(err.args[0])+'</p>'
        send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        return render_template('errors/500.html', error=err)        

    # if redis_store.hmget(base, ['cache'])[0] == '': # в данном случае НЕ ИСПОЛЬЗУЕТСЯ Redis, данные каждый раз берутся из БД  
    #     users = conn.execute(querySQL.sql_select9).fetchall()        
    #     !!! подумать о временных рамках получения данных для REDIS 
    #     for user in users:
    #         key_id = user.username+'_'+base
    #         redis_store.hmset(key_id, {'username': user['username'], 'sett': user['sett'], 'res': user['res']})            
    #         redis_store.hset('users', key_id, key_id)
    #     redis_store.hmset(base, {'cache': '1'})
    # else:        
    #     for key in redis_store.hkeys('users'):            
    #         if key[-8:] == base:
    #             data_user = redis_store.hgetall(key)            
    #             users.append(data_user)    
    #     users = sorted(users, key=lambda x: x['username'])    
    #идет получение данных о неправильных нормерах и пустых ГРС
    # bad_num_ls = conn.execute(querySQL.sql_select7).fetchall()
    # empty_grs  = conn.execute(querySQL.sql_select8).fetchall()
    
    try:
        # настройки пользователей
        cursor.execute(querySQL.sql_select9)
        users = cursor.fetchall()
    except ProgrammingError as err:
        html_body='<p><b>Район:</b> '+basename+'</p><p><b>Действие:</b> Получение настроек пользователей</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
        send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
    try:
        # неправильные ЛС
        cursor.execute(querySQL.sql_select7)    
        bad_num_ls = cursor.fetchall()
    except ProgrammingError as err:
        html_body='<p><b>Район:</b> '+basename+'</p><p><b>Действие:</b> Получение данных по неправльным ЛС</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
        send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
    try:
        # здания без ГРС
        cursor.execute(querySQL.sql_select8)
        empty_grs  = cursor.fetchall()
    except ProgrammingError as err:
        html_body='<p><b>Район:</b> '+basename+'</p><p><b>Действие:</b> Получение данных по зданиям без ГРС</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
        send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
    
    conn.close()

    return render_template('admin.html', users=users, basename=basename, bad_num_ls=bad_num_ls, empty_grs=empty_grs)

@bp.route('/abonents')
@bp.route('/abonents/<string:db>/<string:period_start>/<string:status_ls>')
@bp.route('/abonents/<string:db>/<string:period_start>/<string:status_ls>/<string:status_podkl>')
@login_required
def abonents(db=None, period_start=None, status_ls=None, status_podkl=None):
    if (db == None and period_start == None and status_ls == None and status_podkl == None):
        # выводим страницу поиска
        return render_template('abonents.html', status=1)
    else:
        # проверка на валидность
        if not validation(db=db, period_start=period_start, status_ls=status_ls, status_podkl=status_podkl):
            return abort(404)    
        result = []
        host = redis_store.hmget(db, ['host'])[0]
        name = redis_store.hmget(db, ['name'])[0]
        try:            
            if platform == 'linux':
                call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
            else:
                call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
        except TimeoutExpired:            
            # выводим пустую страницу
            return render_template('abonents.html', data=result)    
        base   = db+'_'+current_user.operating_mode
        conn = get_connection(base)            
        cursor = conn.cursor()
        time   = datetime.strptime(period_start, '%d.%m.%Y')
        sql_select5 = querySQL.sql_select5.replace('<доп переменная @P2>', 'SET @P2 = %s').replace('<доп условие открыт/закрыт>', "and case when dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00' then 'on' else 'off' end = @P2")
        if status_podkl != None:
            status_podkl = 'Подключен' if status_podkl == 'podkl' else 'Отключен'
            sql_select5  = sql_select5.replace('<доп переменная @P3>', 'SET @P3 = %s').replace('<доп условие подключен/отключен>', 'and dbo.Перечисление_СостоянияПодключенияАбонента.Наименование = @P3')
            sql_select   = sql_select5.replace('<доп переменная @P4>', '').replace('<доп таблица спр.Абоненты>', '').replace('<доп условие отбор ЛС>', '')
            cursor.execute(sql_select, (time, status_ls, status_podkl))
            result = cursor.fetchall()            
        else:            
            sql_select5  = sql_select5.replace('<доп переменная @P3>', '').replace('<доп условие подключен/отключен>', '')
            sql_select   = sql_select5.replace('<доп переменная @P4>', '').replace('<доп таблица спр.Абоненты>', '').replace('<доп условие отбор ЛС>', '')
            cursor.execute(sql_select, (time, status_ls))
            result = cursor.fetchall()
        if status_podkl == 'Подключен':
            status_podkl = ' - подключенные'
        elif status_podkl == 'Отключен':
            status_podkl = ' - отключенные'
        else:
            status_podkl = ''
        status_ls = ' - открытые' if status_ls == 'on' else ' - закрытые'    
        text = ' на '+ period_start.replace('.4', '.2') +' ('+name+status_ls+status_podkl+')'
        conn.close()
        # выводим таблицу абонентов
        return render_template('abonents.html', data=result, text=text, status=0)

# ajax
@bp.route('/get_data_abonent', methods=['post'])
@login_required
def get_data_abonent():
    data = {}
    ls   = request.form['ls']   # например '037000010'
    db   = ''

    if 'period_start' in request.form:
        time = datetime.strptime(request.form['period_start'], '%d.%m.%Y')
    else:        
        time = datetime.now()

    if 'data' in request.form:
        db = request.form['data']
    else:
        base_number = ls[0:3]

        if base_number == '032':
            db = 'elc'
        elif base_number == '033':
            db = 'bor'
        elif base_number == '034':
            db = 'vol'
        elif base_number == '035':
            db = 'grz'
        elif base_number == '036':
            db = 'dan'
        elif base_number == '037':
            db = 'dbk'
        elif base_number == '038':
            db = 'dbr'
        elif base_number == '039':
            db = 'dlk'
        elif base_number == '040':
            db = 'zdn'
        elif base_number == '041':
            db = 'izm'        
        elif base_number == '042':
            db = 'krs'
        elif base_number == '043':
            db = 'lbd'
        elif base_number == '044':
            db = 'lvt'
        elif base_number == '045':
            db = 'stn'
        elif base_number == '046':
            db = 'trb'
        elif base_number == '047':
            db = 'usm'
        elif base_number == '048':
            db = 'hlv'
        elif base_number == '049':
            db = 'cha'

    host = redis_store.hmget(db, ['host'])[0]
    name = redis_store.hmget(db, ['name'])[0]
    try:            
        if platform == 'linux':
            call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
        else:
            call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)
    except (TimeoutExpired, TypeError):
        return jsonify(data)
    
    base   = db+'_'+current_user.operating_mode
    conn   = get_connection(base)
    cursor = conn.cursor()

    if 'search' in request.form:
        sql_select5 = querySQL.sql_select5.replace('<доп переменная @P2>', '').replace('<доп условие открыт/закрыт>', '')
        sql_select5 = sql_select5.replace('<доп переменная @P3>', '').replace('<доп условие подключен/отключен>', '')
        sql_select  = sql_select5.replace('<доп переменная @P4>', 'SET @P4 = %s').replace('<доп таблица спр.Абоненты>', 'inner join dbo.Справочник_Абоненты on dbo.РегистрСведений_СостояниеПодключениеУслуг.Абонент = dbo.Справочник_Абоненты.Ссылка').replace('<доп условие отбор ЛС>', 'and dbo.Справочник_Абоненты.ЛицевойСчет = @P4')
    
        try:
            cursor.execute(sql_select, (time, ls))# получение данных по состоянию подключения и персональным данным
            result = cursor.fetchone()
            data = get_personaldata(result)
        except ProgrammingError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Информация по абонентам (получение данных по состоянию подключения и персональным данным)</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        
        try:
            cursor.execute(querySQL.sql_select6, (time, ls))# получение данных по установленному оборудованию
            result = cursor.fetchall()
            ob = get_equipments(result)
            data.update(ob)
        except ProgrammingError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Информация по абонентам (получение данных по установленному оборудованию)</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
             
        try:
            cursor.execute(querySQL.sql_select11, (time, ls))# получение данных по параметрам расчета
            result = cursor.fetchall()
            param = get_parameters(result)
            data.update(param)
        except ProgrammingError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Информация по абонентам (получение данных по параметрам расчета)</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        
        try:
            cursor.execute(querySQL.sql_select12, (time, ls))# получение данных по режимам потребления
            result = cursor.fetchall()
            reg = get_regimes(result)
            data.update(reg)
        except ProgrammingError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Информация по абонентам (получение данных по режимам потребления)</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        
        try:
            cursor.execute(querySQL.sql_select13, (time, ls))# получение данных по взаиморасчетам
            result = cursor.fetchall()
            acc = get_accounts(result)
            data.update(acc)
        except ProgrammingError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Информация по абонентам (получение данных по взаиморасчетам)</p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        
    else:        
        sql_select = querySQL.sql_select6
        cursor.execute(sql_select, (time, ls))# получение данных по установленному оборудованию
        result = cursor.fetchall()
        data   = get_equipments(result)
    conn.close()
    
    return jsonify(data)

# ajax
@bp.route('/check', methods=['post'])
@login_required
def check():
    db = request.form['data'] # например grz_work
    if redis_store.hmget(db, ['status'])[0] == '1':
        return jsonify('Расчет запущен!')    
    return jsonify('ok')

# ajax
@bp.route('/check_user_role', methods=['get'])
@login_required
def check_user_role():    
    return jsonify(current_user.role == 'admin')

# ajax
@bp.route('/get_data', methods=['post'])
@login_required
def get_data():
    # # проверка на валидность
    # if not validation(db=db, period_start=period_start, ls=ls, podkl=podkl):
    #     return abort(404)
    
    db           = request.form['db']           # например grz
    mode         = request.form['mode']         # например dz
    period_start = request.form['period_start'] # 13.05.2019
    period_end   = request.form['period_end']   # 13.05.2019

    data = []
    region = []    
    bases = {db} if db else redis_store.smembers('current_bases')    

    for db in bases:
        host = redis_store.hmget(db, ['host'])[0]
        name = redis_store.hmget(db, ['name'])[0]        
        try:
            if platform == 'linux':
                call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
            else:
                call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)                
        except TimeoutExpired:            
            continue
        base   = db+'_'+current_user.operating_mode
        try:
            conn = get_connection(base)
        except OperationalError as err:
            html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Подключение к базе '+base+'</p><p><b>Текст ошибки: </b>'+str(err.args[0])+'</p>'
            send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
            continue
        cursor = conn.cursor()        
        if mode == 'dz':
            time       = datetime.strptime(period_start, '%d.%m.%Y')
            check_time = time + timedelta(days=1)
            region = [name, '0.00']
            try:
                cursor.execute(querySQL.sql_select1, (check_time,))
                result = cursor.fetchone()
                if result['SUMM'] != None:                
                    region = [name, '{0:,}'.format(result['SUMM']).replace(',', ' ')]
            except ProgrammingError as err:
                html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Формирование отчета по задолженности </p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
                send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        elif mode == 'op':
            time1  = datetime.strptime(period_start, '%d.%m.%Y')
            time2  = datetime.strptime(period_end, '%d.%m.%Y')
            region = [name, '0.00']
            try:
                cursor.execute(querySQL.sql_select2, (time1, time2))
                result = cursor.fetchone()
                if result['SUMM'] != None:
                    region = [name, '{0:,}'.format(result['SUMM']).replace(',', ' ')]
            except ProgrammingError as err:
                html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Формирование отчета по оплатам </p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
                send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
        elif mode == 'ab':
            time       = datetime.strptime(period_start, '%d.%m.%Y')            
            total, podkl_o, otkl_o, total_o, podkl_z, otkl_z, total_z  = 0, 0, 0, 0, 0, 0, 0
            region = [name, total, podkl_o, otkl_o, total_o, podkl_z, otkl_z, total_z]
            try:
                cursor.execute(querySQL.sql_select4, (time,))
                result = cursor.fetchall()
                for row in result:
                    if row['СостояниеЛС'] == 'Открыт':
                        if row['СостояниеПодключения'] == 'Подключен':
                            podkl_o = podkl_o + row['Количество']
                        else:
                            otkl_o = otkl_o + row['Количество']
                        total_o = total_o + row['Количество']
                    else:
                        if row['СостояниеПодключения'] == 'Подключен':
                            podkl_z = podkl_z + row['Количество']
                        else:
                            otkl_z = otkl_z + row['Количество']
                        total_z = total_z + row['Количество']
                    total = total + row['Количество']
            except ProgrammingError as err:
                html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Формирование отчета по абонентам </p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
                send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)
            region = [name, str(total), str(podkl_o), str(otkl_o), str(total_o), str(podkl_z), str(otkl_z), str(total_z), db]
        else:
            time1  = datetime.strptime(period_start, '%d.%m.%Y')
            time2  = datetime.strptime(period_end, '%d.%m.%Y') + timedelta(hours=23, minutes=59, seconds=59)            
            pok_v, sred_v, netpok_v, ot_v, k_v, pgvs_v, cgvs_v, pv_v  = '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'
            pok_s, sred_s, netpok_s, ot_s, k_s, pgvs_s, cgvs_s, pv_s = '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'
            region = [[name, pok_v, pok_s, sred_v, sred_s, netpok_v, netpok_s, '0.000', '0.00'], [name, ot_v, ot_s, k_v, k_s, pgvs_v, pgvs_s, cgvs_v, cgvs_s, pv_v, pv_s, '0.000', '0.00']]
            itog1_v = Decimal('0.000')
            itog1_s = Decimal('0.00')
            itog2_v = Decimal('0.000')
            itog2_s = Decimal('0.00')
            try:
                cursor.execute(querySQL.sql_select3, (time1, time2))
                result = cursor.fetchall()
                for row in result:
                    summ = 0.00 if row['SUMM'] == None else row['SUMM']
                    vol  = 0.000 if row['VOL'] == None else row['VOL']
                    rz   = '' if row['RZ'] == None else row['RZ']
                    if rz == 'Начисление по показаниям':
                        pok_v   = '{0:,}'.format(vol).replace(',', ' ')
                        pok_s   = '{0:,}'.format(summ).replace(',', ' ')
                        itog1_v = itog1_v + vol
                        itog1_s = itog1_s + summ
                    elif rz == 'Начисление по среднему':
                        sred_v  = '{0:,}'.format(vol).replace(',', ' ')
                        sred_s  = '{0:,}'.format(summ).replace(',', ' ')
                        itog1_v = itog1_v + vol
                        itog1_s = itog1_s + summ                    
                    elif rz == 'Начисление при отсутсвии показаний':
                        netpok_v = '{0:,}'.format(vol).replace(',', ' ')
                        netpok_s = '{0:,}'.format(summ).replace(',', ' ')
                        itog1_v  = itog1_v + vol
                        itog1_s  = itog1_s + summ                    
                    elif rz == 'Отопление жилых помещений':
                        ot_v    = '{0:,}'.format(vol).replace(',', ' ')
                        ot_s    = '{0:,}'.format(summ).replace(',', ' ')
                        itog2_v = itog2_v + vol
                        itog2_s = itog2_s + summ                    
                    elif rz == 'Пищеприготовление  и подогрев воды при наличии колонки':
                        k_v     = '{0:,}'.format(vol).replace(',', ' ')
                        k_s     = '{0:,}'.format(summ).replace(',', ' ')
                        itog2_v = itog2_v + vol
                        itog2_s = itog2_s + summ                    
                    elif rz == 'Пищеприготовление при наличии ГВС':
                        pgvs_v  = '{0:,}'.format(vol).replace(',', ' ')
                        pgvs_s  = '{0:,}'.format(summ).replace(',', ' ')
                        itog2_v = itog2_v + vol
                        itog2_s = itog2_s + summ                    
                    elif rz == 'Пищеприготовление при отсутствии ЦГВС':
                        cgvs_v  = '{0:,}'.format(vol).replace(',', ' ')
                        cgvs_s  = '{0:,}'.format(summ).replace(',', ' ')
                        itog2_v = itog2_v + vol
                        itog2_s = itog2_s + summ                    
                    elif rz == 'Подогрев воды':
                        pv_v    = '{0:,}'.format(vol).replace(',', ' ')
                        pv_s    = '{0:,}'.format(summ).replace(',', ' ')
                        itog2_v = itog2_v + vol
                        itog2_s = itog2_s + summ                    
                    
                    itog1_v_ = '{0:,}'.format(itog1_v).replace(',', ' ')
                    itog1_s_ = '{0:,}'.format(itog1_s).replace(',', ' ')
                    itog2_v_ = '{0:,}'.format(itog2_v).replace(',', ' ')
                    itog2_s_ = '{0:,}'.format(itog2_s).replace(',', ' ')
                    
                    region = [[name, pok_v, pok_s, sred_v, sred_s, netpok_v, netpok_s, itog1_v_, itog1_s_], [name, ot_v, ot_s, k_v, k_s, pgvs_v, pgvs_s, cgvs_v, cgvs_s, pv_v, pv_s, itog2_v_, itog2_s_]]
            except ProgrammingError as err:
                html_body='<p><b>Район:</b> '+name+'</p><p><b>Действие:</b> Формирование отчета по абонентам </p><p><b>Текст ошибки: </b>'+str(err.args[1])+'</p>'
                send_email('500 Internal Server Error', 'ak8647@rambler.ru', ['ak8647@rambler.ru'], html_body)            
        conn.close()
        data.append(region)    
    return jsonify(data)

# ajax
@bp.route('/get_info', methods=['post'])
@login_required
def get_info():
    db      = request.form['data'] # например grz_work
    type_op = request.form['type']    
    period  = redis_store.hmget(db, ['period'])[0]
    PO      = redis_store.hmget(db, ['PO'])[0]    
    if type_op == 'change_period':        
        name   = redis_store.hmget(db[:3], ['name'])[0]
        result = name +' '+ period +' '+ PO
    else:        
        PNN    = redis_store.hmget(db, ['PNN'])[0]        
        result = period + PO +' '+ PNN
    
    return jsonify(result)

# ajax
@bp.route('/change_mode', methods=['post'])
@login_required
def change_mode():
    operating_mode = request.form['operating_mode'] # 'work' или 'test'
    redis_store.hset(current_user.id, 'operating_mode', operating_mode)
    return jsonify('')

# ajax
@bp.route('/change', methods=['post'])
@login_required
def change():
    db    = request.form['db'] # например 'grz'
    name  = request.form['name'] # например 'Гринь Ольга Викторовна'
    if request.form['value'] == 'true':        
        value = 1
    else:        
        value = 0
    
    host     = redis_store.hmget(db, ['host'])[0]
    basename = redis_store.hmget(db, ['name'])[0]    
    try:
        if platform == 'linux':
            call(["ping", "-c", "1", host], timeout=0.25, stdout=DEVNULL)
        else:
            call(["ping", "-n", "1", host], timeout=0.25, stdout=DEVNULL)        
    except TimeoutExpired:
        return jsonify(basename)
    
    db = db+'_'+current_user.operating_mode
    conn = get_connection(db)
    cursor = conn.cursor()
    cursor.execute(querySQL.sql_update1, (value, name))
    conn.commit()
    conn.close()    
    #redis_store.hset(name+'_'+db, 'res', value) закометировал, т.к. не используется кэширование для Настройки пользователей (см. def admin(db):) 
    
    return jsonify('yes')

# ajax
@bp.route('/save', methods=['post'])
@login_required
def save():
    # сохранение интевала проверки
    if 'db' in request.form:
        base = request.form['db'] # например dbk 
        try:
            interval = int(request.form['interval'])
            if interval < 10:
                interval = '10'
        except ValueError:
            interval = '10'
            
        redis_store.hmset(base, {'interval': interval})

        return jsonify('')
    else:    
        # сохранение данных пользователя сайта
        key      = request.form['key']
        username = request.form['username']
        role     = request.form['role']    
        
        redis_store.hset(key, 'username', username)
        redis_store.hset(key, 'role', role)
        
        return jsonify({'key': key, 'username': username, 'role': role})    

# ajax
@bp.route('/clean', methods=['post'])
@login_required
def clean():
    if 'key' in request.form:
        key = request.form['key']
        redis_store.hdel('site_users', key)  # удаляем данные из таблицы site_users
        redis_store.delete(key) # удаляем информацию о пользователе сайта        
    else:
        base = request.form['db']
        redis_store.hmset(base, {'status': '0'})
    # base = request.form['db']    
    # for key in redis_store.hkeys('users'):
    #     if key[-8:] == base:
    #         redis_store.hdel('users', key)  # удаляет данные из таблицы users
    #         redis_store.delete(key)         # удаляет подробную информацию о настройках пользователе в базе 1С
    # redis_store.hmset(base, {'period': '', 'PO': '', 'check_time': '', 'PNN': '', 'status': '0', 'cache': ''})
    return jsonify('')

# ######################
# functions
# ######################
def validation(db=None, mode=None, period_start=None, period_end=None, status_ls=None, status_podkl=None):
    try:
        if db != None and db not in redis_store.smembers('current_bases'):
            raise SyntaxError()
        if mode != None and mode not in ['dz', 'op', 'nach', 'ab']:
            raise SyntaxError()
        if status_ls != None and status_ls not in ['on', 'off']:
            raise SyntaxError()
        if status_podkl not in ['podkl', 'otkl', None]:
            raise SyntaxError()
        if period_start != None:
            period_start = datetime.strptime(period_start, '%d.%m.%Y')
        if period_end != None:    
            period_end   = datetime.strptime(period_end, '%d.%m.%Y')
        return True
    except:
        return False

def get_personaldata(result):
    abon_data = {'PersonalData': '',
                 'Status':       ''}
    
    if result == None:
        return abon_data

    Адрес               = '' if result['Адрес']               == None else '<br>Адрес: '+result['Адрес']
    ВидДокумента        = '' if result['ВидДокумента']        == None else '<br>'       +result['ВидДокумента']    
    СерияДокумента      = '' if result['СерияДокумента']      == None else ' ('          +result['СерияДокумента']
    НомерДокумента      = '' if result['НомерДокумента']      == None else ' '          +result['НомерДокумента']    
    ДатаВыдачиДокумента = '' if result['ДатаВыдачиДокумента'] == None else ')<br>'       +result['ДатаВыдачиДокумента']+'г. '    
    КемВыданДокумент    = '' if result['КемВыданДокумент']    == None else ' '          +result['КемВыданДокумент']
    
    ЛицевойСчет  = 'Лицевой счет: '+result['ЛС']
    ФИО          = '<br>ФИО: '+result['ФИО']
    СостояниеЛС  = 'Открыт' if result['СостояниеЛС'] == 'on' else 'Закрыт'
                    
    PersonalData = ЛицевойСчет+ФИО+Адрес+ВидДокумента+СерияДокумента+НомерДокумента+ДатаВыдачиДокумента+КемВыданДокумент
    Status       = СостояниеЛС+' ('+result['ДатаОткрытияЗакрытия']+')<br>'+result['СостояниеПодключения']+' ('+result['ДатаПодключенияОтключения']+')'

    abon_data = {'PersonalData': PersonalData,
                 'Status':       Status}

    return abon_data

def get_equipments(result):
    sch = otp = pg = otp_pv = cgv = vnp = ''
    for row in result:        
        if row['ТипОборудования'] == 'Счетчик ':            
            ДатаПоследнейПоверки = row['ДатаПоследнейПоверки']
            ДатаОчереднойПоверки = row['ДатаОчереднойПоверки']
            ПериодПоказаний      = row['ПериодПоказаний']
            Показания            = Decimal('0.000') if row['Показания'] == None else row['Показания']
            Показания            = '{0:,}'.format(Показания).replace(',', ' ')[:-4]
            sch = sch + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>Показания: '+ Показания + ' на '+ ПериодПоказаний + '<br>Дата последней поверки: '+ДатаПоследнейПоверки+'<br>Дата следующей поверки: '+ДатаОчереднойПоверки+'<br>'
        elif row['ТипОборудования'] == 'Отопительное оборудование':
            otp = otp + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>'
        elif row['ТипОборудования'] == 'Плита газовая':
            pg = pg + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>'
        elif row['ТипОборудования'] == 'Отопление + подогрев воды':
            otp_pv = otp_pv + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>'
        elif row['ТипОборудования'] == 'Центр. гор. водоснабжение':
            cgv = cgv + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>'
        elif row['ТипОборудования'] == 'Водонагревательные приборы':
            vnp = vnp + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>'
        else:
            pass #Возможно будут еще типы оборудования
        
    ПУ      = '' if sch == '' else '<strong>Прибор учета</strong><br>'+sch+'<br>'
    ОтОб    = '' if otp == '' else '<strong>Отопительное оборудование</strong><br>'+otp+'<br>'
    ПГ      = '' if pg == '' else '<strong>Плита газовая</strong><br>'+pg+'<br>'
    ОтПВ    = '' if otp_pv == '' else '<strong>Отопление + подогрев воды</strong><br>'+otp_pv+'<br>'
    ЦГВ     = '' if cgv == '' else '<strong>Центр. гор. водоснабжение</strong><br>'+cgv+'<br>'
    ВП      = '' if vnp == '' else '<strong>Водонагревательные приборы</strong><br>'+vnp+'<br>'        
    
    abon_data = {'Equipments': ПУ+ОтОб+ПГ+ОтПВ+ЦГВ+ВП}
    
    return abon_data

def get_parameters(result):
    param1 = param2 = param3 = param4 = param5 = param6 = ''
    for row in result:
        if row['Параметры'] == 'Количество собственников':
            param1 = 'Количество собственников: '+row['Значения']+'<br>'
        if row['Параметры'] == 'Наличие горячего водоснабжения':
            param2 = 'Наличие горячего водоснабжения: '+row['Значения']+'<br>'
        if row['Параметры'] == 'Количество проживающих':
            param3 = 'Количество проживающих: '+row['Значения'].replace('.00', '')+'<br>'
        if row['Параметры'] == 'Вид договора':
            param4 = 'Вид договора: '+row['Значения']+'<br>'
        if row['Параметры'] == 'Площадь жилая':
            param5 = 'Площадь жилая: '+row['Значения']+'<br>'
        if row['Параметры'] == 'Доля собственности':
            param6 = 'Доля собственности: '+row['Значения']+'<br>'
    abon_data = {'Parameters': param1+param2+param3+param4+param5+param6}

    return abon_data

def get_regimes(result):
    uu = pu = param1 = param2 = param3 = param4 = param5 = ''
    for row in result:
        uu = '<strong>'+row['УзелУчета']+' ('+row['ДатаНачалаДействия']+')</strong><br>'
        pu = '<span style="margin-left: 20px">'+row['Оборудование']+'</span><br>'
        if row['РежимПотребления'] == 'Пищеприготовление  и подогрев воды при наличии колонки':
            param1 = '<span style="margin-left: 40px">Пищеприготовление и подогрев воды при наличии колонки ('+row['Действует']+')</span><br>'
        if row['РежимПотребления'] == 'Пищеприготовление при наличии ГВС':
            param2 = '<span style="margin-left: 40px">Пищеприготовление при наличии ГВС ('+row['Действует']+')</span><br>'
        if row['РежимПотребления'] == 'Пищеприготовление при отсутствии ЦГВС':
            param3 = '<span style="margin-left: 40px">Пищеприготовление при отсутствии ЦГВС ('+row['Действует']+')</span><br>'
        if row['РежимПотребления'] == 'Отопление жилых помещений':
            param4 = '<span style="margin-left: 40px">Отопление жилых помещений ('+row['Действует']+')</span><br>'
        if row['РежимПотребления'] == 'Подогрев воды':
            param5 = '<span style="margin-left: 40px">Подогрев воды ('+row['Действует']+')</span><br>'
        
    abon_data = {'Regimes': uu+pu+param1+param2+param3+param4+param5}

    return abon_data

def get_accounts(result):
    s1 = Decimal('0.00')
    s2 = Decimal('0.00')
    s3 = Decimal('0.00')
    p0 = p1 = p2 = p3 = p4 = p5 = ''    
    for row in result:        
        p0 ='''<table class="table">
                    <thead>                        
                        <tr>
                            <td style="font-size: 13px;">Услуга</td>
                            <td align=right style="font-size: 13px;">Текущая</td>
                            <td align=right style="font-size: 13px;">Рассрочка</td>
                            <td align=right style="font-size: 13px;">Списанная</td>
                        </tr>
                    </thead>
                    <tbody>
                        '''
        
        if row['Услуга'] == 'Газоснабжение природным газом':
            var1 = '{0:,}'.format(row['ТекущаяЗадолженность']).replace(',', ' ')
            var2 = '{0:,}'.format(row['Рассрочка']).replace(',', ' ')
            var3 = '{0:,}'.format(row['СписаннаяЗадолженность']).replace(',', ' ')            
            p1 = '<tr><td style="font-size: 13px;">Газоснабжение природным газом</td><td align=right>'+var1+'</td><td align=right>'+var2+'</td><td align=right>'+var3+'</td></tr>'
        if row['Услуга'] == 'Гос пошлина':
            var1 = '{0:,}'.format(row['ТекущаяЗадолженность']).replace(',', ' ')
            var2 = '{0:,}'.format(row['Рассрочка']).replace(',', ' ')
            var3 = '{0:,}'.format(row['СписаннаяЗадолженность']).replace(',', ' ')
            p2 = '<tr><td style="font-size: 13px;">Госпошлина</td><td align=right>'+var1+'</td><td align=right>'+var2+'</td><td align=right>'+var3+'</td></tr>'        
        s1 = s1 + row['ТекущаяЗадолженность']
        s2 = s2 + row['Рассрочка']
        s3 = s3 + row['СписаннаяЗадолженность']        
        e3 = '{0:,}'.format(s1).replace(',', ' ')
        e4 = '{0:,}'.format(s2).replace(',', ' ')
        e5 = '{0:,}'.format(s3).replace(',', ' ')
        p4 = '<tr><td><strong>ВСЕГО</strong></td><td align=right>'+e3+'</td><td align=right>'+e4+'</td><td align=right>'+e5+'</td></tr>'
        p5 ='''</tbody>
            </table>'''
    
    abon_data = {'Accounts': p0+p1+p2+p3+p4+p5}

    return abon_data
