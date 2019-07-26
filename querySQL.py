# текущая сумма деб. задолженности
sql_select1 = '''
                    SET NOCOUNT ON;
                    
                    DECLARE @P1 DATETIME

                    SET		@P1 = DATEADD(year, 2000, %s) --период
                    --   	0x963228632B0039644C534B49F4AFF61D -- услуга населению "Газоснабжение природным газом"

                    SELECT
                    (CAST(SUM(T1.Q_001_F_003_) AS NUMERIC(38, 2))) as DZ
                    INTO #VT
                    FROM (SELECT
                            T2.Q_001_F_000RRef AS Q_001_F_000RRef,
                            T2.Q_001_F_002RRef AS Q_001_F_001RRef,
                            ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'}) AS Q_001_F_002_,
                            CAST(SUM(T2.Q_001_F_003_) AS NUMERIC(38, 8)) AS Q_001_F_003_,
                            CAST(DATEDIFF(MONTH,DATEADD(DAY,1.0 - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'})) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'})) AS NUMERIC(4)) - 2000) - 2000,{ts '4000-01-01 00:00:00'}))),T2.Q_001_F_005_) AS NUMERIC(12)) AS Q_001_F_004_,
                            T2.Q_001_F_004RRef AS Q_001_F_005RRef
                            FROM (SELECT
                                    T3.Fld3873RRef AS Q_001_F_000RRef,
                                    T3.Fld3874_ AS Q_001_F_001_,
                                    T3.Fld3872RRef AS Q_001_F_002RRef,
                                    CAST(SUM(T3.Fld3875Balance_) AS NUMERIC(38, 8)) AS Q_001_F_003_,
                                    T3.Fld3871RRef AS Q_001_F_004RRef,
                                    {ts '4019-04-01 00:00:00'} AS Q_001_F_005_
                                    FROM (SELECT
                                            T4.Fld3872RRef AS Fld3872RRef,
                                            T4.Fld3874_ AS Fld3874_,
                                            T4.Fld3873RRef AS Fld3873RRef,
                                            T4.Fld3871RRef AS Fld3871RRef,
                                            CAST(SUM(T4.Fld3875Balance_) AS NUMERIC(37, 5)) AS Fld3875Balance_
                                            FROM (SELECT
                                                    T5._Fld3872RRef AS Fld3872RRef,
                                                    T5._Fld3874 AS Fld3874_,
                                                    T5._Fld3873RRef AS Fld3873RRef,
                                                    T5._Fld3871RRef AS Fld3871RRef,
                                                    CAST(SUM(T5._Fld3875) AS NUMERIC(31, 5)) AS Fld3875Balance_
                                                    FROM dbo._AccumRgT3888 T5
                                                    WHERE T5._Period = '5999-11-01 00:00:00' AND (T5._Fld3875 <> 0) AND (T5._Fld3875 <> 0)
                                                    GROUP BY T5._Fld3872RRef,
                                                    T5._Fld3874,
                                                    T5._Fld3873RRef,
                                                    T5._Fld3871RRef
                                                    HAVING (CAST(SUM(T5._Fld3875) AS NUMERIC(31, 5))) <> 0.0
                                                    
                                                    UNION ALL SELECT
                                                    
                                                    T6._Fld3872RRef AS Fld3872RRef,
                                                    T6._Fld3874 AS Fld3874_,
                                                    T6._Fld3873RRef AS Fld3873RRef,
                                                    T6._Fld3871RRef AS Fld3871RRef,
                                                    CAST(CAST(SUM(CASE WHEN T6._RecordKind = 0.0 THEN -T6._Fld3875 ELSE T6._Fld3875 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld3875Balance_
                                                    FROM dbo._AccumRg3869 T6
                                                    WHERE T6._Period >= @P1 AND T6._Period < '5999-11-01 00:00:00' AND T6._Active = 0x01
                                                    GROUP BY T6._Fld3872RRef,
                                                    T6._Fld3874,
                                                    T6._Fld3873RRef,
                                                    T6._Fld3871RRef
                                                    HAVING (CAST(CAST(SUM(CASE WHEN T6._RecordKind = 0.0 THEN -T6._Fld3875 ELSE T6._Fld3875 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T4
                                            GROUP BY T4.Fld3872RRef,
                                            T4.Fld3874_,
                                            T4.Fld3873RRef,
                                            T4.Fld3871RRef
                                    HAVING (CAST(SUM(T4.Fld3875Balance_) AS NUMERIC(37, 5))) <> 0.0) T3
                                    GROUP BY T3.Fld3872RRef,
                                    T3.Fld3874_,
                                    T3.Fld3873RRef,
                                    T3.Fld3871RRef
                            
                                    UNION ALL SELECT
                                    
                                    T7.Fld3893RRef AS Fld3893RRef,
                                    CASE WHEN (T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF) THEN DATEADD(DAY,1.0 - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF THEN T11._Fld2303 ELSE CAST(NULL AS DATETIME) END) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF THEN T11._Fld2303 ELSE CAST(NULL AS DATETIME) END) AS NUMERIC(4)) - 2000) - 2000,{ts '4000-01-01 00:00:00'}))) ELSE CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000C3 THEN T12._Fld2440 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00001953 THEN T13._Fld6497 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BE THEN T14._Fld2263 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000011A8 THEN T15.УчетныйМесяц WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00000098 THEN T16._Fld4099 ELSE CAST(NULL AS DATETIME) END END,
                                    T7.Fld3892RRef AS Fld3892RRef,
                                    CAST(SUM(T7.Fld3896Balance_) AS NUMERIC(38, 8)),
                                    T7.Fld3891RRef AS Fld3891RRef,
                                    {ts '4019-04-01 00:00:00'}
                                    FROM (SELECT
                                            T8.Fld3892RRef AS Fld3892RRef,
                                            T8.Fld3895_TYPE AS Fld3895_TYPE,
                                            T8.Fld3895_RTRef AS Fld3895_RTRef,
                                            T8.Fld3895_RRRef AS Fld3895_RRRef,
                                            T8.Fld3891RRef AS Fld3891RRef,
                                            T8.Fld3893RRef AS Fld3893RRef,
                                            CAST(SUM(T8.Fld3896Balance_) AS NUMERIC(37, 5)) AS Fld3896Balance_
                                            FROM (SELECT
                                                    T9._Fld3892RRef AS Fld3892RRef,
                                                    T9._Fld3895_TYPE AS Fld3895_TYPE,
                                                    T9._Fld3895_RTRef AS Fld3895_RTRef,
                                                    T9._Fld3895_RRRef AS Fld3895_RRRef,
                                                    T9._Fld3891RRef AS Fld3891RRef,
                                                    T9._Fld3893RRef AS Fld3893RRef,
                                                    CAST(SUM(T9._Fld3896) AS NUMERIC(31, 5)) AS Fld3896Balance_
                                                    FROM dbo._AccumRgT3910 T9
                                                    WHERE T9._Period = '5999-11-01 00:00:00' AND (T9._Fld3896 <> 0) AND (T9._Fld3896 <> 0)
                                                    GROUP BY T9._Fld3892RRef,
                                                    T9._Fld3895_TYPE,
                                                    T9._Fld3895_RTRef,
                                                    T9._Fld3895_RRRef,
                                                    T9._Fld3891RRef,
                                                    T9._Fld3893RRef
                                                    HAVING (CAST(SUM(T9._Fld3896) AS NUMERIC(31, 5))) <> 0.0
                                                    
                                                    UNION ALL SELECT
                                                    
                                                    T10._Fld3892RRef AS Fld3892RRef,
                                                    T10._Fld3895_TYPE AS Fld3895_TYPE,
                                                    T10._Fld3895_RTRef AS Fld3895_RTRef,
                                                    T10._Fld3895_RRRef AS Fld3895_RRRef,
                                                    T10._Fld3891RRef AS Fld3891RRef,
                                                    T10._Fld3893RRef AS Fld3893RRef,
                                                    CAST(CAST(SUM(CASE WHEN T10._RecordKind = 0.0 THEN -T10._Fld3896 ELSE T10._Fld3896 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld3896Balance_
                                                    FROM dbo._AccumRg3889 T10
                                                    WHERE T10._Period >= @P1 AND T10._Period < '5999-11-01 00:00:00' AND T10._Active = 0x01
                                                    GROUP BY T10._Fld3892RRef,
                                                    T10._Fld3895_TYPE,
                                                    T10._Fld3895_RTRef,
                                                    T10._Fld3895_RRRef,
                                                    T10._Fld3891RRef,
                                                    T10._Fld3893RRef
                                                    HAVING (CAST(CAST(SUM(CASE WHEN T10._RecordKind = 0.0 THEN -T10._Fld3896 ELSE T10._Fld3896 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T8
                                            GROUP BY T8.Fld3892RRef,
                                            T8.Fld3895_TYPE,
                                            T8.Fld3895_RTRef,
                                            T8.Fld3895_RRRef,
                                            T8.Fld3891RRef,
                                            T8.Fld3893RRef
                                    HAVING (CAST(SUM(T8.Fld3896Balance_) AS NUMERIC(37, 5))) <> 0.0) T7
                                    LEFT OUTER JOIN dbo._Document191 T11
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF AND T7.Fld3895_RRRef = T11._IDRRef
                                    LEFT OUTER JOIN dbo._Document195 T12
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000C3 AND T7.Fld3895_RRRef = T12._IDRRef
                                    LEFT OUTER JOIN dbo._Document6483 T13
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00001953 AND T7.Fld3895_RRRef = T13._IDRRef
                                    LEFT OUTER JOIN dbo._Document190 T14
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BE AND T7.Fld3895_RRRef = T14._IDRRef
                                    LEFT OUTER JOIN dbo.Документ_Квитанция T15
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000011A8 AND T7.Fld3895_RRRef = T15.Ссылка
                                    LEFT OUTER JOIN dbo._Document152 T16
                                    ON T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00000098 AND T7.Fld3895_RRRef = T16._IDRRef
                                    GROUP BY T7.Fld3892RRef,
                                    CASE WHEN (T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF) THEN DATEADD(DAY,1.0 - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF THEN T11._Fld2303 ELSE CAST(NULL AS DATETIME) END) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BF THEN T11._Fld2303 ELSE CAST(NULL AS DATETIME) END) AS NUMERIC(4)) - 2000) - 2000,{ts '4000-01-01 00:00:00'}))) ELSE CASE WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000C3 THEN T12._Fld2440 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00001953 THEN T13._Fld6497 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000000BE THEN T14._Fld2263 WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x000011A8 THEN T15.УчетныйМесяц WHEN T7.Fld3895_TYPE = 0x08 AND T7.Fld3895_RTRef = 0x00000098 THEN T16._Fld4099 ELSE CAST(NULL AS DATETIME) END END,
                                    T7.Fld3893RRef,
                                    T7.Fld3891RRef) T2		
                            GROUP BY T2.Q_001_F_002RRef,
                            T2.Q_001_F_000RRef,
                            T2.Q_001_F_004RRef,
                            ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'}),
                            CAST(DATEDIFF(MONTH,DATEADD(DAY,1.0 - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'})) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,ISNULL(T2.Q_001_F_001_,{ts '2001-01-01 00:00:00'})) AS NUMERIC(4)) - 2000) - 2000,{ts '4000-01-01 00:00:00'}))),T2.Q_001_F_005_) AS NUMERIC(12))) T1
                    LEFT OUTER JOIN dbo._Reference16 T19
                    ON T1.Q_001_F_001RRef = T19._IDRRef
                    LEFT OUTER JOIN dbo._Reference93 T20
                    ON T1.Q_001_F_005RRef = T20._IDRRef
                    LEFT OUTER JOIN dbo._Reference122 T21
                    ON T19._Fld362RRef = T21._IDRRef
                    WHERE		(T1.Q_001_F_004_ >= 0) AND (CASE WHEN (T1.Q_001_F_000RRef = 0x00000000000000000000000000000000) THEN 0x963228632B0039644C534B49F4AFF61D ELSE T1.Q_001_F_000RRef END = 0x963228632B0039644C534B49F4AFF61D)
                    GROUP BY	T1.Q_001_F_001RRef,			
                                T19._Fld375,
                                T1.Q_001_F_005RRef,
                                CASE WHEN (T1.Q_001_F_004_ <= 3.0) THEN N'1. до 3-х месяцев' WHEN ((T1.Q_001_F_004_ > 3.0) AND (T1.Q_001_F_004_ <= 6.0)) THEN N'2. от 4-х до 6 месяцев' WHEN ((T1.Q_001_F_004_ > 6.0) AND (T1.Q_001_F_004_ <= 12.0)) THEN N'3. от 7-ми до 12 месяцев' WHEN ((T1.Q_001_F_004_ > 12.0) AND (T1.Q_001_F_004_ <= 24.0)) THEN N'4. от 13-ти до 24 месяцев' WHEN ((T1.Q_001_F_004_ > 24.0) AND (T1.Q_001_F_004_ <= 36.0)) THEN N'5. от 25-х до 36-ти месяцев' ELSE N'6. свыше 36-ти месяцев' END,
                                T21._Fld1519,
                                T1.Q_001_F_001RRef,
                                T19._Description,
                                T19._Description,
                                T1.Q_001_F_005RRef,
                                T20._Description,
                                T20._Description
                    HAVING (CAST(SUM(T1.Q_001_F_003_) AS NUMERIC(38, 8)) > 0.0)

                    SELECT SUM(DZ) as SUMM
                    FROM #VT

                    DROP TABLE #VT;
'''

