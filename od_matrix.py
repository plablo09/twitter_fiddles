# -*- coding: utf-8 -*-
import psycopg2 as psy
from config.credentials import get_auth_credentials
import numpy as np

conn_params = get_auth_credentials()
conn_str =" host='localhost' dbname='twitter_feed'" + "user=" + \
            conn_params["dbuser"] + " password=" + conn_params["dbpassword"]

conn = psy.connect(conn_str)

if conn:
    q_distritos = "select cve_dist from distritos_eod_corrected;"
    cur = conn.cursor()
    cur.execute(q_distritos)
    distritos = cur.fetchall()
    distritos = sorted([d[0] for d in distritos])
    print distritos
    od = {}
    matriz = np.zeros(shape=(len(distritos),len(distritos)),dtype=np.int)
    for n,d in enumerate(distritos):
        viajes = np.zeros(len(distritos),dtype=np.int)
        ini_fin = []
        ini_q = "select o.id, o.inicio, o.final, d.geom, d.cve_dist from \
                o_d_afternoon o join distritos_eod_corrected d on \
                st_intersects(o.inicio,d.geom) where d.cve_dist = %s"
        cur.execute(ini_q,[d])
        inicios = cur.fetchall()
        inicios = [i[0] for i in inicios]
        #print len(inicios)
        for i in inicios:
            #print "el inicioo " + str(i[0])
            fin_q = "select d.cve_dist from \
                    o_d_afternoon o join distritos_eod_corrected d on \
                    st_intersects(o.final,d.geom) where o.id = %s"
            cur.execute(fin_q,[i])
            final = cur.fetchall()
            if len(final):
                idx = distritos.index(final[0][0])
                viajes[idx] +=1

        matriz[n] = viajes



    print matriz
    np.savetxt('output/od_matrix_afternoon.csv',matriz,fmt='%i',delimiter=',')

        #print inicios
        # for i in inicios:
        #
        #     print cur.fetchall()
else:
    print 'No se pudo establecer una conección con la base de datos\
            checa los parámetros'
