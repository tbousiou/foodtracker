create table log_date (
	id integer primary key autoincrement,
	entry_date date not null
);

create table food (
	id integer primary key autoincrement,
	name text not null,
	protein integer not null,
	carbohydrates integer not null,
	fat integer not null,
	calories integer not null
);

create table food_date (
	food_id integer not null,
	log_date_id integer not null,
	primary key(food_id, log_date_id)
);

insert into log_date values (1, '2019-09-01');
insert into log_date values (2, '2019-09-05');
insert into log_date values (3, '2019-09-10');
insert into log_date values (4, '2019-09-15');
insert into log_date values (5, '2019-09-20');

insert into food values (1, 'pizza', 10, 20, 30, 60);
insert into food values (2, 'burger', 10, 20, 30, 60);
insert into food values (3, 'feta', 10, 20, 30, 60);
insert into food values (4, 'banana', 10, 20, 30, 60);
insert into food values (5, 'cake', 10, 20, 30, 60);

insert into food_date values (1,1);
insert into food_date values (1,3);
insert into food_date values (1,5);
insert into food_date values (2,3);
insert into food_date values (2,4);
insert into food_date values (3,2);
insert into food_date values (3,3);
insert into food_date values (3,4);
insert into food_date values (5,1);
insert into food_date values (5,4);