# сумма оплат
sql_select2 = '''
                SET NOCOUNT ON;

                DECLARE @P1 DATETIME, @P2 DATETIME

                SET		@P1 = DATEADD(year, 2000, %s) --дата начала
                SET		@P2 = DATEADD(year, 2000, %s) --дата окончания

                select (CAST(SUM(Сумма) AS NUMERIC(38, 2))) as SUMM                    
                from 
                (

                    select Абонент, Сумма, Регистратор, УслугаНаселению, Подразделение
                    from dbo.РегистрНакопления_Авансы
                    where Регистратор_RTREF = 0x000000BE -- Документ.РегистрацияОплат
                    and ВидДвижения = 1 -- вид движения: расход
                    and Период between convert(datetime2, @P1) and convert(datetime2, @P2)

                    UNION ALL

                    select Абонент, Сумма, Регистратор, УслугаНаселению, Подразделение
                    from 
                    (
                        select dbo.РегистрНакопления_Авансы.Абонент as Абонент,
                            sum(case when ВидДвижения = 1 then Сумма else -Сумма end) as Сумма,
                            Регистратор,
                            УслугаНаселению,
                            dbo.РегистрНакопления_Авансы.Подразделение as Подразделение
                        from dbo.РегистрНакопления_Авансы
                        inner join dbo.Документ_РучнаяКорректировка on dbo.РегистрНакопления_Авансы.Регистратор = dbo.Документ_РучнаяКорректировка.Ссылка
                        where Регистратор_RTREF = 0x000000BF -- Документ.РучнаяКорректировка
                        and Период between convert(datetime2, @P1) and convert(datetime2, @P2)
                        and (dbo.Документ_РучнаяКорректировка.ВидКорректировки in (
                            select Ссылка from dbo.Перечисление_ВидыКорректировок where Наименование in (
                            'Неверно разнесенная сумма квитанции',
                            'Перенос квитанции с одного абонента на другого',
                            'Перенос с технического лицевого счета',
                            'Перенос квитанции на технический лицевой счет',
                            'Аннулирование корректировки оплаты',
                            'Ввод оплаты по служебной записке',
                            'Корректировка оплат', --Корректировка оплат до переноса
                            'Корректировка остатка квитанции')))
                        group by dbo.РегистрНакопления_Авансы.Абонент,
                                Регистратор,
                                УслугаНаселению,
                                dbo.РегистрНакопления_Авансы.Подразделение

                        UNION

                        select dbo.РегистрНакопления_Долги.Абонент as Абонент,
                            sum(case when ВидДвижения = 1 then Сумма else -Сумма end) as Сумма,
                            Регистратор,
                            УслугаНаселению,
                            dbo.РегистрНакопления_Долги.Подразделение as Подразделение
                        from dbo.РегистрНакопления_Долги
                        inner join dbo.Документ_РучнаяКорректировка on dbo.РегистрНакопления_Долги.Регистратор = dbo.Документ_РучнаяКорректировка.Ссылка
                        where Регистратор_RTREF = 0x000000BF -- Документ.РучнаяКорректировка
                        and Период between convert(datetime2, @P1) and convert(datetime2, @P2)
                        and (dbo.Документ_РучнаяКорректировка.ВидКорректировки in (
                            select Ссылка from dbo.Перечисление_ВидыКорректировок where Наименование in (
                            'Неверно разнесенная сумма квитанции',
                            'Перенос квитанции с одного абонента на другого',
                            'Перенос с технического лицевого счета',
                            'Перенос квитанции на технический лицевой счет',
                            'Аннулирование корректировки оплаты',
                            'Ввод оплаты по служебной записке',
                            'Корректировка оплат', --Корректировка оплат до переноса
                            'Корректировка остатка квитанции')))
                        group by dbo.РегистрНакопления_Долги.Абонент,
                                Регистратор,
                                УслугаНаселению,
                                dbo.РегистрНакопления_Долги.Подразделение
                    ) as КорректировкаОплаты

                    UNION ALL

                    select Абонент, Сумма, Регистратор, УслугаНаселению, Подразделение
                    from
                    (
                        select Абонент,
                            sum(case when ВидДвижения = 1 then Сумма else -Сумма end) as Сумма,
                            Регистратор,
                            УслугаНаселению,
                            Подразделение
                        from dbo.РегистрНакопления_Авансы
                        where Регистратор_RTREF = 0x00000098 -- Документ.ВозвратДенежныхСредств
                        and Период between convert(datetime2, @P1) and convert(datetime2, @P2)
                        group by dbo.РегистрНакопления_Авансы.Абонент,
                                Регистратор,
                                УслугаНаселению,
                                dbo.РегистрНакопления_Авансы.Подразделение
                                
                        UNION

                        select Абонент,
                            sum(Сумма) as Сумма,
                            Регистратор,
                            УслугаНаселению,
                            Подразделение
                        from dbo.РегистрНакопления_Долги
                        where Регистратор_RTREF = 0x00000098 -- Документ.ВозвратДенежныхСредств
                        and Период between convert(datetime2, @P1) and convert(datetime2, @P2)
                        and ВидДвижения = 1
                        group by Абонент,
                                Регистратор,
                                УслугаНаселению,
                                Подразделение 
                    ) as Возвраты
                    where Сумма <> 0
                ) as Отчет
'''

# фактические объемы
sql_select3 = '''
                SET NOCOUNT ON;

                DECLARE @P1 DATETIME, @P2 DATETIME

                SET		@P1 = DATEADD(year, 2000, %s) --дата начала
                SET		@P2 = DATEADD(year, 2000, %s) --дата окончания

                SELECT sum(T3.Сумма) as SUMM, sum(T3.Объем) as VOL, T3.РежимПотребления as RZ
                FROM (
                    SELECT
                    CASE WHEN (CASE WHEN (T1._Fld3696RRef = 0x908EC10B1C3D1CAF4F175961C4B99182) THEN 0x00 ELSE 0x01 END = 0x00) THEN T2._Description ELSE CASE WHEN (T1._Fld3696RRef IN (0x8C5B96FBF061972047A17A49866A5EC3, 0x870B8718B47C9827464053C1AD204DD4, 0xBADFC770117228CC473AD05D43C0B24F)) THEN 'Начисление при отсутсвии показаний' WHEN (T1._Fld3696RRef IN (0x823F72D3B3FA32414E85A0DEE38499A8, 0x905B77265CE961F74F381DC62E3411FD)) THEN 'Начисление по среднему' ELSE 'Начисление по показаниям' END END AS РежимПотребления,	
                    CAST(SUM(T1._Fld3681) AS NUMERIC(21, 3)) AS Объем,
                    CAST(SUM(T1._Fld3680) AS NUMERIC(21, 2)) AS Сумма,
                    T2._Fld1442RRef AS Услуга,
                    T1._Fld3695RRef AS Подразделение
                    FROM dbo._AccumRg3674 T1
                    LEFT OUTER JOIN dbo._Reference107 T2
                    ON T1._Fld3676RRef = T2._IDRRef	
                    WHERE ((T1._Period >= @P1) AND (T1._Period <= @P2)) AND T2._Fld1442RRef = 0x963228632B0039644C534B49F4AFF61D
                    GROUP BY T1._Fld3675RRef,
                    CASE WHEN (CASE WHEN (T1._Fld3696RRef = 0x908EC10B1C3D1CAF4F175961C4B99182) THEN 0x00 ELSE 0x01 END = 0x00) THEN T2._Description ELSE CASE WHEN (T1._Fld3696RRef IN (0x8C5B96FBF061972047A17A49866A5EC3, 0x870B8718B47C9827464053C1AD204DD4, 0xBADFC770117228CC473AD05D43C0B24F)) THEN 'Начисление при отсутсвии показаний' WHEN (T1._Fld3696RRef IN (0x823F72D3B3FA32414E85A0DEE38499A8, 0x905B77265CE961F74F381DC62E3411FD)) THEN 'Начисление по среднему' ELSE 'Начисление по показаниям' END END,
                    T2._Fld1442RRef,
                    T1._Fld3695RRef) AS T3
                GROUP BY T3.РежимПотребления    
'''

