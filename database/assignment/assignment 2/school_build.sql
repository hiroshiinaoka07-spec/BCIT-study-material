-- ACIT 3910 Assignment 2
-- Run as root inside the Ubuntu VM:
--   mysql -u root -p < school_build.sql
-- If root uses socket auth (Access denied with -p):
--   sudo mysql < school_build.sql

DROP USER IF EXISTS
    'Ally'@'%', 'Evangelica'@'%', 'Ema'@'%', 'Zed'@'%', 'Tulio'@'%',
    'Collyn'@'%', 'Linnea'@'%', 'Jayson'@'%', 'Duston'@'%', 'Chen'@'%';

DROP ROLE IF EXISTS 'student', 'instructor';

DROP DATABASE IF EXISTS school;
CREATE DATABASE school;
USE school;

CREATE TABLE student (
    student_id    INT         NOT NULL AUTO_INCREMENT,
    first_name    VARCHAR(45) NOT NULL,
    last_name     VARCHAR(45) NOT NULL,
    date_of_birth DATE        NOT NULL,
    PRIMARY KEY (student_id)
) ENGINE=InnoDB;

CREATE TABLE instructor (
    instructor_id INT         NOT NULL AUTO_INCREMENT,
    first_name    VARCHAR(45) NOT NULL,
    last_name     VARCHAR(45) NOT NULL,
    date_of_birth DATE        NOT NULL,
    PRIMARY KEY (instructor_id)
) ENGINE=InnoDB;

CREATE TABLE course (
    course_id   INT          NOT NULL AUTO_INCREMENT,
    course_code VARCHAR(10)  NOT NULL,
    start_date  DATE         NULL,
    end_date    DATE         NULL,
    description VARCHAR(100) NULL,
    PRIMARY KEY (course_id)
) ENGINE=InnoDB;

