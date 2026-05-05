PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Students (
    registration_number TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Professors (
    registration_number TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    specialization TEXT
);

CREATE TABLE IF NOT EXISTS Courses (
    course_code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Enrollments (
    student_registration_number TEXT NOT NULL,
    course_code TEXT NOT NULL,
    grade REAL,
    enrollment_date TEXT NOT NULL,
    PRIMARY KEY (student_registration_number, course_code),
    FOREIGN KEY (student_registration_number) REFERENCES Students(registration_number),
    FOREIGN KEY (course_code) REFERENCES Courses(course_code)
);

CREATE TABLE IF NOT EXISTS TeachingAssignments (
    professor_registration_number TEXT NOT NULL,
    course_code TEXT NOT NULL,
    PRIMARY KEY (professor_registration_number, course_code),
    FOREIGN KEY (professor_registration_number) REFERENCES Professors(registration_number),
    FOREIGN KEY (course_code) REFERENCES Courses(course_code)
);

CREATE TABLE IF NOT EXISTS ProfessorEvaluations (
    student_registration_number TEXT NOT NULL,
    professor_registration_number TEXT NOT NULL,
    grade REAL,
    PRIMARY KEY (student_registration_number, professor_registration_number),
    FOREIGN KEY (student_registration_number) REFERENCES Students(registration_number),
    FOREIGN KEY (professor_registration_number) REFERENCES Professors(registration_number)
);

CREATE TABLE IF NOT EXISTS EvaluationComments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_registration_number TEXT NOT NULL,
    professor_registration_number TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    FOREIGN KEY (student_registration_number, professor_registration_number)
        REFERENCES ProfessorEvaluations(student_registration_number, professor_registration_number)
);