# данные по абонентам
# используется для заполнения таблицы "Данные по абонентам"
sql_select4 = '''
                SET NOCOUNT ON;
                
                DECLARE @P1 DATETIME

                SET		@P1 = DATEADD(year, 2000, %s) --период

                ----------------------------------------------------------------
                -------/////АБОНЕНТЫ С ИХ СОСТОЯНИЕМ ПОДКЛЮЧЕНИЯ//////----------
                ----------------------------------------------------------------
                select dbo.РегистрСведений_СостояниеПодключениеУслуг.Абонент as Абонент, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.СостояниеПодключения as СостояниеПодключения, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.НеПриниматьКУчету as НеПриниматьКУчету, 
                    ДатаРегистрацииИзменения, 
                    Период, 
                    dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Дата_Time as Дата_Time
                into #втНач
                from dbo.РегистрСведений_СостояниеПодключениеУслуг
                inner join dbo.Документ_ИзменениеСостоянияПодключенияАбонента on dbo.РегистрСведений_СостояниеПодключениеУслуг.Регистратор = dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Ссылка
                where dbo.РегистрСведений_СостояниеПодключениеУслуг.Период <= @P1
                and dbo.РегистрСведений_СостояниеПодключениеУслуг.УчетныйМесяц <= @P1
                ;
                
                with втДни2 as (
                select Абонент as AB, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач
                group by Абонент, Период)

                select Абонент as AB_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_
                into #втДни
                from #втНач 
                inner join втДни2 on #втНач.Период = втДни2.PER
                and #втНач.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач.Абонент = втДни2.AB
                group by Абонент, Период, ДатаРегистрацииИзменения 
                
                select Абонент, СостояниеПодключения, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time
                into #ПКУ_СостояниеПодключениеУслуг
                from #втНач
                inner join #втДни on #втНач.ДатаРегистрацииИзменения = #втДни.DRI_
                and #втНач.Период = #втДни.PER_
                and #втНач.Дата_Time = #втДни.REG_
                and #втНач.Абонент = #втДни.AB_
                where НеПриниматьКУчету = 0x00
                
                drop table #втНач;
                drop table #втДни;
                
                with МаксПериодРегистратор as (
                select Абонент as AB, max(Период) as PER
                from #ПКУ_СостояниеПодключениеУслуг
                group by Абонент
                )

                select Абонент, СостояниеПодключения
                into #СП_ПКУ_СостояниеПодключениеУслуг
                from #ПКУ_СостояниеПодключениеУслуг 
                inner join МаксПериодРегистратор on #ПКУ_СостояниеПодключениеУслуг.Абонент = МаксПериодРегистратор.AB 
                and #ПКУ_СостояниеПодключениеУслуг.Период = МаксПериодРегистратор.PER
                
                select count(#СП_ПКУ_СостояниеПодключениеУслуг.Абонент) as Количество,	   
                    case when dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00' then 'Открыт' else 'Закрыт' end as СостояниеЛС,
                    dbo.Перечисление_СостоянияПодключенияАбонента.Наименование as СостояниеПодключения	   
                from #СП_ПКУ_СостояниеПодключениеУслуг
                left join dbo.Справочник_Абоненты						on #СП_ПКУ_СостояниеПодключениеУслуг.Абонент = dbo.Справочник_Абоненты.Ссылка
                left join dbo.Перечисление_СостоянияПодключенияАбонента on #СП_ПКУ_СостояниеПодключениеУслуг.СостояниеПодключения = dbo.Перечисление_СостоянияПодключенияАбонента.Ссылка
                where dbo.Справочник_Абоненты.ЛицевойСчет is not Null
                group by case when dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00' then 'Открыт' else 'Закрыт' end,
                        dbo.Перечисление_СостоянияПодключенияАбонента.Наименование
                
                drop table #ПКУ_СостояниеПодключениеУслуг, #СП_ПКУ_СостояниеПодключениеУслуг;
'''

# данные по абонентам (фильтр по состоянию ЛС и фильтр по состоянию подключения)
# используется для заполнения таблицы абонентов 
sql_select5 = '''
 
                SET NOCOUNT ON;
                    
                DECLARE @P1 DATETIME, @P2 NVARCHAR(20), @P3 NVARCHAR(20), @P4 NVARCHAR(10)

                SET		@P1 = DATEADD(year, 2000, %s) 
                <доп переменная @P2>
                <доп переменная @P3>
                <доп переменная @P4>
                
                
                select dbo.РегистрСведений_СостояниеПодключениеУслуг.Абонент as Абонент, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.СостояниеПодключения as СостояниеПодключения, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.НеПриниматьКУчету as НеПриниматьКУчету, 
                    ДатаРегистрацииИзменения, 
                    Период, 
                    dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Дата_Time as Дата_Time
                into #втНач
                from dbo.РегистрСведений_СостояниеПодключениеУслуг
                inner join dbo.Документ_ИзменениеСостоянияПодключенияАбонента on dbo.РегистрСведений_СостояниеПодключениеУслуг.Регистратор = dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Ссылка
                <доп таблица спр.Абоненты>
                where dbo.РегистрСведений_СостояниеПодключениеУслуг.Период <= @P1
                and dbo.РегистрСведений_СостояниеПодключениеУслуг.УчетныйМесяц <= @P1
                <доп условие отбор ЛС>
                ;
                
                with втДни2 as (
                select Абонент as AB, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач
                group by Абонент, Период)

                select Абонент as AB_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_
                into #втДни
                from #втНач 
                inner join втДни2 on #втНач.Период = втДни2.PER
                and #втНач.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач.Абонент = втДни2.AB
                group by Абонент, Период, ДатаРегистрацииИзменения 
                
                select Абонент, СостояниеПодключения, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time
                into #ПКУ_СостояниеПодключениеУслуг
                from #втНач
                inner join #втДни on #втНач.ДатаРегистрацииИзменения = #втДни.DRI_
                and #втНач.Период = #втДни.PER_
                and #втНач.Дата_Time = #втДни.REG_
                and #втНач.Абонент = #втДни.AB_
                where НеПриниматьКУчету = 0x00
                
                drop table #втНач;
                drop table #втДни;
                
                with МаксПериодРегистратор as (
                select Абонент as AB, max(Период) as PER
                from #ПКУ_СостояниеПодключениеУслуг
                group by Абонент
                )

                select Абонент, СостояниеПодключения, Период
                into #СП_ПКУ_СостояниеПодключениеУслуг
                from #ПКУ_СостояниеПодключениеУслуг
                inner join МаксПериодРегистратор on #ПКУ_СостояниеПодключениеУслуг.Абонент = МаксПериодРегистратор.AB 
                and #ПКУ_СостояниеПодключениеУслуг.Период = МаксПериодРегистратор.PER
                                    
                                    
                select #СП_ПКУ_СостояниеПодключениеУслуг.Абонент as Абонент, 
                        #СП_ПКУ_СостояниеПодключениеУслуг.СостояниеПодключения as СостояниеПодключения, 
                        #СП_ПКУ_СостояниеПодключениеУслуг.Период as Период, 
                        T6.ФизЛицо as ФизЛицо
                into #Итоговая
                from #СП_ПКУ_СостояниеПодключениеУслуг 
                left join (
                    select dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент, dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.ФизЛицо
                    from dbo.Документ_ИзменениеСвязиФизЛицаИАбонента
                    inner join (
                        select dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент, dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Дата_Time, MAX(dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Номер) as Номер
                        from dbo.Документ_ИзменениеСвязиФизЛицаИАбонента
                        inner join (
                            select MAX(dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Дата_Time) as Дата_Time, dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент as Абонент
                            from dbo.Документ_ИзменениеСвязиФизЛицаИАбонента
                            where dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент in (select Абонент from #СП_ПКУ_СостояниеПодключениеУслуг group by Абонент)
                            group by dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент) as T4 on dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Дата_Time = T4.Дата_Time and dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент = T4.Абонент
                        group by dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент, dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Дата_Time) as T5 on dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Номер = T5.Номер and dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Абонент = T5.Абонент
                        and dbo.Документ_ИзменениеСвязиФизЛицаИАбонента.Дата_Time = T5.Дата_Time
                ) as T6 on #СП_ПКУ_СостояниеПодключениеУслуг.Абонент = T6.Абонент
                group by #СП_ПКУ_СостояниеПодключениеУслуг.Абонент, #СП_ПКУ_СостояниеПодключениеУслуг.СостояниеПодключения, #СП_ПКУ_СостояниеПодключениеУслуг.Период, T6.ФизЛицо                    
                
                
                select  dbo.Справочник_Абоненты.Наименование as ФИО,	
                        dbo.Справочник_Абоненты.ЛицевойСчет as ЛС,
                        dbo.Справочник_Абоненты.Адрес as Адрес,
                        case when dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00' then 'on' else 'off' end as СостояниеЛС,
                        dbo.Перечисление_СостоянияПодключенияАбонента.Наименование as СостояниеПодключения,                            
                        replace(replace(convert(varchar, case when dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00' then dbo.Справочник_Абоненты.ДатаОткрытия else dbo.Справочник_Абоненты.ДатаЗакрытия end, 104), '.4', '.2'), '.3', '.1') as ДатаОткрытияЗакрытия,
                        replace(replace(convert(varchar, Период, 104), '.4', '.2'), '.3', '.1') as ДатаПодключенияОтключения,
                        T7.ДокументВид as ВидДокумента,
                        T7.ДокументНомер as НомерДокумента,
                        T7.ДокументСерия as СерияДокумента,
                        replace(replace(convert(varchar, T7.ДокументДатаВыдачи, 104), '.4', '.2'), '.3', '.1') as ДатаВыдачиДокумента,
                        T7.ДокументКемВыдан as КемВыданДокумент
                from #Итоговая
                left join dbo.Справочник_Абоненты						on #Итоговая.Абонент = dbo.Справочник_Абоненты.Ссылка
                left join dbo.Перечисление_СостоянияПодключенияАбонента on #Итоговая.СостояниеПодключения = dbo.Перечисление_СостоянияПодключенияАбонента.Ссылка
                left join (
                    select dbo.РегистрСведений_ПаспортныеДанныеФизЛиц.ФизЛицо, dbo.Справочник_ДокументыУдостоверяющиеЛичность.Наименование as ДокументВид, ДокументСерия, ДокументНомер, ДокументДатаВыдачи, ДокументКемВыдан
                    from dbo.РегистрСведений_ПаспортныеДанныеФизЛиц
                    inner join (	
                            select max(Период) as Период, ФизЛицо
                            from dbo.РегистрСведений_ПаспортныеДанныеФизЛиц
                            where ФизЛицо in (select ФизЛицо from #Итоговая group by ФизЛицо)
                            group by ФизЛицо
                        ) as T6 on dbo.РегистрСведений_ПаспортныеДанныеФизЛиц.Период = T6.Период and dbo.РегистрСведений_ПаспортныеДанныеФизЛиц.ФизЛицо = T6.ФизЛицо
                        inner join dbo.Справочник_ДокументыУдостоверяющиеЛичность on dbo.РегистрСведений_ПаспортныеДанныеФизЛиц.ДокументВид = dbo.Справочник_ДокументыУдостоверяющиеЛичность.Ссылка
                    ) as T7 on #Итоговая.ФизЛицо = T7.ФизЛицо
                where dbo.Справочник_Абоненты.ЛицевойСчет is not Null                    
                <доп условие открыт/закрыт>
                <доп условие подключен/отключен>

                drop table #ПКУ_СостояниеПодключениеУслуг, #СП_ПКУ_СостояниеПодключениеУслуг, #Итоговая;
'''

