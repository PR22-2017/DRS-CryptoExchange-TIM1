create database if not exists `cryptoexchange` default character set utf8 collate utf8_general_ci;
use `cryptoexchange`;

create table if not exists `accounts` (
	`firstname` varchar(50) not null,
    `lastname` varchar(50) not null,
    `address` varchar(100) not null,
    `city` varchar(50) not null,
    `phone_number` varchar(20) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `verified` bool not null,
    `balance` double not null,
    primary key (`email`)
) engine=InnoDB default charset=utf8;