select name, id, course_id, grade from students left join grades on grades.student_id=student_id;