# данные по абоненту (установленное оборудование)
# используется для получения данных по абоненту при нажатии на поле в таблице абонентов
sql_select6 = '''
                SET NOCOUNT ON;

                DECLARE @P1 DATETIME, @P2 NVARCHAR(20)

                SET		@P1 = DATEADD(year, 2000, %s)
                SET		@P2 = %s                

                select dbo.РегистрСведений_УстановленноеОборудование.Абонент as Абонент, 
                    Оборудование, 
                    dbo.РегистрСведений_УстановленноеОборудование.УзелУчета as УзелУчета, 
                    Действует,
                    НеПриниматьКУчету,
                    ДатаРегистрацииИзменения,		
                    Период,
                    dbo.Документ_ИзменениеПараметровОборудования.Дата_Time as Дата_Time
                into #втНач
                from dbo.РегистрСведений_УстановленноеОборудование
                inner join dbo.Справочник_Оборудование					on dbo.РегистрСведений_УстановленноеОборудование.Оборудование = dbo.Справочник_Оборудование.Ссылка
                inner join dbo.Документ_ИзменениеПараметровОборудования on dbo.РегистрСведений_УстановленноеОборудование.Регистратор = dbo.Документ_ИзменениеПараметровОборудования.Ссылка
                inner join dbo.Справочник_Абоненты						on dbo.РегистрСведений_УстановленноеОборудование.Абонент = dbo.Справочник_Абоненты.Ссылка
                where dbo.Документ_ИзменениеПараметровОборудования.Дата_Time <= @P1
                and dbo.РегистрСведений_УстановленноеОборудование.Период <= @P1
                and dbo.РегистрСведений_УстановленноеОборудование.УчетныйМесяц <= @P1
                and dbo.Справочник_Абоненты.ЛицевойСчет = @P2
                ;

                with втДни2 as (
                select Абонент as AB, Оборудование as OB, УзелУчета as UZ, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач
                group by Абонент, Оборудование, УзелУчета, Период)

                select Абонент as AB_, Оборудование as OB_, УзелУчета as UZ_, max(Дата_Time) as Дата_Time_, Период as PER_, ДатаРегистрацииИзменения as DRI_ 
                into #втДни 
                from #втНач
                inner join втДни2 on #втНач.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач.Период = втДни2.PER
                and #втНач.Абонент = втДни2.AB
                and #втНач.Оборудование = втДни2.OB
                and #втНач.УзелУчета = втДни2.UZ
                group by Абонент, Оборудование, УзелУчета, Период, ДатаРегистрацииИзменения 
                

                select Абонент, Оборудование, УзелУчета, Действует, ДатаРегистрацииИзменения, Период, Период as ДеньПериода, Дата_Time
                into #ПКУ_УстановленноеОборудование
                from #втНач
                inner join #втДни on #втНач.ДатаРегистрацииИзменения = #втДни.DRI_
                and #втНач.Период = #втДни.PER_
                and #втНач.Дата_Time = #втДни.Дата_Time_
                and #втНач.Абонент = #втДни.AB_
                and #втНач.Оборудование = #втДни.OB_
                and #втНач.УзелУчета = #втДни.UZ_
                where #втНач.НеПриниматьКУчету = 0x00
                

                drop table #втНач;
                drop table #втДни;
                

                with МаксПериод as (
                select Абонент as AB, Оборудование as OB, УзелУчета as UZ, max(Период) as PER
                from #ПКУ_УстановленноеОборудование
                group by Абонент, Оборудование, УзелУчета
                )

                select #ПКУ_УстановленноеОборудование.Абонент as Абонент, ДеньПериода, Оборудование
                into #АбонентыСоСчетчиком
                from #ПКУ_УстановленноеОборудование
                inner join МаксПериод on #ПКУ_УстановленноеОборудование.Абонент = МаксПериод.AB
                and #ПКУ_УстановленноеОборудование.Оборудование = МаксПериод.OB
                and #ПКУ_УстановленноеОборудование.УзелУчета = МаксПериод.UZ
                and #ПКУ_УстановленноеОборудование.Период = МаксПериод.PER
                where #ПКУ_УстановленноеОборудование.Действует = 0x01
                group by Абонент, ДеньПериода, Оборудование
                

                drop table #ПКУ_УстановленноеОборудование;
                
                -------------СЧЕТЧИКИ С ИХ СОСТОЯНИЕМ---------------------------
                select Объект, Идентификатор, Значение, Значение_T, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, dbo.Документ_ИзменениеПараметровОборудования.Дата_Time as Дата_Time 
                into #втНач1
                from dbo.РегистрСведений_ПараметрыОборудования
                inner join dbo.Документ_ИзменениеПараметровОборудования on dbo.РегистрСведений_ПараметрыОборудования.Регистратор = dbo.Документ_ИзменениеПараметровОборудования.Ссылка
                inner join dbo.Справочник_Оборудование on dbo.РегистрСведений_ПараметрыОборудования.Объект = dbo.Справочник_Оборудование.Ссылка
                where (Идентификатор = 0xAD444FEC06ECBF9A4153E86202DE5D80 -- идентификатор "Состояние"
                        or Идентификатор = 0x967172FDBCB421E54F221AF09B962931 -- Дата последней поверки
                        or Идентификатор = 0xBD43D8B3863DF5E54747593F7762F53A) -- Дата очередной поверки
                and dbo.РегистрСведений_ПараметрыОборудования.Период <= @P1
                and dbo.РегистрСведений_ПараметрыОборудования.УчетныйМесяц <= @P1
                and dbo.Документ_ИзменениеПараметровОборудования.Дата_Time <= @P1
                and Объект in (select Оборудование from #АбонентыСоСчетчиком)
                ;


                with втДни2 as (
                select Объект as OB, Идентификатор as ID, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач1
                group by Объект, Идентификатор, Период
                )

                select Объект as OB_, Идентификатор as ID_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_
                into #втДни1
                from #втНач1
                inner join втДни2 on #втНач1.Период = втДни2.PER
                and #втНач1.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач1.Объект = втДни2.OB
                and #втНач1.Идентификатор = втДни2.ID
                group by Объект, Идентификатор, Период, ДатаРегистрацииИзменения
                

                select Объект, Идентификатор, Значение, Значение_T, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time, Период as ПериодДень
                into #ПКУ_ПараметрыОборудования
                from #втНач1
                inner join #втДни1 on #втНач1.ДатаРегистрацииИзменения = #втДни1.DRI_
                and #втНач1.Период = #втДни1.PER_
                and #втНач1.Дата_Time = #втДни1.REG_
                and #втНач1.Объект = #втДни1.OB_
                and #втНач1.Идентификатор = #втДни1.ID_
                where НеПриниматьКУчету = 0x00 
                

                drop table #втНач1;
                drop table #втДни1;
                

                with МаксПериод as (
                select Объект as OB_, Идентификатор as ID_, max(Период) as PER_
                from #ПКУ_ПараметрыОборудования
                group by Объект, Идентификатор)

                select Объект, Идентификатор, Значение, Значение_T, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time, Период as ПериодДень
                into #СП_ПКУ_ПараметрыОборудования
                from #ПКУ_ПараметрыОборудования
                inner join МаксПериод on #ПКУ_ПараметрыОборудования.Объект = МаксПериод.OB_
                and #ПКУ_ПараметрыОборудования.Идентификатор = МаксПериод.ID_
                and #ПКУ_ПараметрыОборудования.Период = МаксПериод.PER_
                order by Объект
                

                drop table #ПКУ_ПараметрыОборудования;
                

                ---------------ПОКАЗАНИЯ СЧЕТЧИКА---------------------------
                select Оборудование, Значение, ДатаРегистрацииИзменения, ИсточникПоказания, НеПриниматьКУчету, Перекрут, Период, dbo.Документ_ВводПоказанийСчетчиков.Дата_Time as Дата_Time 
                into #втНач2
                from dbo.РегистрСведений_ПоказанияСчетчиков
                inner join dbo.Документ_ВводПоказанийСчетчиков on dbo.РегистрСведений_ПоказанияСчетчиков.Регистратор = dbo.Документ_ВводПоказанийСчетчиков.Ссылка
                where dbo.РегистрСведений_ПоказанияСчетчиков.Период <= @P1
                and dbo.РегистрСведений_ПоказанияСчетчиков.УчетныйМесяц <= @P1
                and dbo.Документ_ВводПоказанийСчетчиков.Дата_Time <= @P1
                and Оборудование in (select Оборудование from #АбонентыСоСчетчиком)
                ;

                with втДни2 as (
                select Оборудование as OB, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач2
                group by Оборудование, Период
                )

                select Оборудование as OB_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_
                into #втДни2
                from #втНач2
                inner join втДни2 on #втНач2.Период = втДни2.PER
                and #втНач2.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач2.Оборудование = втДни2.OB
                group by Оборудование, Период, ДатаРегистрацииИзменения

                
                select Оборудование, Значение, ДатаРегистрацииИзменения, ИсточникПоказания, НеПриниматьКУчету, Перекрут, Период, Дата_Time 
                into #ПКУ_ПоказанияСчетчиков
                from #втНач2
                inner join #втДни2 on #втНач2.ДатаРегистрацииИзменения = #втДни2.DRI_
                and #втНач2.Период = #втДни2.PER_
                and #втНач2.Дата_Time = #втДни2.REG_
                and #втНач2.Оборудование = #втДни2.OB_
                where НеПриниматьКУчету = 0x00                

                drop table #втНач2;
                drop table #втДни2;


                with МаксПериод as (
                select Оборудование as OB_, max(Период) as PER_
                from #ПКУ_ПоказанияСчетчиков
                group by Оборудование)

                select Оборудование, Значение as Показания, Период
                into #СП_ПКУ_ПоказанияСчетчиков
                from #ПКУ_ПоказанияСчетчиков
                inner join МаксПериод on #ПКУ_ПоказанияСчетчиков.Оборудование = МаксПериод.OB_
                and #ПКУ_ПоказанияСчетчиков.Период = МаксПериод.PER_
                order by Оборудование


                drop table #ПКУ_ПоказанияСчетчиков;
                
                --------------------------------------------------
                --------------------------------------------------                
                --0x811B2BFF0371062B4C92255B3266E02D - вид Адрес
                --0x8DF1D2DBAB354CD441306966C04F98F5 - тип Адрес
                --0x985D216B1D88DAA94A92E835D8156621 - тип Телефон

                select #АбонентыСоСчетчиком.Абонент as Абонент,
                    #АбонентыСоСчетчиком.Оборудование as Оборудование,
                    T1.СостояниеРаботы as СостояниеРаботы,
                    T2.ДатаПоследнейПоверки as ДатаПоследнейПоверки,
                    T3.ДатаОчереднойПоверки as ДатаОчереднойПоверки,
                    #СП_ПКУ_ПоказанияСчетчиков.Показания as Показания,
                    #СП_ПКУ_ПоказанияСчетчиков.Период as ПериодПоказаний                    
                into #Итоговая
                from #АбонентыСоСчетчиком
                left join #СП_ПКУ_ПоказанияСчетчиков on #АбонентыСоСчетчиком.Оборудование = #СП_ПКУ_ПоказанияСчетчиков.Оборудование
                left join (
                    select Объект, 
                    case when Идентификатор = 0xAD444FEC06ECBF9A4153E86202DE5D80 then Значение end as СостояниеРаботы	
                    from #СП_ПКУ_ПараметрыОборудования
                    where case when Идентификатор = 0xAD444FEC06ECBF9A4153E86202DE5D80 then Значение end is not Null
                ) as T1 on #АбонентыСоСчетчиком.Оборудование = T1.Объект
                left join (
                    select Объект, 
                    case when Идентификатор = 0x967172FDBCB421E54F221AF09B962931 then Значение_T end as ДатаПоследнейПоверки	
                    from #СП_ПКУ_ПараметрыОборудования
                    where case when Идентификатор = 0x967172FDBCB421E54F221AF09B962931 then Значение_T end is not Null
                ) as T2 on #АбонентыСоСчетчиком.Оборудование = T2.Объект
                left join (
                    select Объект, 
                    case when Идентификатор = 0xBD43D8B3863DF5E54747593F7762F53A then Значение_T end as ДатаОчереднойПоверки	
                    from #СП_ПКУ_ПараметрыОборудования
                    where case when Идентификатор = 0xBD43D8B3863DF5E54747593F7762F53A then Значение_T end is not Null
                ) as T3 on #АбонентыСоСчетчиком.Оборудование = T3.Объект                
                group by #АбонентыСоСчетчиком.Абонент, 
                        #АбонентыСоСчетчиком.Оборудование, 
                        T1.СостояниеРаботы,
                        T2.ДатаПоследнейПоверки,
                        T3.ДатаОчереднойПоверки,
                        #СП_ПКУ_ПоказанияСчетчиков.Показания,
                        #СП_ПКУ_ПоказанияСчетчиков.Период

                
                select dbo.Справочник_Абоненты.Наименование as Абонент,
                    dbo.Справочник_Оборудование.Наименование as Оборудование,	   
                    dbo.Справочник_ТипыОборудования.Наименование as ТипОборудования,
                    dbo.Справочник_СостоянияОборудования.Наименование as СостояниеОборудования,	   
                    replace(replace(convert(varchar, #Итоговая.ДатаПоследнейПоверки, 104), '.4', '.2'), '.3', '.1') as ДатаПоследнейПоверки,
                    replace(replace(convert(varchar, #Итоговая.ДатаОчереднойПоверки, 104), '.4', '.2'), '.3', '.1') as ДатаОчереднойПоверки,
                    #Итоговая.Показания as Показания,
                    replace(replace(convert(varchar, #Итоговая.ПериодПоказаний, 104), '.4', '.2'), '.3', '.1') as ПериодПоказаний
                from #Итоговая
                left join dbo.Справочник_Абоненты			   on #Итоговая.Абонент							= dbo.Справочник_Абоненты.Ссылка
                left join dbo.Справочник_Оборудование		   on #Итоговая.Оборудование					= dbo.Справочник_Оборудование.Ссылка
                left join dbo.Справочник_ВидыОборудования	   on dbo.Справочник_Оборудование.Вид			= dbo.Справочник_ВидыОборудования.Ссылка
                left join dbo.Справочник_ТипыОборудования	   on dbo.Справочник_ВидыОборудования.Владелец	= dbo.Справочник_ТипыОборудования.Ссылка
                left join dbo.Справочник_СостоянияОборудования on #Итоговая.СостояниеРаботы					= dbo.Справочник_СостоянияОборудования.Ссылка                
                
                drop table #АбонентыСоСчетчиком, #СП_ПКУ_ПараметрыОборудования, #СП_ПКУ_ПоказанияСчетчиков, #Итоговая;                
'''

