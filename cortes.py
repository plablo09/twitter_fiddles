# -*- coding: utf-8 -*-
import psycopg2 as psy
from config.credentials import get_auth_credentials

conn_params = get_auth_credentials()
conn_str =" host='localhost' dbname='twitter_feed'" + "user=" + \
conn_params["dbuser"] + " password=" + conn_params["dbpassword"]

#
# "2014-10-29"
# "2014-10-30"
# "2014-10-31"
# "2014-11-01"
# "2014-11-02"
# "2014-11-03"
# "2014-11-04"
# "2014-11-05"
# "2014-11-06"
# "2014-11-07"
# "2014-11-08"
# "2014-11-09"
# "2014-11-10"
# "2014-11-11"
# "2014-11-12"
# "2014-11-13"
# "2014-11-14"
#
# ('2014-10-30','2014-10-31','2014-11-03','2014-11-04','2014-11-05','2014-11-06',
# '2014-11-07','2014-11-10','2014-11-11','2014-11-12','2014-11-13')

# try:
#     conn = psy.connect(conn_str)
# except psy.Error, e:
#     print e.pgerror
conn = psy.connect(conn_str)
if conn:

    fechas =('2014-10-30','2014-10-31','2014-11-03','2014-11-04','2014-11-05','2014-11-06',
                '2014-11-07','2014-11-10','2014-11-11','2014-11-12','2014-11-13')
    #fecha = "2014-11-03"

    sql = "insert into afternoon_paths (uname,geom)( \
                select uname, ST_MAKELINE(geom) as geom from(\
                SELECT uname,  geom, hora, min(hora)\
                OVER (PARTITION BY uname ORDER BY hora ASC)\
                from (\
                            select * from tweets where fecha = %s and (hora>='00:00:00' and hora <='04:00:00')\
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
