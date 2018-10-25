create database IS_SQL_Injection_Test;
use IS_SQL_Injection_Test;
create table login (
    username varchar(32) not null,
    password varchar(32) not null,
    primary key(`username`)
);
insert into login values ('abhishek', 'abhishekpass');
insert into login values ('anurag', 'anuragpass');
insert into login values ('vaibhav', 'vaibhavpass');
insert into login values ('tanmay', 'tanmaypass');
