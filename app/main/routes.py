from flask import render_template, g, request, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from app.main import bp
from models import get_db_class, get_engine, session
from app import redis_store
import subprocess
import querySQL
from datetime import datetime, timedelta
from decimal import Decimal


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
        order = {'grz': '1', 'dbk': '2', 'lvt': '3', 'usm': '4'}
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
        if redis_store.sismember('current_bases', 'grz') == 0:
            redis_store.hmset('grz', {'name': 'Грязи', 'host': '192.168.105.1', 'interval': '10'})
            redis_store.hmset('grz_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('grz_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'grz')

        if redis_store.sismember('current_bases', 'dbk') == 0:
            redis_store.hmset('dbk', {'name': 'Добринка', 'host': '192.168.107.1', 'interval': '10'})
            redis_store.hmset('dbk_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('dbk_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'dbk')

        if redis_store.sismember('current_bases', 'lvt') == 0:
            redis_store.hmset('lvt', {'name': 'Лев Толстой', 'host': '192.168.114.1', 'interval': '10'})
            redis_store.hmset('lvt_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('lvt_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'lvt')

        if redis_store.sismember('current_bases', 'usm') == 0:
            redis_store.hmset('usm', {'name': 'Усмань', 'host': '192.168.117.1', 'interval': '10'})
            redis_store.hmset('usm_work', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.hmset('usm_test', {'cache': '', 'PO': '', 'period': '', 'status': '0', 'PNN': '', 'check_time': ''})
            redis_store.sadd('current_bases', 'usm')        
        
        order = {'grz': '1', 'dbk': '2', 'lvt': '3', 'usm': '4'}

        data = {}        
        for base in redis_store.smembers('current_bases'):
            num = order[base]
            data[num+base] = {
                            'basename': redis_store.hmget(base, ['name'])[0],                             
                            'interval': redis_store.hmget(base, ['interval'])[0]                            
                            }
                   
        return render_template('settings.html', data=data)
    
    host     = redis_store.hmget(db, ['host'])[0]
    basename = redis_store.hmget(db, ['name'])[0]    
    try:        
        subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)        
    except subprocess.TimeoutExpired:
        return render_template('/errors/503.html', basename=basename)
    
    users      = []
    bad_num_ls = []
    empty_grs  = []
    base = db+'_'+current_user.operating_mode
    engine = get_engine(base)            
    conn   = engine.connect()

    if redis_store.hmget(base, ['cache'])[0] == '':
        users = conn.execute(querySQL.sql_select9).fetchall()
        #!!! подумать о временных рамках получения данных для REDIS 
        # for user in users:
        #     key_id = user.username+'_'+base
        #     redis_store.hmset(key_id, {'username': user['username'], 'sett': user['sett'], 'res': user['res']})            
        #     redis_store.hset('users', key_id, key_id)
        # redis_store.hmset(base, {'cache': '1'})
    else:        
        for key in redis_store.hkeys('users'):            
            if key[-8:] == base:
                data_user = redis_store.hgetall(key)            
                users.append(data_user)    
        users = sorted(users, key=lambda x: x['username'])
    #идет получение данных о неправильных нормерах и пустых ГРС
    bad_num_ls = conn.execute(querySQL.sql_select7).fetchall()
    empty_grs  = conn.execute(querySQL.sql_select8).fetchall()

    return render_template('admin.html', users=users, basename=basename, bad_num_ls=bad_num_ls, empty_grs=empty_grs)

@bp.route('/abonents/<string:db>/<string:period_start>/<string:ls>')
@bp.route('/abonents/<string:db>/<string:period_start>/<string:ls>/<string:podkl>')
@login_required
def abonents(db, period_start, ls, podkl=None):
    # проверка на валидность
    if not validation(db=db, period_start=period_start, ls=ls, podkl=podkl):
        return abort(404)    
    result = []
    host = redis_store.hmget(db, ['host'])[0]
    name = redis_store.hmget(db, ['name'])[0]
    try:
        subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)                
    except subprocess.TimeoutExpired:            
        return render_template('abonents.html', data=result)    
    base   = db+'_'+current_user.operating_mode
    engine = get_engine(base)            
    conn   = engine.connect()    
    time   = datetime.strptime(period_start, '%d.%m.%Y')
    if podkl != None:
        podkl       = 'Подключен' if podkl == 'podkl' else 'Отключен'        
        sql_select5 = querySQL.sql_select5.replace('<доп переменная>', 'SET @P3 = ?')
        sql_select  = sql_select5.replace('<доп условие>', 'and dbo.Перечисление_СостоянияПодключенияАбонента.Наименование = @P3')        
        result      = conn.execute(sql_select, time, ls, podkl)
    else:
        sql_select5 = querySQL.sql_select5.replace('<доп переменная>', '')
        sql_select  = sql_select5.replace('<доп условие>', '')
        result      = conn.execute(sql_select, time, ls)    
    if podkl == 'Подключен':
        podkl = ' - подключенные'
    elif podkl == 'Отключен':
        podkl = ' - отключенные'
    else:
        podkl = ''
    ls = ' - открытые' if ls == 'on' else ' - закрытые'    
    text = ' на '+ period_start.replace('.4', '.2') +' ('+name+ls+podkl+')'
    
    return render_template('abonents.html', data=result, text=text)

