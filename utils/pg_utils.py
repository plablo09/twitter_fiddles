# -*- coding: utf-8 -*-
import psycopg2 as psy
from datetime import datetime



class PgPersistence():
    """Al instanciarlo crea una conección a una bd y provee un método para escribir filas.

    Asumimos que el servidor está en localhost y que tiene una tabla "tweets"
    con las siguientes columnas:
    user: text
    date: timestamp
    text:text
    geom: geometry(point)

    @param conn_params dict con las llaves dbuser:dbuser, dbpassword:dbpwd

    """

    def __init__(self,conn_params):
        print "siiiii"
        conn_str =" host='localhost' dbname='twitter_feed'" + "user=" + \
                    conn_params["dbuser"] + " password=" + conn_params["dbpassword"]

        try:
            self.conn = psy.connect(conn_str)
        except psy.Error, e:
            print e.pgerror



    def insert_row(self,row):
        """Inserta la fila en la base de datos.

        Da formato las coordenadas antes de mandar a la BD.

        @param row list [user,text,date,coordenadas]
        """
        print 'entre'
        cur = self.conn.cursor()
        lat_lon = row.pop()
        cur.execute("SELECT ST_SetSRID(ST_MakePoint(%s, %s),4326);",lat_lon)
        point_wkb = cur.fetchall()
        row.append(point_wkb[0])
        query = """INSERT INTO tweets(uname,text,fecha,hora,geom) VALUES (%s,%s,%s,%s,%s);"""
        print query
        print row
        cur.execute(query,row)
        self.conn.commit()