CREATE TABLE course_instructor (
    course_instructor_id INT NOT NULL AUTO_INCREMENT,
    frn_course_id        INT NOT NULL,
    frn_instructor_id    INT NOT NULL,
    PRIMARY KEY (course_instructor_id),
    CONSTRAINT fk_course_instructor_course
        FOREIGN KEY (frn_course_id) REFERENCES course (course_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_course_instructor_instructor
        FOREIGN KEY (frn_instructor_id) REFERENCES instructor (instructor_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE course_student (
    course_student_id INT NOT NULL AUTO_INCREMENT,
    frn_course_id     INT NOT NULL,
    frn_student_id    INT NOT NULL,
    PRIMARY KEY (course_student_id),
    CONSTRAINT fk_course_student_course
        FOREIGN KEY (frn_course_id) REFERENCES course (course_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_course_student_student
        FOREIGN KEY (frn_student_id) REFERENCES student (student_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE grade (
    grade_id       INT          NOT NULL AUTO_INCREMENT,
    frn_course_id  INT          NOT NULL,
    frn_student_id INT          NOT NULL,
    grade_percent  DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (grade_id),
    CONSTRAINT fk_grade_course
        FOREIGN KEY (frn_course_id) REFERENCES course (course_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_grade_student
        FOREIGN KEY (frn_student_id) REFERENCES student (student_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB;

INSERT INTO student (student_id, first_name, last_name, date_of_birth) VALUES
(1, 'Ally',       'Brannon',  '1997-05-06'),
(2, 'Evangelica', 'Cruz',     '1998-04-21'),
(3, 'Ema',        'Kimberly', '2000-01-18'),
(4, 'Zed',        'Notaro',   '1999-10-01'),
(5, 'Tulio',      'Steffen',  '1998-08-08');

INSERT INTO instructor (instructor_id, first_name, last_name, date_of_birth) VALUES
(1, 'Collyn', 'Kistner',    '1985-07-24'),
(2, 'Linnea', 'Nosek',      '1975-12-30'),
(3, 'Jayson', 'Phelps',     '1976-12-17'),
(4, 'Duston', 'Bunschoten', '1981-08-11'),
(5, 'Chen',   'Esparza',    '1982-02-02');

INSERT INTO course (course_id, course_code, start_date, end_date, description) VALUES
(1, 'BIO 111',  '2018-01-05', '2018-04-15', 'Introduction to Animal Biology'),
(2, 'BIO 112',  '2018-01-05', '2018-04-15', 'Introduction to Plant Biology'),
(3, 'CHEM 121', '2018-01-05', '2018-04-15', 'Organic Chemistry'),
(4, 'MATH 152', '2018-01-05', '2018-04-15', 'Calculus 1'),
(5, 'MATH 155', '2018-01-05', '2018-04-15', 'Calculus 2');

INSERT INTO course_instructor (course_instructor_id, frn_course_id, frn_instructor_id) VALUES
(1, 1, 2),
(2, 2, 2),
(3, 3, 5),
(4, 3, 3),
(5, 4, 4),
(6, 5, 1);

INSERT INTO course_student (course_student_id, frn_course_id, frn_student_id) VALUES
(1,  1, 1),
(2,  1, 2),
(3,  2, 1),
(4,  3, 2),
(5,  3, 4),
(6,  4, 4),
(7,  5, 5),
(8,  3, 5),
(9,  2, 3),
(10, 3, 3),
(11, 4, 3);

INSERT INTO grade (grade_id, frn_course_id, frn_student_id, grade_percent) VALUES
(1,  1, 1, 95.10),
(2,  1, 2, 88.30),
(3,  2, 1, 92.00),
(4,  3, 2, 78.90),
(5,  3, 4, 75.30),
(6,  4, 4, 82.30),
(7,  5, 5, 74.10),
(8,  3, 5, 90.80),
(9,  2, 3, 82.60),
(10, 3, 3, 79.10),
(11, 4, 3, 85.00);

CREATE SQL SECURITY DEFINER VIEW my_grades AS
SELECT
    s.first_name,
    s.last_name,
    c.course_code,
    g.grade_percent
FROM grade AS g
JOIN student AS s ON g.frn_student_id = s.student_id
JOIN course  AS c ON g.frn_course_id  = c.course_id
WHERE s.first_name = SUBSTRING_INDEX(USER(), '@', 1);

CREATE SQL SECURITY DEFINER VIEW student_schedule AS
SELECT
    s.first_name,
    s.last_name,
    c.course_code,
    c.start_date,
    c.end_date
FROM course_student AS cs
JOIN student AS s ON cs.frn_student_id = s.student_id
JOIN course  AS c ON cs.frn_course_id  = c.course_id
WHERE s.first_name = SUBSTRING_INDEX(USER(), '@', 1);

CREATE SQL SECURITY DEFINER VIEW instructor_schedule AS
SELECT
    i.first_name,
    i.last_name,
    c.course_code,
    c.start_date,
    c.end_date
FROM course_instructor AS ci
JOIN instructor AS i ON ci.frn_instructor_id = i.instructor_id
JOIN course     AS c ON ci.frn_course_id     = c.course_id
WHERE i.first_name = SUBSTRING_INDEX(USER(), '@', 1);

DELIMITER $$

CREATE PROCEDURE check_grade_percent(IN grade_value DECIMAL(5,2))
BEGIN
    DECLARE grade_text VARCHAR(20);
    DECLARE msg VARCHAR(128);

    SET grade_text = TRIM(TRAILING '.' FROM TRIM(TRAILING '0' FROM CAST(grade_value AS CHAR)));

    IF grade_value < 0 THEN
        SET msg = CONCAT(
            'Check constraint on grade.grade_percent failed - grade_percent ',
            grade_text,
            ' must be greater than 0%.'
        );
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;

    IF grade_value > 100 THEN
        SET msg = CONCAT(
            'Check constraint on grade.grade_percent failed - grade_percent ',
            grade_text,
            ' must not be larger than 100%.'
        );
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END$$

CREATE TRIGGER grade_before_insert
BEFORE INSERT ON grade
FOR EACH ROW
BEGIN
    CALL check_grade_percent(NEW.grade_percent);
END$$

CREATE TRIGGER grade_before_update
BEFORE UPDATE ON grade
FOR EACH ROW
BEGIN
    CALL check_grade_percent(NEW.grade_percent);
END$$

DELIMITER ;

-- Roles must be real roles. The verify script looks in mysql.user for
-- student and instructor with an empty password, locked, password expired.
CREATE ROLE 'student', 'instructor';

GRANT SELECT ON school.my_grades TO 'student';
GRANT SELECT ON school.student_schedule TO 'student';

GRANT SELECT, INSERT, UPDATE, DELETE ON school.student TO 'instructor';
GRANT SELECT, INSERT, UPDATE, DELETE ON school.instructor TO 'instructor';
GRANT SELECT, INSERT, UPDATE, DELETE ON school.course TO 'instructor';
GRANT SELECT, INSERT, UPDATE, DELETE ON school.course_instructor TO 'instructor';
GRANT SELECT, INSERT, UPDATE, DELETE ON school.course_student TO 'instructor';
GRANT SELECT, INSERT, UPDATE, DELETE ON school.grade TO 'instructor';
GRANT SELECT ON school.instructor_schedule TO 'instructor';

-- Host is '%' because "SHOW GRANTS FOR 'Ally'" means Ally@'%'.
CREATE USER 'Ally'@'%'       IDENTIFIED BY 'password';
CREATE USER 'Evangelica'@'%' IDENTIFIED BY 'password';
CREATE USER 'Ema'@'%'        IDENTIFIED BY 'password';
CREATE USER 'Zed'@'%'        IDENTIFIED BY 'password';
CREATE USER 'Tulio'@'%'      IDENTIFIED BY 'password';

CREATE USER 'Collyn'@'%' IDENTIFIED BY 'password';
CREATE USER 'Linnea'@'%' IDENTIFIED BY 'password';
CREATE USER 'Jayson'@'%' IDENTIFIED BY 'password';
CREATE USER 'Duston'@'%' IDENTIFIED BY 'password';
CREATE USER 'Chen'@'%'   IDENTIFIED BY 'password';

GRANT 'student' TO
    'Ally'@'%', 'Evangelica'@'%', 'Ema'@'%', 'Zed'@'%', 'Tulio'@'%';

GRANT 'instructor' TO
    'Collyn'@'%', 'Linnea'@'%', 'Jayson'@'%', 'Duston'@'%', 'Chen'@'%';

SET DEFAULT ROLE ALL TO
    'Ally'@'%', 'Evangelica'@'%', 'Ema'@'%', 'Zed'@'%', 'Tulio'@'%',
    'Collyn'@'%', 'Linnea'@'%', 'Jayson'@'%', 'Duston'@'%', 'Chen'@'%';
