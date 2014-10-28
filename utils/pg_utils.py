# -*- coding: utf-8 -*-
import psycopg2 as psy



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
        conn_str =" host='localhost' dbname='twitter_feed'" + "user=" + \
                    conn_params["dbuser"] + " password=" + conn_params["dbpassword"]
        print conn_str
        try:
            self.conn = psy.connect(conn_str)
        except psy.Error, e:
            print e.pgerror

        #self.table = "tweets"


    def insert_row(self,row):

        cur = self.conn.cursor()
        sql = "INSERT INTO tweets VALUES (%s,%s,%s);"
        cur.execute(sql,row)
        self.conn.commit()