# данные по неправильным лицевым номерам
sql_select7 = '''
                SET NOCOUNT ON;


                select ЛицевойСчет as ЛС, dbo.Справочник_Абоненты.Наименование as ФИО
                from dbo.Справочник_Абоненты
                left join dbo.Справочник_Подразделения on dbo.Справочник_Абоненты.Подразделения = dbo.Справочник_Подразделения.Ссылка
                where	substring(dbo.Справочник_Абоненты.ЛицевойСчет, 0, 4) <> Префикс 
                        and dbo.Справочник_Абоненты.ПометкаУдаления = 0x00
                        --and ЛицевойСчет <> '030000001'
                order by ЛицевойСчет
'''

# данные по незаполненным ГРС
sql_select8 = '''
                SET NOCOUNT ON;


                ----------------------------------------------------------------
                -------/////АБОНЕНТЫ С ИХ СОСТОЯНИЕМ ПОДКЛЮЧЕНИЯ//////----------
                ----------------------------------------------------------------
                select dbo.РегистрСведений_СостояниеПодключениеУслуг.Абонент as Абонент, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.СостояниеПодключения as СостояниеПодключения, 
                    dbo.РегистрСведений_СостояниеПодключениеУслуг.НеПриниматьКУчету as НеПриниматьКУчету, 
                    ДатаРегистрацииИзменения, 
                    Период, 
                    dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Дата_Time as Дата_Time
                into #втНач
                from dbo.РегистрСведений_СостояниеПодключениеУслуг
                inner join dbo.Документ_ИзменениеСостоянияПодключенияАбонента on dbo.РегистрСведений_СостояниеПодключениеУслуг.Регистратор = dbo.Документ_ИзменениеСостоянияПодключенияАбонента.Ссылка
                where dbo.РегистрСведений_СостояниеПодключениеУслуг.Период <= DATEADD(YEAR, 2000, GETDATE())
                and dbo.РегистрСведений_СостояниеПодключениеУслуг.УчетныйМесяц <= DATEADD(YEAR, 2000, GETDATE())
                ;


                with втДни2 as (
                select Абонент as AB, Период as PER, max(ДатаРегистрацииИзменения) as DRI
                from #втНач
                group by Абонент, Период)

                select Абонент as AB_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_
                into #втДни
                from #втНач 
                inner join втДни2 on #втНач.Период = втДни2.PER
                and #втНач.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач.Абонент = втДни2.AB
                group by Абонент, Период, ДатаРегистрацииИзменения 
                

                select Абонент, СостояниеПодключения, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time
                into #ПКУ_СостояниеПодключениеУслуг
                from #втНач
                inner join #втДни on #втНач.ДатаРегистрацииИзменения = #втДни.DRI_
                and #втНач.Период = #втДни.PER_
                and #втНач.Дата_Time = #втДни.REG_
                and #втНач.Абонент = #втДни.AB_
                where НеПриниматьКУчету = 0x00
                

                drop table #втНач;
                drop table #втДни;
                

                with МаксПериодРегистратор as (
                select Абонент as AB, max(Период) as PER
                from #ПКУ_СостояниеПодключениеУслуг
                group by Абонент
                )

                select Абонент, СостояниеПодключения
                into #СП_ПКУ_СостояниеПодключениеУслуг
                from #ПКУ_СостояниеПодключениеУслуг 
                inner join МаксПериодРегистратор on #ПКУ_СостояниеПодключениеУслуг.Абонент = МаксПериодРегистратор.AB 
                and #ПКУ_СостояниеПодключениеУслуг.Период = МаксПериодРегистратор.PER
                

                select replace(dbo.Справочник_ЗданияИСооружения.Наименование, ', Липецкая обл,', ',') as АдресЗдания
                from dbo.Справочник_Абоненты
                left join dbo.Справочник_ЗданияИСооружения_РаспределительныеСтанции on dbo.Справочник_Абоненты.Здание = dbo.Справочник_ЗданияИСооружения_РаспределительныеСтанции.Ссылка
                inner join dbo.Справочник_ЗданияИСооружения on dbo.Справочник_Абоненты.Здание = dbo.Справочник_ЗданияИСооружения.Ссылка
                where dbo.Справочник_Абоненты.Ссылка in (select Абонент
                                                        from #СП_ПКУ_СостояниеПодключениеУслуг
                                                        inner join dbo.Справочник_Абоненты on #СП_ПКУ_СостояниеПодключениеУслуг.Абонент = dbo.Справочник_Абоненты.Ссылка
                                                        where СостояниеПодключения = 0xB58B0B6E7D2B79C0452C6BB031E5CCE7
                                                        and dbo.Справочник_Абоненты.ДатаЗакрытия = '2001-01-01 00:00:00')
                and (dbo.Справочник_ЗданияИСооружения_РаспределительныеСтанции.РаспределительнаяСтанция is Null or dbo.Справочник_ЗданияИСооружения_РаспределительныеСтанции.РаспределительнаяСтанция = 0x00000000000000000000000000000000)
                group by dbo.Справочник_ЗданияИСооружения.Наименование, dbo.Справочник_ЗданияИСооружения.НаселенныйПункт
                order by dbo.Справочник_ЗданияИСооружения.НаселенныйПункт
                

                drop table #ПКУ_СостояниеПодключениеУслуг, #СП_ПКУ_СостояниеПодключениеУслуг;
'''

