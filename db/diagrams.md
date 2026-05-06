## Database Diagrams

### Conceptual ER Diagram (Chen Notation)
```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'background': '#000000', 'lineColor': '#ffffff'}, 'flowchart': {'curve': 'step', 'defaultRenderer': 'elk'}}}%%
flowchart LR
    %% Entities
    S[Student]
    P[Instructor]
    C[Course]

    %% Entity-Relationship Connections
    S ---|"N"| Enroll{Enrolls}
    S ---|"N"| Eval{Evaluates}
    Enroll ---|"M"| C
    Eval ---|"M"| P
    Eval ---|"1"| C
    P ---|"1"| Teach{Teaches}
    Teach ---|"N"| C

    %% Attributes Student
    S_User([Username]) --- S
    S_Name(["(Full Name)"]) --- S
    S_FName([First Name]) --- S_Name
    S_LName([Last Name]) --- S_Name
    S_Pass([Password]) --- S
    S_Email([Email]) --- S
    S_AM(["<u>Registration Number (AM)</u>"]) --- S

    %% Attributes Instructor/Professor
    P --- P_AM(["<u>Registration Number (AM)</u>"])
    P --- P_User([Username])
    P --- P_Name(["(Full Name)"])
    P_Name --- P_FName([First Name])
    P_Name --- P_LName([Last Name])
    P --- P_Email([Email])
    P --- P_Spec([Specialization])
    P --- P_Pass([Password])

    %% Attributes Course
    C --- C_Title([Title])
    C --- C_Code(["<u>Course Code</u>"])
    C --- C_Desc([Description])
    C --- C_Cat([Category])

    %% Attributes Relationships
    Eval --- Eval_Grade([Rating])
    Eval --- Eval_Comments([Comments])
    Enroll --- Enroll_Date([Start Date])

    %% Apply Classes to Entities and Relationships (Roots)
    class S,P,C,Eval,Enroll,Teach rootNode;

    %% Apply Classes to Attributes (Branches)
    class S_User,S_Name,S_FName,S_LName,S_Pass,S_Email,S_AM,P_AM,P_User,P_Name,P_FName,P_LName,P_Email,P_Pass,P_Spec,C_Title,C_Code,C_Desc,C_Cat,Eval_Grade,Eval_Comments,Enroll_Date branchNode;

    %% Styling Definitions
    classDef rootNode fill:#0055ff,stroke:#fff,stroke-width:2px,color:#fff;
    classDef branchNode fill:#ffcc00,stroke:#333,stroke-width:2px,color:#000;
```

### Schema Hierarchy View

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'background': '#000000',
    'lineColor': '#ffffff',
    'primaryColor': '#0055ff',
    'primaryBorderColor': '#ffffff',
    'primaryTextColor': '#ffffff',
    'secondaryColor': '#ffcc00',
    'tertiaryColor': '#e6b800',
    'mainBkg': '#001a33',
    'nodeBorder': '#0055ff'
  },
  'flowchart': {
    'curve': 'step',
    'defaultRenderer': 'elk'
  }
}}%%
flowchart TD
 
    db_root["ScholarConnect Database"]
    
    %% Primary Binary Split
    db_root --> users_branch["User Entities"]
    db_root --> academic_branch["Academic Content"]
    
    %% User Entities Branch
    users_branch --> student_node["STUDENT<br/>---<br/>AM (PK)<br/> Password<br/>Username (UK)<br/>email (UK)<br/>FirstName<br/>LastName"]
    users_branch --> instructor_node["INSTRUCTOR<br/>---<br/>AM (PK)<br/> Password<br/>Username (UK)<br/>FirstName<br/>LastName<br/>email (UK)<br/>Specialization"]
    
    %% Academic Content Branch
    academic_branch --> course_node["COURSE<br/>---<br/>C_Code (PK)<br/>AM_Instructor (FK)<br/> Title<br/> Description<br/> Category"]
    academic_branch --> engagement_branch["Course Engagement"]
    
    %% Engagement Branch 
    engagement_branch --> enrollment_node["ENROLLMENT<br/>---<br/>AM_Student (PK, FK)<br/>C_Code (PK, FK)<br/>StartDate"]
    engagement_branch --> evaluation_node["EVALUATION<br/>---<br/>AM_Instructor (PK, FK)<br/>AM_Student (PK, FK)<br/>C_Code (PK, FK)<br/>Rating<br/>Comments"]

    %% Relational Connections | (Orthogonal Dotted Lines) `-.->`
    student_node -.->|registers| enrollment_node
    course_node -.->|has| enrollment_node
    student_node -.->|submits| evaluation_node
    instructor_node -.->|receives| evaluation_node
    instructor_node -.->|teaches| course_node

    %% Styling and Aesthetics
    classDef default fill:#001a33,stroke:#0055ff,stroke-width:2px,color:#ffffff;
    classDef branch fill:#332200,stroke:#ffcc00,stroke-width:2px,color:#ffffff;
    
    class users_branch,academic_branch,engagement_branch branch;
    class db_root fill:#000000,stroke:#ffffff,stroke-width:3px;
```

### Relational Schema (Crow's Foot Notation)

```mermaid
erDiagram
    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "includes"
    STUDENT ||--o{ EVALUATION : "submits"
    INSTRUCTOR ||--o{ EVALUATION : "receives"
    COURSE ||--o{ EVALUATION : "receives"
    INSTRUCTOR ||--o{ COURSE : "teaches"

    STUDENT {
        VARCHAR(20) AM PK
        VARCHAR(255) Password
        VARCHAR(50) Username UK
        VARCHAR(100) email UK
        VARCHAR(50) FirstName
        VARCHAR(50) LastName
    }
    
    INSTRUCTOR {
        VARCHAR(20) AM PK
        VARCHAR(255) Password
        VARCHAR(50) Username UK
        VARCHAR(50) FirstName
        VARCHAR(50) LastName
        VARCHAR(100) email UK
        VARCHAR(100) Specialization
    }

    COURSE {
        VARCHAR(20) C_Code PK
        VARCHAR(20) AM_Instructor FK
        VARCHAR(100) Title
        TEXT Description
        VARCHAR(50) Category
    }

    ENROLLMENT {
        VARCHAR(20) AM_Student PK,FK
        VARCHAR(20) C_Code PK,FK
        DATE StartDate
    }

    EVALUATION {
        VARCHAR(20) AM_Instructor PK,FK
        VARCHAR(20) AM_Student PK,FK
        VARCHAR(20) C_Code PK,FK
        INTEGER Rating
        TEXT Comments
    }
```

#### Legend / Abbreviations
* **PK** - Primary Key
* **FK** - Foreign Key
* **UK** - Unique Key

---

#### The executable schema code is in the file: [`schema.sql`](./schema.sql).
