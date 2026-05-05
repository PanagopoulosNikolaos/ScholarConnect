from src.database import getConnection

# Allowed columns for student updates to prevent SQL errors and protect the primary key.
STUDENT_UPDATE_WHITELIST = {"full_name", "username", "password", "email"}

def addStudent(registration_number, full_name, username, password, email):
    """
    Inserts a new student record into the database.

    Args:
        registration_number (str): The unique student identifier.
        full_name (str): The full name of the student.
        username (str): Unique name used for authentication.
        password (str): Securely stored credential for login.
        email (str): Student's primary contact address.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Students (registration_number, full_name, username, password, email) VALUES (?, ?, ?, ?, ?)",
            (registration_number, full_name, username, password, email)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        return False
    finally:
        conn.close()

def getStudent(registration_number):
    """
    Retrieves a student record by their registration number.

    Args:
        registration_number (str): The unique student identifier.

    Returns:
        dict: The student record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students WHERE registration_number = ?", (registration_number,))
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
        cursor.execute("SELECT * FROM Students")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateStudent(registration_number, **kwargs):
    """
    Updates an existing student record, ignoring invalid keys.

    Args:
        registration_number (str): The unique student identifier.
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
        values.append(registration_number)
        
        cursor.execute(
            f"UPDATE Students SET {set_clause} WHERE registration_number = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating student: {e}")
        return False
    finally:
        conn.close()

def deleteStudent(registration_number):
    """
    Deletes a student record from the database.

    Args:
        registration_number (str): The unique student identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Students WHERE registration_number = ?", (registration_number,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting student: {e}")
        return False
    finally:
        conn.close()