# данные по установленным режимам редактирования у пользователей
sql_select9 = '''
                SET NOCOUNT ON;

                select dbo.Справочник_Пользователи.Наименование as username, dbo.ПланВидовХарактеристик_НастройкиПользователей.Наименование as sett, Значение_L as res
                from dbo.РегистрСведений_НастройкиПользователей
                inner join dbo.Справочник_Пользователи on dbo.РегистрСведений_НастройкиПользователей.Пользователь = dbo.Справочник_Пользователи.Ссылка
                inner join dbo.ПланВидовХарактеристик_НастройкиПользователей on dbo.РегистрСведений_НастройкиПользователей.Настройка = dbo.ПланВидовХарактеристик_НастройкиПользователей.Ссылка
                where Настройка = 0xB08FABBB26672A9248C34E140B5DBA9D --режим исправления ошибок
                order by dbo.Справочник_Пользователи.Наименование
'''

# получение сравнение количества проведнных документов начисления/льгот с их общим количеством за определенный учетный месяц
sql_select10 = '''
                DECLARE @date DATETIME2, @string1 NVARCHAR(200), @string2 NVARCHAR(200)

                SET @date = %s
                SET @string1 = %s
                SET @string2 = %s

                SELECT CASE WHEN (CASE WHEN T1.c1 = T2.c2 THEN 1 ELSE 0 END) = (CASE WHEN T3.c3 = T4.c4 THEN 1 ELSE 0 END) THEN 1 ELSE 0 END AS STATUS
                FROM (
                        SELECT Count(_IDRRef) AS c1
                        FROM dbo._Document177 
                        WHERE dbo._Document177._Fld2112 = @date
                        AND (dbo._Document177._Fld2115 = @string1 OR dbo._Document177._Fld2115 = @string2)) AS T1, 
                    (
                        SELECT Count(_IDRRef) AS c2
                        FROM dbo._Document177
                        WHERE dbo._Document177._Fld2112 = @date
                        AND dbo._Document177._Posted = 0x01) AS T2,
                    (
                        SELECT Count(_IDRRef) AS c3
                        FROM dbo._Document188 
                        WHERE dbo._Document188._Fld2239 = @date
                        AND (dbo._Document188._Fld2242 = @string1 OR dbo._Document188._Fld2242 = @string2)) AS T3, 
                    (
                        SELECT Count(_IDRRef) AS c4
                        FROM dbo._Document188
                        WHERE dbo._Document188._Fld2239 = @date
                        AND dbo._Document188._Posted = 0x01) AS T4
''' 

# абонентские параметры для расчета
sql_select11 = '''
                SET NOCOUNT ON;
                
                DECLARE @P1 DATETIME, @P2 NVARCHAR(20)

                SET	 @P1 = DATEADD(year, 2000, %s)
                SET	 @P2 = %s


                select dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Объект as Абонент, 
                    dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Параметр as Параметр, 
                    dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.УзелУчета as УзелУчета,
                    dbo.Справочник_ВидыДоговоров.Наименование as Значение,
                    dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Значение_N as Значение_N,
                    dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Значение_L as Значение_L,
                    dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.НеПриниматьКУчету as НеПриниматьКУчету, 
                    ДатаРегистрацииИзменения, 
                    Период, 
                    dbo.Документ_ИзменениеПараметровАбонентовДляРасчета.Дата_Time as Дата_Time, 
                    dbo.Справочник_Абоненты.Наименование as ФИО,
                    dbo.ПланВидовХарактеристик_ПараметрыАбонентовДляРасчета.Наименование as Параметры
                into #втНач
                from dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета
                inner join dbo.Документ_ИзменениеПараметровАбонентовДляРасчета on dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Регистратор = dbo.Документ_ИзменениеПараметровАбонентовДляРасчета.Ссылка
                inner join dbo.Справочник_Абоненты on dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Объект = dbo.Справочник_Абоненты.Ссылка
                inner join dbo.ПланВидовХарактеристик_ПараметрыАбонентовДляРасчета on dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Параметр = dbo.ПланВидовХарактеристик_ПараметрыАбонентовДляРасчета.Ссылка
                left join dbo.Справочник_ВидыДоговоров on dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Значение = dbo.Справочник_ВидыДоговоров.Ссылка
                where dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.Период <= @P1
                and dbo.РегистрСведений_ЗначенияПараметровАбонентовДляРасчета.УчетныйМесяц <= @P1
                and dbo.Справочник_Абоненты.ЛицевойСчет = @P2
                ;

                with втДни2 as (
                select Абонент as AB, Период as PER, max(ДатаРегистрацииИзменения) as DRI, Параметр as PARAMETR, УзелУчета as UU
                from #втНач
                group by Абонент, Период, Параметр, УзелУчета)

                select Абонент as AB_, max(Дата_Time) as REG_, Период as PER_, ДатаРегистрацииИзменения as DRI_, Параметр as PARAMETR_, УзелУчета as UU_ 
                into #втДни
                from #втНач 
                inner join втДни2 on #втНач.Период = втДни2.PER
                and #втНач.ДатаРегистрацииИзменения = втДни2.DRI
                and #втНач.Абонент = втДни2.AB
                and #втНач.Параметр = втДни2.PARAMETR
                and #втНач.УзелУчета = втДни2.UU
                group by Абонент, Период, ДатаРегистрацииИзменения, Параметр, УзелУчета
                

                select Абонент, Параметр, НеПриниматьКУчету, ДатаРегистрацииИзменения, Период, Дата_Time, УзелУчета, Значение, Значение_N, Значение_L, ФИО, Параметры
                into #ПКУ_ЗначенияПараметровАбонентовДляРасчета
                from #втНач
                inner join #втДни on #втНач.ДатаРегистрацииИзменения = #втДни.DRI_
                and #втНач.Период = #втДни.PER_
                and #втНач.Дата_Time = #втДни.REG_
                and #втНач.Абонент = #втДни.AB_
                and #втНач.Параметр = #втДни.PARAMETR_
                and #втНач.УзелУчета = #втДни.UU_
                where НеПриниматьКУчету = 0x00

                drop table #втНач;
                drop table #втДни;

                with МаксПериодРегистратор as (
                select Абонент as AB, max(Период) as PER, Параметр as PARAMETR, УзелУчета as UU
                from #ПКУ_ЗначенияПараметровАбонентовДляРасчета
                group by Абонент, Параметр, УзелУчета
                )

                select Параметры, 
                case
                    when Параметры = 'Количество собственников' then STR(Значение_N, 6, 2)
                    when Параметры = 'Наличие горячего водоснабжения' then case when Значение_L = 0x00 then 'Нет' else 'Да' end
                    when Параметры = 'Количество проживающих' then STR(Значение_N, 6, 2)
                    when Параметры = 'Вид договора' then case when Значение is Null then '' else Значение end
                    when Параметры = 'Площадь жилая' then STR(Значение_N, 6, 2)
                    when Параметры = 'Доля собственности' then STR(Значение_N, 6, 2)
                end as Значения
                from #ПКУ_ЗначенияПараметровАбонентовДляРасчета 
                inner join МаксПериодРегистратор on #ПКУ_ЗначенияПараметровАбонентовДляРасчета.Абонент = МаксПериодРегистратор.AB 
                and #ПКУ_ЗначенияПараметровАбонентовДляРасчета.Параметр = МаксПериодРегистратор.PARAMETR
                and #ПКУ_ЗначенияПараметровАбонентовДляРасчета.УзелУчета = МаксПериодРегистратор.UU
                and #ПКУ_ЗначенияПараметровАбонентовДляРасчета.Период = МаксПериодРегистратор.PER


                drop table #ПКУ_ЗначенияПараметровАбонентовДляРасчета;
'''

