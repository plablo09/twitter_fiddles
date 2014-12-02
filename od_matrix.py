# -*- coding: utf-8 -*-
import psycopg2 as psy
from config.credentials import get_auth_credentials

conn_params = get_auth_credentials()
conn_str =" host='localhost' dbname='twitter_feed'" + "user=" + \
            conn_params["dbuser"] + " password=" + conn_params["dbpassword"]

conn = psy.connect(conn_str)

if conn:
    print 'me conecté'
    q_distritos = "select cve_dist from distritos_eod limit 10;"
    cur = conn.cursor()
    cur.execute(q_distritos)
    distritos = cur.fetchall()

    for d in distritos:
        ini_fin = []
        ini_q = "select o.id, o.inicio, o.final, d.geom, d.cve_dist from \
                o_d_morning o join distritos_eod d on \
                st_intersects(o.inicio,d.geom) where d.cve_dist =%s"
        cur.execute(ini_q,[d[0]])
        inicios = cur.fetchall()
        print len(inicios)
        for i in inicios:
            print "el inicioo " + str(i[0])
            fin_q = "select d.cve_dist from \
                    o_d_morning o join distritos_eod d on \
                    st_intersects(o.final,d.geom) where o.id = %s"
            cur.execute(fin_q,[i[0]])
            finales = cur.fetchall()
            print "el fin  " + str(finales[0])
            ini_fin.append((i[4],len(finales)))

        print ini_fin

        #print inicios
        # for i in inicios:
        #
        #     print cur.fetchall()
