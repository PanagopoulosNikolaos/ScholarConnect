from src.database import getConnection

# Allowed columns for course updates to prevent SQL errors and protect primary/foreign keys.
course_update_whitelist = {"Title", "Description", "Category", "AM_Instructor"}

def addCourse(c_code, title, description=None, category=None, am_instructor=None):
    """
    Inserts a new course record into the database.

    Args:
        c_code (str): The unique course identifier.
        title (str): The course's title.
        description (str, optional): The detailed explanation of the course. Defaults to None.
        category (str, optional): The classification group of the course. Defaults to None.
        am_instructor (str, optional): The unique identifier of the assigned instructor. Defaults to None.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO COURSE (C_Code, AM_Instructor, Title, Description, Category) VALUES (?, ?, ?, ?, ?)",
            (c_code, am_instructor, title, description, category)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding course: {e}")
        return False
    finally:
        conn.close()

def getCourse(c_code):
    """
    Retrieves a course record by its unique code.

    Args:
        c_code (str): The unique course identifier.

    Returns:
        dict: The course record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COURSE WHERE C_Code = ?", (c_code,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listCourses():
    """
    Retrieves all course records from the database.

    Returns:
        list: A list of dictionaries representing all courses.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COURSE")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateCourse(c_code, **kwargs):
    """
    Updates an existing course record, ignoring invalid keys.

    Args:
        c_code (str): The unique course identifier.
        **kwargs: Column names and their new values.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    filtered_data = {k: v for k, v in kwargs.items() if k in course_update_whitelist}  # Removes unpermitted attributes.
    
    if not filtered_data:
        return False
    
    conn = getConnection()
    try:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in filtered_data.keys()])  # Constructs the SQL set clause.
        values = list(filtered_data.values())
        values.append(c_code)
        
        cursor.execute(
            f"UPDATE COURSE SET {set_clause} WHERE C_Code = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating course: {e}")
        return False
    finally:
        conn.close()

def deleteCourse(c_code):
    """
    Deletes a course record from the database.

    Args:
        c_code (str): The unique course identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COURSE WHERE C_Code = ?", (c_code,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting course: {e}")
        return False
    finally:
        conn.close()
