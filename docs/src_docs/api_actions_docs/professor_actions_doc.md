# professor_actions.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [addProfessor](#addprofessor) | Function | Inserts a new instructor record into the database. |
| [getProfessor](#getprofessor) | Function | Retrieves an instructor record by their registration number. |
| [listProfessors](#listprofessors) | Function | Retrieves all instructor records from the database. |
| [updateProfessor](#updateprofessor) | Function | Updates an existing instructor record, ignoring invalid keys. |
| [deleteProfessor](#deleteprofessor) | Function | Deletes an instructor record from the database. |

## Overview
This file handles the database CRUD (Create, Read, Update, Delete) operations for the `INSTRUCTOR` table. It provides a standardized data access layer preventing SQL injection and enforcing data integrity, while abstracting the connection logic via a helper module.

## Detailed Breakdown

### addProfessor

**Signature:**
```python
def addProfessor(AM, Password, FirstName, LastName, email, Specialization)
```

**Purpose:** Inserts a new instructor record into the database. Username is set to AM internally.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique instructor identifier. |
| Password | str | Yes | — | Securely stored credential for login. |
| FirstName | str | Yes | — | The instructor's given name. |
| LastName | str | Yes | — | The instructor's family name. |
| email | str | Yes | — | Instructor's primary contact address. |
| Specialization | str | Yes | — | The academic field of expertise. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def addProfessor(AM, Password, FirstName, LastName, email, Specialization):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO INSTRUCTOR (AM, Password, Username, FirstName, LastName, email, Specialization) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (AM, Password, AM, FirstName, LastName, email, Specialization)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding instructor: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def addProfessor(...)` — Accepts instructor details.
* **Line 1:** `conn = getConnection()` — Acquires a database connection.
* **Line 4:** `cursor.execute(...)` — Executes the SQL INSERT statement, intentionally mapping the Username column to the AM parameter.
* **Line 8:** `conn.commit()` — Persists the transaction.
* **Line 11:** `print(f"Error... {e}")` — Catches and logs exceptions to prevent crash.
* **Line 14:** `conn.close()` — Releases the connection back to the system.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### getProfessor

**Signature:**
```python
def getProfessor(AM)
```

**Purpose:** Retrieves an instructor record by their registration number.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique instructor identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict \| None | The instructor record as a dictionary, or None if not found. |

**Source Code:**
```python
def getProfessor(AM):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INSTRUCTOR WHERE AM = ?", (AM,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def getProfessor(AM):` — Accepts unique identifier for lookup.
* **Line 1:** `conn = getConnection()` — Opens connection to SQLite.
* **Line 4:** `cursor.execute(...)` — Fetches the requested record safely mapping AM.
* **Line 5:** `row = cursor.fetchone()` — Retrieves the first matching record.
* **Line 6:** `return dict(row) if row else None` — Casts SQLite row to python dictionary if it exists.
* **Line 8:** `conn.close()` — Safely tears down the connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### listProfessors

**Signature:**
```python
def listProfessors()
```

**Purpose:** Retrieves all instructor records from the database.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|

**Returns:**
| Type | Description |
|------|-------------|
| list | A list of dictionaries representing all instructors. |

**Source Code:**
```python
def listProfessors():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INSTRUCTOR")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def listProfessors():` — Parameterless retrieval trigger.
* **Line 1:** `conn = getConnection()` — Initializes db access.
* **Line 4:** `cursor.execute("SELECT * FROM INSTRUCTOR")` — Runs absolute fetch.
* **Line 5:** `rows = cursor.fetchall()` — Buffers entire result set into memory.
* **Line 6:** `return [dict(row) for row in rows]` — Converts row results into a list of dictionaries.
* **Line 8:** `conn.close()` — Closes active connection block.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### updateProfessor

**Signature:**
```python
def updateProfessor(AM, **kwargs)
```

**Purpose:** Updates an existing instructor record, ignoring invalid keys.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique instructor identifier. |
| kwargs | dict | No | — | Column names and their new values. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def updateProfessor(AM, **kwargs):
    filtered_data = {k: v for k, v in kwargs.items() if k in PROFESSOR_UPDATE_WHITELIST}

    if not filtered_data:
        return False

    conn = getConnection()
    try:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in filtered_data.keys()])
        values = list(filtered_data.values())
        values.append(AM)

        cursor.execute(
            f"UPDATE INSTRUCTOR SET {set_clause} WHERE AM = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating instructor: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def updateProfessor(AM, **kwargs):` — Takes AM and arbitrary dictionary variables.
* **Line 1:** `filtered_data = ...` — Filters kwargs dynamically against `PROFESSOR_UPDATE_WHITELIST`.
* **Line 3:** `if not filtered_data:` — Checks if the payload is empty after sanitization, preventing faulty SQL formatting.
* **Line 9:** `set_clause = ...` — Constructs SQL Set parameters by joining dictionary keys.
* **Line 10:** `values = list(...)` — Prepares variable bind inputs.
* **Line 11:** `values.append(AM)` — Completes payload adding the primary key for WHERE constraints.
* **Line 13:** `cursor.execute(...)` — Issues dynamic UPDATE transaction.
* **Line 17:** `conn.commit()` — Stores updates cleanly.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |


### deleteProfessor

**Signature:**
```python
def deleteProfessor(AM)
```

**Purpose:** Deletes an instructor record from the database.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| AM | str | Yes | — | The unique instructor identifier to delete. |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the operation was successful, False otherwise. |

**Source Code:**
```python
def deleteProfessor(AM):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM INSTRUCTOR WHERE AM = ?", (AM,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting instructor: {e}")
        return False
    finally:
        conn.close()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def deleteProfessor(AM):` — Identifies target by AM.
* **Line 1:** `conn = getConnection()` — Creates link instance.
* **Line 4:** `cursor.execute(...)` — Removes the target row matching AM securely.
* **Line 5:** `conn.commit()` — Enacts the table deletion.
* **Line 6:** `return cursor.rowcount > 0` — Yields truth value checking if deletion occurred.
* **Line 10:** `conn.close()` — Closes the connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getConnection | External | Establish database link | src.database |