# режимы потребления абонента
sql_select12 = '''
                SET NOCOUNT ON;
                                
                DECLARE @P1 DATETIME, @P2 NVARCHAR(20)

                SET		@P1 = DATEADD(year, 2000, %s)
                SET		@P2 = %s

                select dbo.РегистрСведений_РежимыПотребленияАбонентов.Абонент as Абонент,
                    dbo.РегистрСведений_РежимыПотребленияАбонентов.РежимПотребления as РежимПотребления,
                    dbo.РегистрСведений_РежимыПотребленияАбонентов.Поставщик as Поставщик,
                    dbo.РегистрСведений_РежимыПотребленияАбонентов.УзелУчета as УзелУчета,    
                    dbo.РегистрСведений_РежимыПотребленияАбонентов.НеПриниматьКУчету as НеПриниматьКУчету,
                    Действует,
                    Оборудование,
                    ДатаНачалаДействия,
                    ДатаОкончанияДействия,
                    ДатаРегистрацииИзменения,
                    Период,
                    case when dbo.Документ_ИзменениеРежимовПотребленияАбонентов.Дата_Time is null then dbo.Документ_КорректировкаЗаписейРегистровНакопления.Дата_Time else dbo.Документ_ИзменениеРежимовПотребленияАбонентов.Дата_Time end as Дата_Time
                into #втНачРежимыПотребленияАбонентовПред
                from dbo.РегистрСведений_РежимыПотребленияАбонентов
                left join dbo.Документ_ИзменениеРежимовПотребленияАбонентов on dbo.РегистрСведений_РежимыПотребленияАбонентов.Регистратор = dbo.Документ_ИзменениеРежимовПотребленияАбонентов.Ссылка
                left join dbo.Документ_КорректировкаЗаписейРегистровНакопления on dbo.РегистрСведений_РежимыПотребленияАбонентов.Регистратор = dbo.Документ_КорректировкаЗаписейРегистровНакопления.Ссылка
                inner join dbo.Справочник_Абоненты on dbo.РегистрСведений_РежимыПотребленияАбонентов.Абонент = dbo.Справочник_Абоненты.Ссылка
                where dbo.РегистрСведений_РежимыПотребленияАбонентов.Период <= @P1
                and dbo.РегистрСведений_РежимыПотребленияАбонентов.УчетныйМесяц <= @P1
                and dbo.Справочник_Абоненты.ЛицевойСчет = @P2


                select Период, Абонент, РежимПотребления, Поставщик, УзелУчета, max(ДатаРегистрацииИзменения) as ДатаРегистрацииИзменения
                into #втМаксДатаРегистрацииРежимыПотребленияАбонентов
                from #втНачРежимыПотребленияАбонентовПред
                group by Период, Абонент, РежимПотребления, Поставщик, УзелУчета


                select #втНачРежимыПотребленияАбонентовПред.Период, 
                    #втНачРежимыПотребленияАбонентовПред.Дата_Time,
                    #втНачРежимыПотребленияАбонентовПред.ДатаРегистрацииИзменения,
                    #втНачРежимыПотребленияАбонентовПред.Абонент,
                    #втНачРежимыПотребленияАбонентовПред.РежимПотребления,
                    #втНачРежимыПотребленияАбонентовПред.Поставщик,
                    #втНачРежимыПотребленияАбонентовПред.УзелУчета,
                    #втНачРежимыПотребленияАбонентовПред.Действует,
                    #втНачРежимыПотребленияАбонентовПред.Оборудование,
                    #втНачРежимыПотребленияАбонентовПред.ДатаНачалаДействия,
                    #втНачРежимыПотребленияАбонентовПред.ДатаОкончанияДействия	
                into #втНачРежимыПотребленияАбонентов
                from #втНачРежимыПотребленияАбонентовПред 
                inner join #втМаксДатаРегистрацииРежимыПотребленияАбонентов on #втНачРежимыПотребленияАбонентовПред.Абонент = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.Абонент
                and #втНачРежимыПотребленияАбонентовПред.РежимПотребления = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.РежимПотребления
                and #втНачРежимыПотребленияАбонентовПред.Поставщик = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.Поставщик
                and #втНачРежимыПотребленияАбонентовПред.УзелУчета = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.УзелУчета
                and #втНачРежимыПотребленияАбонентовПред.Период = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.Период
                and #втНачРежимыПотребленияАбонентовПред.ДатаРегистрацииИзменения = #втМаксДатаРегистрацииРежимыПотребленияАбонентов.ДатаРегистрацииИзменения


                select Период, max(Дата_Time) as Дата_Time, Абонент, РежимПотребления, Поставщик, УзелУчета, ДатаРегистрацииИзменения
                into #втМаксРегистраторРежимыПотребленияАбонентов
                from #втНачРежимыПотребленияАбонентов
                group by Период, Абонент, РежимПотребления, Поставщик, УзелУчета, ДатаРегистрацииИзменения


                select #втНачРежимыПотребленияАбонентов.Период, 
                    #втНачРежимыПотребленияАбонентов.Дата_Time,
                    #втНачРежимыПотребленияАбонентов.ДатаРегистрацииИзменения,
                    #втНачРежимыПотребленияАбонентов.Абонент,
                    #втНачРежимыПотребленияАбонентов.РежимПотребления,
                    #втНачРежимыПотребленияАбонентов.Поставщик,
                    #втНачРежимыПотребленияАбонентов.УзелУчета,
                    #втНачРежимыПотребленияАбонентов.Действует,
                    #втНачРежимыПотребленияАбонентов.Оборудование,
                    #втНачРежимыПотребленияАбонентов.ДатаНачалаДействия,
                    #втНачРежимыПотребленияАбонентов.ДатаОкончанияДействия	
                into #втПоследниеВДнеРежимыПотребленияАбонентов
                from #втНачРежимыПотребленияАбонентов 
                inner join #втМаксРегистраторРежимыПотребленияАбонентов on #втНачРежимыПотребленияАбонентов.Период = #втМаксРегистраторРежимыПотребленияАбонентов.Период
                and #втНачРежимыПотребленияАбонентов.Дата_Time = #втМаксРегистраторРежимыПотребленияАбонентов.Дата_Time
                and #втНачРежимыПотребленияАбонентов.ДатаРегистрацииИзменения = #втМаксРегистраторРежимыПотребленияАбонентов.ДатаРегистрацииИзменения
                and #втНачРежимыПотребленияАбонентов.Абонент = #втМаксРегистраторРежимыПотребленияАбонентов.Абонент
                and #втНачРежимыПотребленияАбонентов.РежимПотребления = #втМаксРегистраторРежимыПотребленияАбонентов.РежимПотребления
                and #втНачРежимыПотребленияАбонентов.Поставщик = #втМаксРегистраторРежимыПотребленияАбонентов.Поставщик
                and #втНачРежимыПотребленияАбонентов.УзелУчета = #втМаксРегистраторРежимыПотребленияАбонентов.УзелУчета


                select max(Период) as Период, Абонент, РежимПотребления, Поставщик, УзелУчета
                into #втМаксПериодРежимыПотребленияАбонентов
                from #втПоследниеВДнеРежимыПотребленияАбонентов
                group by Абонент, РежимПотребления, Поставщик, УзелУчета


                select dbo.Справочник_РежимыПотребленияУслуг.Наименование as РежимПотребления,	   
                    dbo.Справочник_УзлыУчета.Наименование as УзелУчета,
                    case when #втПоследниеВДнеРежимыПотребленияАбонентов.Действует = 0x01 then 'Да' else 'Нет' end as Действует,	   
                    case when dbo.Справочник_Оборудование.Наименование is null then '---' else dbo.Справочник_Оборудование.Наименование end as Оборудование,
                    replace(replace(convert(varchar, #втПоследниеВДнеРежимыПотребленияАбонентов.ДатаНачалаДействия, 104), '.4', '.2'), '.3', '.1') as ДатаНачалаДействия,
                    replace(replace(replace(convert(varchar, #втПоследниеВДнеРежимыПотребленияАбонентов.ДатаОкончанияДействия, 104), '.4', '.2'), '.3', '.1'), '.2', '.0') as ДатаОкончанияДействия
                from #втПоследниеВДнеРежимыПотребленияАбонентов
                inner join #втМаксПериодРежимыПотребленияАбонентов on #втПоследниеВДнеРежимыПотребленияАбонентов.Период = #втМаксПериодРежимыПотребленияАбонентов.Период
                and #втПоследниеВДнеРежимыПотребленияАбонентов.Абонент = #втМаксПериодРежимыПотребленияАбонентов.Абонент
                and #втПоследниеВДнеРежимыПотребленияАбонентов.РежимПотребления = #втМаксПериодРежимыПотребленияАбонентов.РежимПотребления
                and #втПоследниеВДнеРежимыПотребленияАбонентов.Поставщик = #втМаксПериодРежимыПотребленияАбонентов.Поставщик
                and #втПоследниеВДнеРежимыПотребленияАбонентов.УзелУчета = #втМаксПериодРежимыПотребленияАбонентов.УзелУчета
                inner join dbo.Справочник_РежимыПотребленияУслуг on #втПоследниеВДнеРежимыПотребленияАбонентов.РежимПотребления = dbo.Справочник_РежимыПотребленияУслуг.Ссылка
                inner join dbo.Справочник_УзлыУчета on #втПоследниеВДнеРежимыПотребленияАбонентов.УзелУчета = dbo.Справочник_УзлыУчета.Ссылка
                left join dbo.Справочник_Оборудование on #втПоследниеВДнеРежимыПотребленияАбонентов.Оборудование = dbo.Справочник_Оборудование.Ссылка

                drop table #втНачРежимыПотребленияАбонентовПред,
                        #втМаксДатаРегистрацииРежимыПотребленияАбонентов, 
                        #втНачРежимыПотребленияАбонентов, 
                        #втМаксРегистраторРежимыПотребленияАбонентов, 
                        #втПоследниеВДнеРежимыПотребленияАбонентов,
                        #втМаксПериодРежимыПотребленияАбонентов;
'''

