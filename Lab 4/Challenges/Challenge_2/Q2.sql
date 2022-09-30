create table students (
    id integer null,
    name varchar(30) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(30) NOT NULL);

create table teachers (
    id integer null,
    name varchar(30) not null);

create table grades (
    student_id integer null,
    course_id integer null,
    grade varchar(30) not null
);

create table courses(
    id integer null,
    name varchar(70) not null,
    teacher_id integer null
);
