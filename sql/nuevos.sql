#----------------------------------
#Estas consultas incluyen algunas repetidas de queries.sql
#Hay que hacer un merge manual pero mejor las pongo aquí.
#
#-----------------------------------


#----------------------------------
#Selecciona una fecha y un intervalo de horas.
#Selecciona los usuarios con más de un tuit
#Regresa las geometrías de las trayectorias definidas por la sucesión de tuits
#-----------------------------------

with grupos as
(
SELECT foo.uname,  geom, hora, min(hora)
OVER (PARTITION BY uname ORDER BY hora DESC)
FROM (select * from tweets where fecha = '2014-11-3' and (hora>='13:00:00' and hora <='17:00:00')
	and uname in (select uname from tweets group by uname having count(uname)>1)
) as foo
)
select row_number() over(), uname, ST_MAKELINE(geom) as geom from grupos
Group BY uname

#----------------------------------
#
#Lo mismo que el anterior pero sin la cláusula with,
#para que sea fácil de usar en inserts
#-----------------------------------
select row_number() over(), uname, ST_MAKELINE(geom) as geom from(
	SELECT uname,  geom, hora, min(hora)
	OVER (PARTITION BY uname ORDER BY hora DESC)
	from (
		select * from tweets where fecha = '2014-11-3' and (hora>='13:00:00' and hora <='17:00:00')
		and uname in (
			select uname from tweets group by uname having count(uname)>1
		)
	) as bar
) as foo
Group BY uname

#----------------------------------
#Crear una tabla para guardar todas las líneas que correspondan a
#un mismo corte del día y para todos los días de la semana
#-----------------------------------
create table morning_paths
(
	uname text,
	geom geometry(Linestring,4326)
)

ALTER TABLE morning_paths ADD COLUMN id BIGSERIAL PRIMARY KEY;

#----------------------------------
#Popular la tabla con un día específico y un intervalo de horas
#
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
