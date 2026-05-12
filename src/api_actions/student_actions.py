from src.database import getConnection

# Allowed columns for student updates to prevent SQL errors and protect the primary key.
# Username is intentionally excluded because it mirrors AM.
STUDENT_UPDATE_WHITELIST = {"FirstName", "LastName", "Password", "email"}

def addStudent(AM, Password, email, FirstName, LastName):
    """
    Inserts a new student record into the database.  Username is set to AM internally.

    Args:
        AM (str): The unique student identifier.
        Password (str): Securely stored credential for login.
        email (str): Student's primary contact address.
        FirstName (str): The student's given name.
        LastName (str): The student's family name.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
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

def getStudent(AM):
    """
    Retrieves a student record by their registration number.

    Args:
        AM (str): The unique student identifier.

    Returns:
        dict: The student record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT WHERE AM = ?", (AM,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listStudents():
    """
    Retrieves all student records from the database.

    Returns:
        list: A list of dictionaries representing all students.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateStudent(AM, **kwargs):
    """
    Updates an existing student record, ignoring invalid keys.

    Args:
        AM (str): The unique student identifier.
        **kwargs: Column names and their new values.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    # Filter kwargs against the whitelist.
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

def deleteStudent(AM):
    """
    Deletes a student record from the database.

    Args:
        AM (str): The unique student identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
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