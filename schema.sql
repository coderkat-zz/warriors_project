create table Users (
	id INTEGER PRIMARY KEY,
	email VARCHAR(64),
	password VARCHAR(64),
	name VARCHAR(64)
);
create table Participants (
	id INTEGER PRIMARY KEY,
	name VARCHAR(64),
	chances INTEGER
);
create table Winners(
	id INTEGER PRIMARY KEY,
	name VARCHAR(64),
	game INTEGER
);