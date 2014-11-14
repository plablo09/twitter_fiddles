#----------------------------------
#################################
#Flujo de trabajo para obtener inicios y finales
#en los distritos de la EOD
#################################
#-----------------------------------



#----------------------------------
#Popular la tabla con un día específico y un intervalo de horas
#(en el scrpt cortes.py se automatiza el proceso)
#-----------------------------------
insert into morning_paths (uname,geom)
(
select  uname, ST_MAKELINE(geom) from(
    SELECT uname,  geom, hora, min(hora)
    OVER (PARTITION BY uname ORDER BY hora DESC)
    from (
        select * from tweets where fecha = '2014-11-6' and (hora>='13:00:00' and hora <='17:00:00')
        and uname in (
            select uname from tweets group by uname having count(uname)>1
        )
    ) as bar
) as foo
Group BY uname
)

#----------------------------------
#crear y popular la tabla con los puntos de origen y
#destino de cada trayectoria (filtrados por aquellos que tengan una separación
#mayor a 1000 metros )
#-----------------------------------

create table o_d_afternoon as
select id, uname, st_startpoint(geom) as inicio, st_endpoint(geom) as final
from afternoon_paths where st_distance(st_startpoint(geom),st_endpoint(geom)) > 1000

#----------------------------------
#Unir puntos de inicio (fin) con
#distritos de la EOD
#-----------------------------------

select distritos_eod.gid, distritos_eod.geom, subq.viajes from distritos_eod join
(
    SELECT d.gid, count(v.inicio) AS viajes
    FROM distritos_eod d LEFT JOIN o_d_afternoon v
    ON st_contains(d.geom,v.inicio)
    GROUP BY d.gid
)as subq
on distritos_eod.gid = subq.gid
