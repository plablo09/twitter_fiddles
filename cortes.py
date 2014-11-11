# -*- coding: utf-8 -*-
import psycopg2 as psy
from config.credentials import get_auth_credentials

conn_params = get_auth_credentials()
conn_str =" host='localhost' dbname='tuiter'" + "user=" + \
conn_params["dbuser"] + " password=" + conn_params["dbpassword"]

# try:
#     conn = psy.connect(conn_str)
# except psy.Error, e:
#     print e.pgerror
conn = psy.connect(conn_str)
if conn:

    fechas = ('2014-11-07','2014-11-06','2014-11-05','2014-11-04',
                '2014-11-03','2014-11-02')
    #fecha = "2014-11-03"

    sql = "insert into morning_paths (uname,geom)( \
                select uname, ST_MAKELINE(geom) as geom from(\
                SELECT uname,  geom, hora, min(hora)\
                OVER (PARTITION BY uname ORDER BY hora DESC)\
                from (\
                            select * from tweets where fecha = %s and (hora>='13:00:00' and hora <='17:00:00')\
                            and uname in (\
                                        select uname from tweets group by uname having count(uname)>1\
                            )\
                ) as bar\
                ) as foo\
                Group BY uname)"
    cur = conn.cursor()
    for fecha in fechas:
        cur.execute(sql,(fecha,))
        conn.commit()
    # for record in cur:
    #     print record
