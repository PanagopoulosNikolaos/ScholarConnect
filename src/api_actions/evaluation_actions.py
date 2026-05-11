from src.database import getConnection

# Allowed columns for evaluation updates.
evaluation_update_whitelist = {"Rating", "Comments"}

def addEvaluation(am_instructor, am_student, c_code, rating=None, comments=None):
    """
    Inserts a new evaluation record into the database.

    Args:
        am_instructor (str): The unique instructor identifier.
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.
        rating (int, optional): The numerical score assigned. Defaults to None.
        comments (str, optional): The textual feedback provided. Defaults to None.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO EVALUATION (AM_Instructor, AM_Student, C_Code, Rating, Comments) VALUES (?, ?, ?, ?, ?)",
            (am_instructor, am_student, c_code, rating, comments)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding evaluation: {e}")
        return False
    finally:
        conn.close()

def getEvaluation(am_instructor, am_student, c_code):
    """
    Retrieves an evaluation record by instructor, student, and course identifiers.

    Args:
        am_instructor (str): The unique instructor identifier.
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.

    Returns:
        dict: The evaluation record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EVALUATION WHERE AM_Instructor = ? AND AM_Student = ? AND C_Code = ?", (am_instructor, am_student, c_code))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listEvaluations():
    """
    Retrieves all evaluation records from the database.

    Returns:
        list: A list of dictionaries representing all evaluations.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EVALUATION")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateEvaluation(am_instructor, am_student, c_code, **kwargs):
    """
    Updates an existing evaluation record, ignoring invalid keys.

    Args:
        am_instructor (str): The unique instructor identifier.
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.
        **kwargs: Column names and their new values.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    filtered_data = {k: v for k, v in kwargs.items() if k in evaluation_update_whitelist}  # Extracts only valid fields for modification.
    
    if not filtered_data:
        return False
    
    conn = getConnection()
    try:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in filtered_data.keys()])  # Formats attributes for SQL insertion.
        values = list(filtered_data.values())
        values.extend([am_instructor, am_student, c_code])
        
        cursor.execute(
            f"UPDATE EVALUATION SET {set_clause} WHERE AM_Instructor = ? AND AM_Student = ? AND C_Code = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating evaluation: {e}")
        return False
    finally:
        conn.close()

def deleteEvaluation(am_instructor, am_student, c_code):
    """
    Deletes an evaluation record from the database.

    Args:
        am_instructor (str): The unique instructor identifier.
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EVALUATION WHERE AM_Instructor = ? AND AM_Student = ? AND C_Code = ?", (am_instructor, am_student, c_code))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting evaluation: {e}")
        return False
    finally:
        conn.close()
