with t_intervals as (
    select
    (select min(fecha_hora)::date from tweets_rectificado) + ( n    || ' minutes')::interval start_time,
    (select min(fecha_hora)::date from tweets_rectificado) + ((n+60) || ' minutes')::interval end_time
    from generate_series(0, (24*60), 60) n
)
select f.start_time, count(m.uname)
from tweets_rectificado m
right join t_intervals f
on m.fecha_hora >= f.start_time and m.fecha_hora < f.end_time
group by f.start_time, f.end_time
order by f.start_time
