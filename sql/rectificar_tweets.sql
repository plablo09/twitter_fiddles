#----------------------------------
#################################
#Crear una tabla con los tweets rectificados:
#-reproyectados a 32614
#-corregidas la fecha y la hora al uso de la ciudad de méxico
#################################
#-----------------------------------

create table tweets_rectificado as select * from tweets;

alter table tweets_rectificado add constraint tw_r_id unique(id);
alter table tweets_rectificado add constraint tw_r_pk primary key (id);

ALTER TABLE tweets_rectificado
ALTER COLUMN geom
TYPE Geometry(Point, 32614)
USING ST_Transform(geom, 32614);

alter table tweets_rectificado add column fecha_hora timestamp with time zone;
update tweets_rectificado set
fecha_hora = to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS') - interval '6 hours';

update tweets_rectificado set fecha = fecha_hora::date;
update tweets_rectificado set hora = fecha_hora::time;

#----------------------------------
#################################
#Actualizar la tabla rectificada con los valores
#de la tabla tweets desde la última actualización
#
#################################
    #-----------------------------------

insert into tweets_rectificado (id, uname, "text", fecha, hora, geom, fecha_hora)
    (
        select id, uname, "text", (to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS')- interval '6 hours')::date,
        (to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS')- interval '6 hours')::time,
        ST_Transform(geom, 32614),
        to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS')- interval '6 hours'
        from tweets where
        to_timestamp(fecha::text|| ' ' || hora::text,'YYYY-MM-DD HH24:MI:SS') >(select max(fecha_hora) + interval '6 hours' from tweets_rectificado)
    )