# ajax
@bp.route('/get_data_abonent', methods=['post'])
@login_required
def get_data_abonent():
    db     = request.form['data'] # например grz_work
    ls     = request.form['ls']   # например '037000010'
    time   = datetime.strptime(request.form['period_start'], '%d.%m.%Y') # например '13.05.4019'
    data = []
    host   = redis_store.hmget(db, ['host'])[0]
    try:
        subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return jsonify(data)    
    base   = db+'_'+current_user.operating_mode
    engine = get_engine(base)
    conn   = engine.connect()    
    result = conn.execute(querySQL.sql_select6, time, ls)    
    
    sch    = ''
    otp    = ''
    pg     = ''
    otp_pv = ''
    cgv    = ''
    vnp    = ''
    for row in result:        
        Адрес               = '' if row['Адрес'] == None else row['Адрес']
        ВидДокумента        = '' if row['ВидДокумента'] == None else row['ВидДокумента']
        НомерДокумента      = '' if row['НомерДокумента'] == None else row['НомерДокумента']
        СерияДокумента      = '' if row['СерияДокумента'] == None else row['СерияДокумента']
        ДатаВыдачиДокумента = check_type(row['ДатаВыдачиДокумента'])
        if ДатаВыдачиДокумента != '':
            ДатаВыдачиДокумента = ДатаВыдачиДокумента+'г. '        
        КемВыданДокумент    = '' if row['КемВыданДокумент'] == None else row['КемВыданДокумент']
        text_ab = Адрес+'<br>'+ВидДокумента+' '+СерияДокумента+' '+НомерДокумента+'<br>'+ДатаВыдачиДокумента+' '+КемВыданДокумент        
        
        if row['ТипОборудования'] == 'Счетчик ':
            ДатаПоследнейПоверки = check_type(row['ДатаПоследнейПоверки'])
            ДатаОчереднойПоверки = check_type(row['ДатаОчереднойПоверки'])
            ПериодПоказаний      = check_type(row['ПериодПоказаний'])            
            Показания            = Decimal('0.000') if row['Показания'] == None else row['Показания']
            Показания            = '{0:,}'.format(Показания).replace(',', ' ')[:-4]
            sch = sch + row['Оборудование']+' ('+row['СостояниеОборудования']+')<br>Показания: '+ Показания + ' на '+ ПериодПоказаний + '<br>Дата последней поверки: '+ДатаПоследнейПоверки+'<br>Дата следующей поверки: '+ДатаОчереднойПоверки+'<br><br>'
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

    data = {'ЛичныеДанные':              text_ab,
            'Счетчик':                   sch[:-4],
            'ОтопительноеОборудование':  otp,
            'ПлитаГазовая':              pg,
            'ОтоплениеПодогрев':         otp_pv,
            'ЦентрГорВодоснабжение':     cgv,
            'ВодонагревательныеПриборы': vnp}
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
@bp.route('/get_data', methods=['post'])
@login_required
def get_data():
    # # проверка на валидность
    # if not validation(db=db, period_start=period_start, ls=ls, podkl=podkl):
    #     return abort(404)
    
    db           = request.form['db']           # например grz
    mode         = request.form['mode']         # например dz
    period_start = request.form['period_start'] # 13.05.4019
    period_end   = request.form['period_end']   # 13.05.4019

    data = []
    region = []    
    bases = {db} if db else redis_store.smembers('current_bases')    

    for db in bases:
        host = redis_store.hmget(db, ['host'])[0]
        name = redis_store.hmget(db, ['name'])[0]        
        try:
            subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)                
        except subprocess.TimeoutExpired:            
            continue
        base   = db+'_'+current_user.operating_mode
        engine = get_engine(base)            
        conn   = engine.connect()
        
        if mode == 'dz':
            time       = datetime.strptime(period_start, '%d.%m.%Y')
            check_time = time + timedelta(days=1)
            result     = conn.execute(querySQL.sql_select1, check_time)
            region = [name, '0.00']
            for row in result:           
                if row['SUMM'] == None:
                    region = [name, '0.00']
                else:                
                    region = [name, '{0:,}'.format(row['SUMM']).replace(',', ' ')]
        elif mode == 'op':
            time1  = datetime.strptime(period_start, '%d.%m.%Y')
            time2  = datetime.strptime(period_end, '%d.%m.%Y')        
            result = conn.execute(querySQL.sql_select2, time1, time2)
            region = [name, '0.00']
            for row in result:           
                if row['SUMM'] == None:
                    region = [name, '0.00']
                else:                
                    region = [name, '{0:,}'.format(row['SUMM']).replace(',', ' ')]
        elif mode == 'ab':
            time       = datetime.strptime(period_start, '%d.%m.%Y')
            result     = conn.execute(querySQL.sql_select4, time)
            total, podkl_o, otkl_o, total_o, podkl_z, otkl_z, total_z  = 0, 0, 0, 0, 0, 0, 0
            region = [name, total, podkl_o, otkl_o, total_o, podkl_z, otkl_z, total_z]
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
            region = [name, str(total), str(podkl_o), str(otkl_o), str(total_o), str(podkl_z), str(otkl_z), str(total_z), db]
        else:
            time1  = datetime.strptime(period_start, '%d.%m.%Y')
            time2  = datetime.strptime(period_end, '%d.%m.%Y') + timedelta(hours=23, minutes=59, seconds=59)
            result = conn.execute(querySQL.sql_select3, time1, time2)            
            pok_v, sred_v, netpok_v, ot_v, k_v, pgvs_v, cgvs_v, pv_v  = '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'
            pok_s, sred_s, netpok_s, ot_s, k_s, pgvs_s, cgvs_s, pv_s = '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'
            region = [[name, pok_v, pok_s, sred_v, sred_s, netpok_v, netpok_s, '0.000', '0.00'], [name, ot_v, ot_s, k_v, k_s, pgvs_v, pgvs_s, cgvs_v, cgvs_s, pv_v, pv_s, '0.000', '0.00']]
            itog1_v = Decimal('0.000')
            itog1_s = Decimal('0.00')
            itog2_v = Decimal('0.000')
            itog2_s = Decimal('0.00')
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
    name  = request.form['name']
    set_n = request.form['set']    
    if request.form['value'] == 'true':
        value = b'\x01' 
    else: 
        value = b'\x00'
    
    host     = redis_store.hmget(db, ['host'])[0]
    basename = redis_store.hmget(db, ['name'])[0]    
    try:
        subprocess.call(["ping", "-n", "1", host], timeout=0.25, stdout=subprocess.DEVNULL)        
    except subprocess.TimeoutExpired:
        return jsonify(basename)
    
    db = db+'_'+current_user.operating_mode
    engine   = get_engine(db)    
    Abonents = get_db_class('_Reference95', engine)
    Pvh      = get_db_class('_Chrc4250', engine)
    RegInfo  = get_db_class('_InfoRg4272', engine)    
    
    FIO_ref = session.query(Abonents).filter(Abonents._Description == name).first()._IDRRef
    Set_ref = session.query(Pvh).filter(Pvh._Description == set_n).first()._IDRRef    
    
    session.query(RegInfo).filter(RegInfo._Fld4273_RRRef == FIO_ref, RegInfo._Fld4274RRef == Set_ref).update({RegInfo._Fld4275_L: value})
    session.commit()
    
    redis_store.hset(name+'_'+db, 'res', value)
    
    return jsonify('yes')

