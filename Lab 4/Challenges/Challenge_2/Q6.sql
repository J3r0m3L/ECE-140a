update teachers set name="Ramsin" where id=5678;

select teachers.name as teacher_name, courses.name as course_name, courses.id as course_id from teachers left join courses on teachers.id=courses.teacher_id;