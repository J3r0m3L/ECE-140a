create table testusers (
    id integer auto_increment primary key,
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    email varchar(50) not null,
    age int,
    created_at timestamp);