# ajax
@bp.route('/save', methods=['post'])
@login_required
def save():
    base = request.form['db']
    try:
        interval = int(request.form['interval'])
        if interval < 10:
            interval = '10'
    except ValueError:
        interval = '10'
        
    redis_store.hmset(base, {'interval': interval})
    return jsonify('')

# ajax
@bp.route('/clean', methods=['post'])
@login_required
def clean():
    base = request.form['db']    
    for key in redis_store.hkeys('users'):
        if key[-8:] == base:
            redis_store.hdel('users', key)  # удаляет данные из таблицы users
            redis_store.delete(key)         # удаляет подробную информацию о настройках пользователе в базе 1С
    redis_store.hmset(base, {'period': '', 'PO': '', 'check_time': '', 'PNN': '', 'status': '0', 'cache': ''})
    return jsonify('')

def validation(db=None, mode=None, period_start=None, period_end=None, ls=None, podkl=None):
    try:
        if db != None and db not in redis_store.smembers('current_bases'):
            raise SyntaxError()
        if mode != None and mode not in ['dz', 'op', 'nach', 'ab']:
            raise SyntaxError()
        if ls != None and ls not in ['on', 'off']:
            raise SyntaxError()
        if podkl not in ['podkl', 'otkl', None]:
            raise SyntaxError()
        if period_start != None:
            period_start = datetime.strptime(period_start, '%d.%m.%Y')
        if period_end != None:    
            period_end   = datetime.strptime(period_end, '%d.%m.%Y')
        return True
    except:
        return False

def check_type(var):
    if isinstance(var, str):
        new_var = datetime.strptime(var, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y').replace('.4', '.2')
    elif isinstance(var, datetime):
        new_var = var.strftime('%d.%m.%Y').replace('.4', '.2')
    else:
        new_var  = ''
    return new_var