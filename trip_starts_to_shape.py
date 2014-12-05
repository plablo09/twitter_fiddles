# -*- coding: utf-8 -*-
import subprocess

base_sql = """with m_p as (select * from
    (
        select  row_number() over() as id, uname, ST_MAKELINE(geom) as geom from(
            SELECT uname,  geom, hora, min(hora)
            OVER (PARTITION BY uname ORDER BY hora DESC)
            from (
                select * from tweets_rectificado
                where extract(dow from fecha_hora) not in (0,6)
                and (hora>='%s' and hora <='%s')
                and uname in (select uname from tweets_rectificado group by uname having count(uname)>1)
            ) as bar
        ) as foo
        Group BY uname
    ) as ext)

    select m_p.id, st_setsrid(st_transform(st_startpoint(m_p.geom),4326),4326) from m_p
    where st_distance(st_startpoint(m_p.geom),st_endpoint(m_p.geom)) >1000"""

lista_horas = [(str(h) + ':00:00',str(h+1) +':00:00') for h in xrange(06,23)]
each_hour = [base_sql % h for h in lista_horas]
lista_comandos = []
for i,sql in enumerate(each_hour):
    nombre_shape = "/home/plablo/twitter_tmp/"+"t_"  + str(i) +".shp"
    cmd = ["ogr2ogr","-f", "ESRI Shapefile",nombre_shape,
            "PG:dbname=twitter_feed host=localhost port=5432 user=postgres password=l4szl0.l0szl4",
            "-sql", sql,
            "-lco" ,"ENCODING=", "UTF-8",
            "-a_srs","EPSG:4326"
            ]
    lista_comandos.append(cmd)

for comando in lista_comandos:
    process = subprocess.Popen(comando,stdout=subprocess.PIPE)
    streamdata = process.communicate()[0]
    print process.returncode
#
# sql = "select c.id, c.uname, c.text, to_char(c.hora,'HH24:MI:SS') as hora, st_transform(c.geom,4326) from tweets_rectificado c where c.fecha = '" + fecha +\
#         "' and (c.hora >= '" + h + "' and c.hora <= '" + \
#         lista_horas[i+1]+ "')"
# nombre_shape = "/home/plablo/twitter_tmp/"+"t_"  + str(i) +".shp"
# cmd = ["ogr2ogr","-f", "ESRI Shapefile",nombre_shape,
#         "PG:dbname=twitter_feed host=localhost port=5432 user=postgres password=l4szl0.l0szl4",
#         "-sql", sql,
#         "-lco" ,"ENCODING=", "UTF-8"
#         ]
# lista_comandos.append(cmd)
