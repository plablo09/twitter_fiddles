CREATE TABLE tweets
(
  id SERIAL,
  uname text,
  text text,
  fecha date,
  hora time
  CONSTRAINT tweets_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tweets
  OWNER TO postgres;

ALTER TABLE tweets ADD COLUMN geom geometry(Point,4326);
