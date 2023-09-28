-- The following table names are forbidden [archive, record, connection]
-- Use the same structure, and follow the same pattern of the comments below
-- Use `_connection_` as an authentication column
-- MySql DBMS is strongly recommended

/*START*/
CREATE TABLE teacher_account(
	id INT AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE,
	password VARCHAR(128) NOT NULL,
	_connection_ VARCHAR(200),
	PRIMARY KEY (id)
);
/**/
CREATE TABLE classroom(
	id INT AUTO_INCREMENT,
	teacherId INT,
	classroom_name VARCHAR(50) NOT NULL,
	classroom_description VARCHAR(200),
	PRIMARY KEY (id),
	FOREIGN KEY (teacherId) REFERENCES teacher_account(id)
);
/**/
CREATE TABLE student_account(
	id INT AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE,
	password VARCHAR(128) NOT NULL,
	_connection_ VARCHAR(200),
	PRIMARY KEY (id)
);
/**/
CREATE TABLE studet_classroom(
	id INT AUTO_INCREMENT,
	studetId INT NOT NULL,
	classroomId INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (studetId) REFERENCES student_account(id),
	FOREIGN KEY (classroomId) REFERENCES classroom(id)
);
/**/
CREATE TABLE exam(
	id INT AUTO_INCREMENT,
	num INT,
	exam_name VARCHAR(50),
	classroomId INT,
	PRIMARY KEY (id),
	FOREIGN KEY (classroomId) REFERENCES classroom(id)
);
/**/
CREATE TABLE MCQ(
	id INT AUTO_INCREMENT,
	examId INT,
	question VARCHAR(200),
	ch1 VARCHAR(200),
	ch2 VARCHAR(200),
	ch3 VARCHAR(200),
	ch4 VARCHAR(200),
	ch1_ INT,
	ch2_ INT,
	ch3_ INT,
	ch4_ INT,
	PRIMARY KEY (id),
	FOREIGN KEY (examId) REFERENCES exam(id)
);
/**/
CREATE TABLE TF(
	id INT AUTO_INCREMENT,
	examId INT,
	question VARCHAR(200),
	answer INT,
	PRIMARY KEY (id),
	FOREIGN KEY (examId) REFERENCES exam(id)
);
/**/
CREATE TABLE announcement(
	id INT AUTO_INCREMENT,
	date VARCHAR(100),
	announcement_body VARCHAR(50) UNIQUE,
	announcer_name VARCHAR(50),
	classroomId INT,
	PRIMARY KEY (id),
	FOREIGN KEY (classroomId) REFERENCES classroom(id)
);
/**/
CREATE TABLE student_exam(
	id INT AUTO_INCREMENT,
	studetId INT NOT NULL,
	examId INT NOT NULL,
	mark VARCHAR(10) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (studetId) REFERENCES student_account(id),
	FOREIGN KEY (examId) REFERENCES exam(id)
);
/**/
CREATE TABLE question_answer(
	id INT AUTO_INCREMENT,
	studentExamId INT NOT NULL,
	answer VARCHAR(120) NOT NULL,
	MCQId INT,
	TFId INT,
	PRIMARY KEY (id),
	FOREIGN KEY (studentExamId) REFERENCES student_exam(id),
	FOREIGN KEY (MCQId) REFERENCES MCQ(id),
	FOREIGN KEY (TFId) REFERENCES TF(id)
);
/*END*/
