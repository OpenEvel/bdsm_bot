BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `states` (
	`id`	INTEGER NOT NULL UNIQUE,
	`state`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `projects` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE IF NOT EXISTS `callcenters` (
	`id`	INTEGER NOT NULL UNIQUE,
	`company`	TEXT NOT NULL,
	`username`	TEXT NOT NULL,
	`first_name`	TEXT NOT NULL,
	`last_name`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `admins` (
	`id`	INTEGER NOT NULL UNIQUE,
	`username`	TEXT NOT NULL,
	`first_name`	TEXT NOT NULL,
	`last_name`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
COMMIT;
