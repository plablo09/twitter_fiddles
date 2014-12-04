# -*- coding: utf-8 -*-
import subprocess

lista_horas = ['%s:00:00' % h for h in xrange(06,23)]

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


# lista_fechas =('2014-10-30','2014-10-31','2014-11-03','2014-11-04','2014-11-05','2014-11-06',
#             '2014-11-07','2014-11-10','2014-11-11','2014-11-12','2014-11-13')
#lista_fechas = ('2014-10-31','2014-11-01','2014-11-02','2014-11-03','2014-11-04')
lista_fechas = ('2014-11-04',)

lista_comandos = []
for k, fecha in enumerate(lista_fechas):
    for i,h in enumerate(lista_horas):
        if i < len(lista_horas) -1:
            sql = "select c.id, c.uname, c.text, to_char(c.hora,'HH24:MI:SS') as hora, st_transform(c.geom,4326) from tweets_rectificado c where c.fecha = '" + fecha +\
                    "' and (c.hora >= '" + h + "' and c.hora <= '" + \
                    lista_horas[i+1]+ "')"
            nombre_shape = "/home/plablo/twitter_tmp/"+"t_"  + str(i) +".shp"
            cmd = ["ogr2ogr","-f", "ESRI Shapefile",nombre_shape,
                    "PG:dbname=twitter_feed host=localhost port=5432 user=postgres password=l4szl0.l0szl4",
                    "-sql", sql,
                    "-lco" ,"ENCODING=", "UTF-8"
                    ]
            lista_comandos.append(cmd)


# lista_comandos = []
# for k, fecha in enumerate(lista_fechas):
#     sql = "select c.id, c.uname, c.text, to_char(c.hora,'HH24:MI:SS') as hora, c.geom from tweets c where c.fecha = '" + fecha +\
#             "'"
#     nombre_shape = "/home/plablo/twitter_shapes/d_"+str(k) + ".shp"
#     cmd = ["ogr2ogr","-f", "ESRI Shapefile",nombre_shape,
#             "PG:dbname=twitter_feed host=localhost port=5432 user=postgres password=l4szl0.l0szl4",
#             "-sql", sql,
#             "-lco" ,"ENCODING=", "UTF-8"
#             ]
#     lista_comandos.append(cmd)

#print lista_comandos


# lista_comandos = []
# for k, fecha in enumerate(lista_fechas):
#     for i,h in enumerate(lista_horas):
#         if i < len(lista_horas) -1:
#             sql = "select c.id, c.uname, c.text, to_char(c.hora,'HH24:MI:SS') as hora, c.geom from corte_1 c where c.fecha = '" + fecha +\
#                     "' and (c.hora >= '" + h + "' and c.hora <= '" + \
#                     lista_horas[i+1]+ "')"
#             nombre_shape = "output/d_"+str(k)+ "_t_"  + str(i) +".shp"
#             cmd = ["ogr2ogr","-f", "ESRI Shapefile",nombre_shape,
#                     "PG:dbname=twitter_feed host=localhost port=5432 user=postgres password=l4szl0.l0szl4",
#                     "-sql", sql,
#                     "-lco" ,"ENCODING=", "UTF-8"
#                     ]
#             lista_comandos.append(cmd)
#
# print lista_comandos

for comando in lista_comandos:
    process = subprocess.Popen(comando,stdout=subprocess.PIPE)
    streamdata = process.communicate()[0]
    print process.returncode
