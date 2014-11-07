#FILTRAR POR INTERVALO DE TIEMPO Y HACER CLIP CON
#EL LÍMITE METROPOLITANO
select q1.id,q1.uname
from (
select t.id,t.uname,t.text,to_char(t.hora,'HH24:MI:SS') as hora, t.geom from tweets t
where fecha = '2014-11-1' and
(hora <  '05:00:00' + interval'4 hours')
) q1
inner join limite_metropolitano l
on st_intersects(q1.geom,l.geom)

#Crear corte temporal y reproyectar a 32614
create table corte as select * from tweets
where fecha >= 'fecha_inicial' and fecha <='fecha_final';

alter table corte add constraint corte_id unique(id);
alter table corte add constraint corte_pk primary key (id);

ALTER TABLE corte
ALTER COLUMN geom
TYPE Geometry(Point, 32614)
USING ST_Transform(geom, 32614);

#Crear una columna con el tiempo corregido y popularla
alter table corte add column fecha_hora timestamp with time zone
update corte_1 set time_corregido = to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS')


#Seleccionar usuarios con más de un tuit:
#
select uname, count(uname) as count from tweets
group by uname
having (count(uname)>1)
order by count desc


#Seleccionar todos los tuits de usuarios con más de un tuit

select * from tweets where uname in
(select uname from tweets
group by uname
having (count(uname)>1))

#buffer alrededor de cada tuit (para los tuits de los usuarios con
#más de un tuit)
select id,st_buffer(geom,500) as geom from corte_1 where uname in
(select uname from corte_1
group by uname
having (count(uname)>1))

#Hacer líneas para la actividad de cada usuario para un día

with grupos as
(
SELECT foo.uname, geom, hora, min(hora)
OVER (PARTITION BY uname ORDER BY hora DESC)
FROM (select * from corte_1 where fecha = '2014-11-3') as foo
)
select row_number() over(), uname, ST_MAKELINE(geom) as geom from grupos
Group BY uname


#Crear una tabla con los puntos de origen y fin de las trayectorias:
with grupos as
(
SELECT foo.uname, geom, hora, min(hora)
OVER (PARTITION BY uname ORDER BY hora DESC)
FROM (select * from corte
where fecha_hora > '2014-11-4 12:00:00'
    and fecha_hora < '2014-11-4 16:00:00') as foo
)
select bar.id,uname, st_startpoint(bar.geom) as geo_start, st_endpoint(bar.geom) as geo_end
into o_d
from(
select row_number() over() as id , uname, ST_MAKELINE(geom) as geom from grupos
Group BY uname
) as bar

#Contar los viajes que inician (terminan) en cada distrito
SELECT d.gid, count(v.geom) AS viajes
FROM distritos_eod LEFT JOIN o_d v
ON st_contains(d.geom,v.geom)
GROUP BY d.gid;