# взаиморасчеты абонента на тек дату
sql_select13 = '''
                SET NOCOUNT ON;

                DECLARE @P0 datetime, @P1 datetime2(3), @P2 datetime2(3), @P3 varbinary(16), @P4 varbinary(16)

                SET @P0 = %s                
                SET @P1 = DATEADD(year, 2000, dateadd(day, 1-day(@P0), @P0))                           -- дата начала 
                SET @P2 = DATEADD(year, 2000, dateadd(month, 1, dateadd(day, 1-day(@P0), @P0))-1)      -- дата окончания
                SET @P3 = (SELECT _IDRRef FROM dbo._Reference16 WHERE dbo._Reference16._Fld375 = %s)   -- абонент
                SET @P4 = (SELECT _IDRRef FROM dbo._Reference93 WHERE dbo._Reference93._Marked = 0x00) -- подразделение

                SELECT
                    (SELECT dbo._Reference129._Description FROM dbo._Reference129 WHERE dbo._Reference129._IDRRef = T21._ParentIDRRef) as УслугаРодитель,
                    T21._Description AS Услуга,
                    CAST(SUM(T1.Q_001_F_001_) AS NUMERIC(38, 2)) AS ТекущаяЗадолженность,
                    CAST(SUM(T1.Q_001_F_003_) AS NUMERIC(38, 2)) AS Рассрочка,
                    CAST(SUM(T1.Q_001_F_002_) AS NUMERIC(38, 2)) AS СписаннаяЗадолженность
                FROM (  SELECT
                            T2.Fld3893RRef AS Q_001_F_000RRef,
                            T2.Fld3896Balance_ AS Q_001_F_001_,
                            CAST(0.0 AS NUMERIC(37, 5)) AS Q_001_F_002_,
                            CAST(0.0 AS NUMERIC(37, 5)) AS Q_001_F_003_
                        FROM (  SELECT
                                    T3.Fld3893RRef AS Fld3893RRef,
                                    CAST(SUM(T3.Fld3896Balance_) AS NUMERIC(37, 5)) AS Fld3896Balance_
                                FROM (  SELECT
                                            T4._Fld3893RRef AS Fld3893RRef,
                                            CAST(SUM(T4._Fld3896) AS NUMERIC(31, 5)) AS Fld3896Balance_
                                        FROM dbo._AccumRgT3910 T4
                                        WHERE T4._Period = '5999-11-01 00:00:00' AND (((T4._Fld3892RRef = @P3) AND CASE WHEN (T4._Fld3891RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01)) AND (T4._Fld3896 <> 0) AND (T4._Fld3896 <> 0)
                                        GROUP BY T4._Fld3893RRef
                                        HAVING (CAST(SUM(T4._Fld3896) AS NUMERIC(31, 5))) <> 0.0
                                        
                                        UNION ALL 
                                        
                                        SELECT
                                            T5._Fld3893RRef AS Fld3893RRef,
                                            CAST(CAST(SUM(CASE WHEN T5._RecordKind = 0.0 THEN -T5._Fld3896 ELSE T5._Fld3896 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld3896Balance_
                                        FROM dbo._AccumRg3889 T5
                                        WHERE T5._Period > @P2 AND T5._Period < '5999-11-01 00:00:00' AND T5._Active = 0x01 AND (((T5._Fld3892RRef = @P3) AND CASE WHEN (T5._Fld3891RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01))
                                        GROUP BY T5._Fld3893RRef
                                        HAVING (CAST(CAST(SUM(CASE WHEN T5._RecordKind = 0.0 THEN -T5._Fld3896 ELSE T5._Fld3896 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T3
                                GROUP BY T3.Fld3893RRef
                                HAVING (CAST(SUM(T3.Fld3896Balance_) AS NUMERIC(37, 5))) <> 0.0) T2
                                
                        UNION ALL 
                                
                        SELECT
                            T6.Fld3873RRef AS Fld3873RRef,
                            T6.Fld3875Balance_ AS Fld3875Balance_,
                            CAST(0.0 AS NUMERIC(37, 5)),
                            CAST(0.0 AS NUMERIC(37, 5))
                        FROM (  SELECT
                                    T7.Fld3873RRef AS Fld3873RRef,
                                    CAST(SUM(T7.Fld3875Balance_) AS NUMERIC(37, 5)) AS Fld3875Balance_
                                FROM (  SELECT
                                            T8._Fld3873RRef AS Fld3873RRef,
                                            CAST(SUM(T8._Fld3875) AS NUMERIC(31, 5)) AS Fld3875Balance_
                                        FROM dbo._AccumRgT3888 T8
                                        WHERE T8._Period = '5999-11-01 00:00:00' AND (((T8._Fld3872RRef = @P3) AND CASE WHEN (T8._Fld3871RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01)) AND (T8._Fld3875 <> 0) AND (T8._Fld3875 <> 0)
                                        GROUP BY T8._Fld3873RRef
                                        HAVING (CAST(SUM(T8._Fld3875) AS NUMERIC(31, 5))) <> 0.0
                                        
                                        UNION ALL
                                        
                                        SELECT                                                
                                            T9._Fld3873RRef AS Fld3873RRef,
                                            CAST(CAST(SUM(CASE WHEN T9._RecordKind = 0.0 THEN -T9._Fld3875 ELSE T9._Fld3875 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld3875Balance_
                                        FROM dbo._AccumRg3869 T9
                                        WHERE T9._Period > @P2 AND T9._Period < '5999-11-01 00:00:00' AND T9._Active = 0x01 AND (((T9._Fld3872RRef = @P3) AND CASE WHEN (T9._Fld3871RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01))
                                        GROUP BY T9._Fld3873RRef
                                        HAVING (CAST(CAST(SUM(CASE WHEN T9._RecordKind = 0.0 THEN -T9._Fld3875 ELSE T9._Fld3875 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T7
                                GROUP BY T7.Fld3873RRef
                                HAVING (CAST(SUM(T7.Fld3875Balance_) AS NUMERIC(37, 5))) <> 0.0) T6
                                        
                        UNION ALL 
                        
                        SELECT
                            T10.Fld3848RRef AS Fld3848RRef,
                            CAST(0.0 AS NUMERIC(37, 5)),
                            T10.Fld3851Balance_ AS Fld3851Balance_,
                            CAST(0.0 AS NUMERIC(37, 5))
                        FROM (  SELECT
                                    T11.Fld3848RRef AS Fld3848RRef,
                                    CAST(SUM(T11.Fld3851Balance_) AS NUMERIC(37, 5)) AS Fld3851Balance_
                                FROM (  SELECT
                                            T12._Fld3848RRef AS Fld3848RRef,
                                            CAST(SUM(T12._Fld3851) AS NUMERIC(31, 5)) AS Fld3851Balance_
                                        FROM dbo._AccumRgT3858 T12
                                        WHERE T12._Period = '5999-11-01 00:00:00' AND (((T12._Fld3847RRef = @P3) AND CASE WHEN (T12._Fld3846RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01)) AND (T12._Fld3851 <> 0) AND (T12._Fld3851 <> 0)
                                        GROUP BY T12._Fld3848RRef
                                        HAVING (CAST(SUM(T12._Fld3851) AS NUMERIC(31, 5))) <> 0.0
                                        
                                        UNION ALL
                                                        
                                        SELECT
                                            T13._Fld3848RRef AS Fld3848RRef,
                                            CAST(CAST(SUM(CASE WHEN T13._RecordKind = 0.0 THEN -T13._Fld3851 ELSE T13._Fld3851 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld3851Balance_
                                        FROM dbo._AccumRg3844 T13
                                        WHERE T13._Period > @P2 AND T13._Period < '5999-11-01 00:00:00' AND T13._Active = 0x01 AND (((T13._Fld3847RRef = @P3) AND CASE WHEN (T13._Fld3846RRef IN (@P4)) THEN 0x01 ELSE 0x00 END = 0x01))
                                        GROUP BY T13._Fld3848RRef
                                        HAVING (CAST(CAST(SUM(CASE WHEN T13._RecordKind = 0.0 THEN -T13._Fld3851 ELSE T13._Fld3851 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T11
                                GROUP BY T11.Fld3848RRef
                                HAVING (CAST(SUM(T11.Fld3851Balance_) AS NUMERIC(37, 5))) <> 0.0) T10
                                                
                        UNION ALL 
                        
                        SELECT
                            T20._Fld5137RRef AS Fld5137RRef,
                            CAST(0.0 AS NUMERIC(37, 5)),
                            CAST(0.0 AS NUMERIC(37, 5)),
                            T14.Fld5228Balance_ AS Fld5228Balance_
                        FROM (  SELECT
                                    T15.Fld5227RRef AS Fld5227RRef,
                                    CAST(SUM(T15.Fld5228Balance_) AS NUMERIC(37, 5)) AS Fld5228Balance_
                                FROM (  SELECT
                                            T16._Fld5227RRef AS Fld5227RRef,
                                            CAST(SUM(T16._Fld5228) AS NUMERIC(31, 5)) AS Fld5228Balance_
                                        FROM dbo._AccumRgT5232 T16
                                        LEFT OUTER JOIN dbo._Document5100 T17
                                        ON T16._Fld5227RRef = T17._IDRRef
                                        WHERE T16._Period = '5999-11-01 00:00:00' AND ((((T17._Fld5135RRef = @P3) AND CASE WHEN (T17._Fld5139RRef IN (@P4)) THEN 0x01 WHEN NOT ((T17._Fld5139RRef IN (@P4))) THEN 0x00 END = 0x01) AND (T16._Fld5226 <= @P1))) AND (T16._Fld5228 <> 0) AND (T16._Fld5228 <> 0)
                                        GROUP BY T16._Fld5227RRef
                                        HAVING (CAST(SUM(T16._Fld5228) AS NUMERIC(31, 5))) <> 0.0
                                UNION ALL 
                                
                                SELECT
                                    T18._Fld5227RRef AS Fld5227RRef,
                                    CAST(CAST(SUM(CASE WHEN T18._RecordKind = 0.0 THEN -T18._Fld5228 ELSE T18._Fld5228 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5)) AS Fld5228Balance_
                                FROM dbo._AccumRg5225 T18
                                LEFT OUTER JOIN dbo._Document5100 T19
                                ON T18._Fld5227RRef = T19._IDRRef
                                WHERE T18._Period > @P2 AND T18._Period < '5999-11-01 00:00:00' AND T18._Active = 0x01 AND ((((T19._Fld5135RRef = @P3) AND CASE WHEN (T19._Fld5139RRef IN (@P4)) THEN 0x01 WHEN NOT ((T19._Fld5139RRef IN (@P4))) THEN 0x00 END = 0x01) AND (T18._Fld5226 <= @P1)))
                                GROUP BY T18._Fld5227RRef
                                HAVING (CAST(CAST(SUM(CASE WHEN T18._RecordKind = 0.0 THEN -T18._Fld5228 ELSE T18._Fld5228 END) AS NUMERIC(25, 5)) AS NUMERIC(31, 5))) <> 0.0) T15
                        GROUP BY T15.Fld5227RRef
                        HAVING (CAST(SUM(T15.Fld5228Balance_) AS NUMERIC(37, 5))) <> 0.0) T14
                        LEFT OUTER JOIN dbo._Document5100 T20
                        ON T14.Fld5227RRef = T20._IDRRef) T1
                INNER JOIN dbo._Reference129 T21
                ON (CASE WHEN (T1.Q_001_F_000RRef = 0x00000000000000000000000000000000) THEN 0x963228632B0039644C534B49F4AFF61D ELSE T1.Q_001_F_000RRef END = T21._IDRRef)
                WHERE 1=1
                GROUP BY T21._Description,
                         T21._ParentIDRRef
'''

# изменение режима исправления ошибок
sql_update1 = '''
                SET NOCOUNT ON;

                DECLARE @P1 BINARY, @P2 NVARCHAR(200)

                SET @P1 = CONVERT(BINARY(1), %s)
                SET @P2 = %s
                
                UPDATE dbo._InfoRg4272
                SET dbo._InfoRg4272._Fld4275_L = @P1
                FROM dbo._InfoRg4272
                INNER JOIN dbo._Reference95 on dbo._InfoRg4272._Fld4273_RRRef = dbo._Reference95._IDRRef
                WHERE dbo._InfoRg4272._Fld4274RRef = 0xB08FABBB26672A9248C34E140B5DBA9D 
                AND dbo._Reference95._Description = @P2
'''

# изменение периода расчета
sql_update2 = '''
                SET NOCOUNT ON;

                DECLARE @P1 DATETIME, @P2 BINARY

                SET @P1 = %s
                SET @P2 = CONVERT(BINARY(1), %s)
                
                UPDATE dbo._InfoRg2721
                SET	dbo._InfoRg2721._Fld2723 = @P1,  
                    dbo._InfoRg2721._Fld2725 = @P1,
                    dbo._InfoRg2721._Fld2724 = @P2,
                    dbo._InfoRg2721._Fld2726 = @P2
'''

# установка значений в регламетные задания
sql_update3 = '''
                SET NOCOUNT ON;

                DECLARE @P1 BINARY, @P2 NVARCHAR(1), @P3 NVARCHAR(50)

                SET @P1 = CONVERT(BINARY(1), %s)
                SET @P2 = %s
                SET @P3 = %s

                UPDATE dbo._ScheduledJobs3995
                SET	dbo._ScheduledJobs3995._Use = @P1,  
                    dbo._ScheduledJobs3995._JobKey = @P2		
                WHERE dbo._ScheduledJobs3995._Description = @P3
'''