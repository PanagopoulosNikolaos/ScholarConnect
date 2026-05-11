from src.database import getConnection

# Allowed columns for enrollment updates. Note that primary keys cannot be updated.
enrollment_update_whitelist = {"StartDate"}

def addEnrollment(am_student, c_code, start_date):
    """
    Inserts a new enrollment record into the database.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.
        start_date (str): The date when the enrollment begins.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ENROLLMENT (AM_Student, C_Code, StartDate) VALUES (?, ?, ?)",
            (am_student, c_code, start_date)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding enrollment: {e}")
        return False
    finally:
        conn.close()

def getEnrollment(am_student, c_code):
    """
    Retrieves an enrollment record by student and course identifiers.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.

    Returns:
        dict: The enrollment record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENROLLMENT WHERE AM_Student = ? AND C_Code = ?", (am_student, c_code))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listEnrollments():
    """
    Retrieves all enrollment records from the database.

    Returns:
        list: A list of dictionaries representing all enrollments.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENROLLMENT")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateEnrollment(am_student, c_code, **kwargs):
    """
    Updates an existing enrollment record, ignoring invalid keys.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.
        **kwargs: Column names and their new values.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    filtered_data = {k: v for k, v in kwargs.items() if k in enrollment_update_whitelist}  # Restricts updates to safe columns.
    
    if not filtered_data:
        return False
    
    conn = getConnection()
    try:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in filtered_data.keys()])  # Generates SET conditions dynamically.
        values = list(filtered_data.values())
        values.extend([am_student, c_code])
        
        cursor.execute(
            f"UPDATE ENROLLMENT SET {set_clause} WHERE AM_Student = ? AND C_Code = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating enrollment: {e}")
        return False
    finally:
        conn.close()

def deleteEnrollment(am_student, c_code):
    """
    Deletes an enrollment record from the database.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ENROLLMENT WHERE AM_Student = ? AND C_Code = ?", (am_student, c_code))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting enrollment: {e}")
        return False
    finally:
        conn.close()
