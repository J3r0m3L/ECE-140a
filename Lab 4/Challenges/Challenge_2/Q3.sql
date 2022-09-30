load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/students.csv'
into table students
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/teachers.csv'
into table teachers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/grades.csv'
into table grades
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/courses.csv'
into table courses
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
