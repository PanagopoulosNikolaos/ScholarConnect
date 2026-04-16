```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'background': '#000000', 'lineColor': '#ffffff'}}}%%
flowchart LR
    %% Diagram name: askbd

    %% Entities
    S[Student]
    P[Professor]
    C[Course]

    %% Relationships
    Eval{Evaluates}
    Enroll{Enrollment}
    Teach{Teaches}

    %% Entity-Relationship Connections (using longer lines to untangle)
    S ---- Eval
    Eval ----|"<font color='lightgreen'>o&lt;</font>"| P

    S ----|"<font color='lightgreen'>(1,M)</font>"| Enroll
    Enroll ----|"<font color='lightgreen'>(1,M) o&lt;</font>"| C

    P ----|"<font color='lightgreen'>|&lt;</font>"| Teach
    Teach ---- C

    %% Attributes S
    S_Name(["(Full Name)"])
    S_AM(["<u>Registration Number</u>"])
    S_User([Username])
    S_Pass([Password])
    S_Email([Email])

    S --- S_Name
    S --- S_AM
    S --- S_User
    S --- S_Pass
    S --- S_Email

    %% Attributes Eval
    Eval_Grade([Grade]):::shaded
    Eval_Comments([Comments]):::multivalued

    Eval --- Eval_Grade
    Eval --- Eval_Comments

    %% Attributes P
    P_Name(["(Full Name)"])
    P_FName([First Name])
    P_LName([Last Name])
    P_Email([Email])
    P_Spec([Specialization])
    P_AM(["<u>Registration Number</u>"])

    P --- P_Name
    P_Name --- P_FName
    P_Name --- P_LName
    P --- P_Email
    P --- P_Spec
    P --- P_AM

    %% Attributes Enroll
    Enroll_Grade([Grade])
    Enroll_Date([Date])

    Enroll --- Enroll_Grade
    Enroll --- Enroll_Date

    %% Attributes C
    C_Desc(["(Description)"])
    C_Cat([Category])
    C_Code(["<u>Course Code</u>"])
    C_Title([Title])

    C --- C_Desc
    C --- C_Cat
    C --- C_Code
    C --- C_Title

    %% Apply Classes to Entities and Relationships (Roots)
    class S,P,C,Eval,Enroll,Teach rootNode;

    %% Apply Classes to Attributes (Branches)
    class S_Name,S_AM,S_User,S_Pass,S_Email,P_Name,P_FName,P_LName,P_Email,P_Spec,P_AM,Enroll_Grade,Enroll_Date,C_Desc,C_Cat,C_Code,C_Title branchNode;

    %% Styling Definitions
    classDef rootNode fill:#0055ff,stroke:#fff,stroke-width:2px,color:#fff;
    classDef branchNode fill:#ffcc00,stroke:#333,stroke-width:2px,color:#000;
    classDef shaded fill:#cc9900,stroke:#333,stroke-width:2px,color:#000;
    classDef multivalued fill:#ffcc00,stroke:#333,stroke-width:4px,color:#000;
```

## SQL Schema

```sql
CREATE TABLE Students (
    /**
     * Stores information about students enrolled in the system.
     * 
     * Args:
     *     registration_number (VARCHAR): The unique student identifier.
     *     full_name (VARCHAR): The full name of the student.
     *     username (VARCHAR): Unique name used for authentication.
     *     password (VARCHAR): Securely stored credential for login.
     *     email (VARCHAR): Student's primary contact address.
     */
    registration_number VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Professors (
    /**
     * Stores information about academic faculty members.
     * 
     * Args:
     *     registration_number (VARCHAR): The unique professor identifier.
     *     first_name (VARCHAR): The professor's given name.
     *     last_name (VARCHAR): The professor's family name.
     *     email (VARCHAR): Professor's primary contact address.
     *     specialization (VARCHAR): The academic field of expertise.
     */
    registration_number VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    specialization VARCHAR(100)
);

CREATE TABLE Courses (
    /**
     * Stores information about the courses offered.
     * 
     * Args:
     *     course_code (VARCHAR): The unique course identifier.
     *     title (VARCHAR): The name of the course.
     *     category (VARCHAR): The department or category of the course.
     *     description (TEXT): A brief summary of course content.
     */
    course_code VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    description TEXT
);

CREATE TABLE Enrollments (
    /**
     * Manages the many-to-many relationship between students and courses.
     * 
     * Args:
     *     student_registration_number (VARCHAR): Reference to the student.
     *     course_code (VARCHAR): Reference to the course.
     *     grade (DECIMAL): The grade received by the student.
     *     enrollment_date (DATE): The date the student joined the course.
     */
    student_registration_number VARCHAR(20),
    course_code VARCHAR(20),
    grade DECIMAL(4, 2),
    enrollment_date DATE NOT NULL,
    PRIMARY KEY (student_registration_number, course_code),
    FOREIGN KEY (student_registration_number) REFERENCES Students(registration_number),  -- Ensures data integrity with the Students table.
    FOREIGN KEY (course_code) REFERENCES Courses(course_code)  -- Maintains a valid link to the existing Courses.
);

CREATE TABLE TeachingAssignments (
    /**
     * Manages the relationship between professors and the courses they teach.
     * 
     * Args:
     *     professor_registration_number (VARCHAR): Reference to the professor.
     *     course_code (VARCHAR): Reference to the course.
     */
    professor_registration_number VARCHAR(20),
    course_code VARCHAR(20),
    PRIMARY KEY (professor_registration_number, course_code),
    FOREIGN KEY (professor_registration_number) REFERENCES Professors(registration_number),
    FOREIGN KEY (course_code) REFERENCES Courses(course_code)
);

CREATE TABLE ProfessorEvaluations (
    /**
     * Records evaluations submitted by students for their professors.
     * 
     * Args:
     *     student_registration_number (VARCHAR): Reference to the student reviewer.
     *     professor_registration_number (VARCHAR): Reference to the professor being reviewed.
     *     grade (DECIMAL): The numeric score given to the professor.
     */
    student_registration_number VARCHAR(20),
    professor_registration_number VARCHAR(20),
    grade DECIMAL(4, 2),
    PRIMARY KEY (student_registration_number, professor_registration_number),
    FOREIGN KEY (student_registration_number) REFERENCES Students(registration_number),
    FOREIGN KEY (professor_registration_number) REFERENCES Professors(registration_number)
);

CREATE TABLE EvaluationComments (
    /**
     * Stores individual comments associated with a professor evaluation.
     * Handles the multivalued nature of evaluation comments.
     * 
     * Args:
     *     comment_id (INT): Unique identifier for the comment.
     *     student_registration_number (VARCHAR): Reference to the evaluator.
     *     professor_registration_number (VARCHAR): Reference to the professor.
     *     comment_text (TEXT): The feedback content provided.
     */
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_registration_number VARCHAR(20),
    professor_registration_number VARCHAR(20),
    comment_text TEXT NOT NULL,
    FOREIGN KEY (student_registration_number, professor_registration_number) 
        REFERENCES ProfessorEvaluations(student_registration_number, professor_registration_number)  -- Links comments to a specific evaluation instance.
);
```