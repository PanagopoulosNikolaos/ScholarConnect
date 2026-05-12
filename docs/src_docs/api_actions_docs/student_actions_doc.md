# student_actions.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [addStudent](#addstudent) | Function | Inserts a new student record into the database. |
| [getStudent](#getstudent) | Function | Retrieves a student record by their registration number. |
| [listStudents](#liststudents) | Function | Retrieves all student records from the database. |
| [updateStudent](#updatestudent) | Function | Updates an existing student record, ignoring invalid keys. |
| [deleteStudent](#deletestudent) | Function | Deletes a student record from the database. |

## Overview
This file manages the primary Data Access Object (DAO) behaviors for the `STUDENT` table inside SQLite. It handles the CRUD logic, prevents injection vulnerabilities via parameterized statements, and enforces strict update filtering to prevent ID tampering.

## Detailed Breakdown

### addStudent

**Signature:**
```python
def addStudent(AM, Password, email, FirstName, LastName)
```

**Purpose:** Inserts a new student record into the database. Username is set to AM internally.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique student identifier. |
| Password | str | Yes | — | Securely stored credential for login. |
| email | str | Yes | — | Student's primary contact address. |
| FirstName | str | Yes | — | The student's given name. |
| LastName | str | Yes | — | The student's family name. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def addStudent(AM, Password, email, FirstName, LastName):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO STUDENT (AM, Password, Username, email, FirstName, LastName) VALUES (?, ?, ?, ?, ?, ?)",
            (AM, Password, AM, email, FirstName, LastName)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def addStudent(...)` — Parameter intake for student model.
* **Line 1:** `conn = getConnection()` — Boots sqlite connection context.
* **Line 4:** `cursor.execute(...)` — Executes SQL query substituting AM parameter directly into both the AM and Username schema columns.
* **Line 8:** `conn.commit()` — Writes changes back to database file.
* **Line 11:** `print(...)` — Handles insertion violation constraints safely.
* **Line 14:** `conn.close()` — Connection shutdown.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### getStudent

**Signature:**
```python
def getStudent(AM)
```

**Purpose:** Retrieves a student record by their registration number.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique student identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict \| None | The student record as a dictionary, or None if not found. |

**Source Code:**
```python
def getStudent(AM):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT WHERE AM = ?", (AM,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def getStudent(AM):` — Accepts unique query AM.
* **Line 1:** `conn = getConnection()` — Establishes database socket.
* **Line 4:** `cursor.execute(...)` — Issues parameter bound SQL SELECT querying rows via unique ID.
* **Line 5:** `row = cursor.fetchone()` — Processes response matrix grabbing single index result.
* **Line 6:** `return dict(row) if row else None` — Casts memory mapping to standard dict object returning None upon query failure.
* **Line 8:** `conn.close()` — Releases sqlite state.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### listStudents

**Signature:**
```python
def listStudents()
```

**Purpose:** Retrieves all student records from the database.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|

**Returns:**
| Type | Description |
|------|-------------|
| list | A list of dictionaries representing all students. |

**Source Code:**
```python
def listStudents():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def listStudents():` — Function invocation entry.
* **Line 1:** `conn = getConnection()` — Triggers SQLite connection interface.
* **Line 4:** `cursor.execute("SELECT * FROM STUDENT")` — Pulls data structure unconditionally for UI/Table ingestion.
* **Line 5:** `rows = cursor.fetchall()` — Materializes memory buffers of fetched matrix blocks.
* **Line 6:** `return [dict(row) for row in rows]` — Rebuilds objects into generic python list wrapping dict instances.
* **Line 8:** `conn.close()` — Executes DB termination safely closing access stream.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### updateStudent

**Signature:**
```python
def updateStudent(AM, **kwargs)
```

**Purpose:** Updates an existing student record, ignoring invalid keys.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique student identifier. |
| kwargs | dict | No | — | Column names and their new values. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def updateStudent(AM, **kwargs):
    filtered_data = {k: v for k, v in kwargs.items() if k in STUDENT_UPDATE_WHITELIST}

    if not filtered_data:
        return False

    conn = getConnection()
    try:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in filtered_data.keys()])
        values = list(filtered_data.values())
        values.append(AM)

        cursor.execute(
            f"UPDATE STUDENT SET {set_clause} WHERE AM = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating student: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def updateStudent(AM, **kwargs):` — Takes explicit target via kwargs arguments logic pattern.
* **Line 1:** `filtered_data = ...` — Validates arbitrary parameters with `STUDENT_UPDATE_WHITELIST`.
* **Line 3:** `if not filtered_data:` — Halts early upon whitelist validation failures protecting SQLite structure injections.
* **Line 9:** `set_clause = ...` — Pre-compiles SQL template syntax string combining keys.
* **Line 10:** `values = list(...)` — Builds parameterized variables resolving data sanitization.
* **Line 11:** `values.append(AM)` — Attaches ID to variables payload explicitly mapped for UPDATE WHERE condition matching.
* **Line 13:** `cursor.execute(...)` — Binds query strings to execution variables updating existing registry block.
* **Line 17:** `conn.commit()` — Savepoint triggering.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### deleteStudent

**Signature:**
```python
def deleteStudent(AM)
```

**Purpose:** Deletes a student record from the database.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique student identifier to delete. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def deleteStudent(AM):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STUDENT WHERE AM = ?", (AM,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting student: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def deleteStudent(AM):` — Invoked query function targeting student AM.
* **Line 1:** `conn = getConnection()` — Resolves connection handler.
* **Line 4:** `cursor.execute(...)` — Triggers DELETE SQL command resolving target id securely matching query row object.
* **Line 5:** `conn.commit()` — Performs persistent change onto primary database file.
* **Line 6:** `return cursor.rowcount > 0` — Converts integer returned mapping to boolean result validating successfully destroyed entries.
* **Line 10:** `conn.close()` — Closes the SQLite instance link.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |
