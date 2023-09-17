create table stir_log(
    stir_dt text,
    result text
);

create table temp_log(
	temp_dt text,
	sensor_id int,
	temp real
);




create table heat_log(
	heat_dt text,
	status int -- 0=off 1=on
);

create table light_log(
	light_dt text,
	light int -- 0=off 1=on
);

