drop database plr_photopath;

create database plr_photopath;

use plr_photopath;

create table if not exists label_list(
	label_id int unsigned auto_increment,
	label_name varchar(100) not null unique,
	label_path varchar(100) not null,
	table_name varchar(100) not null,
	primary key(label_id)
)engine=innoDB default charset=utf8;
	