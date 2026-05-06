from src.database import getConnection

# Allowed columns for professor updates to prevent SQL errors and protect the primary key.
PROFESSOR_UPDATE_WHITELIST = {"FirstName", "LastName", "Username", "Password", "email", "Specialization"}

def addProfessor(AM, Password, Username, FirstName, LastName, email, Specialization):
    """
    Inserts a new instructor record into the database.

    Args:
        AM (str): The unique instructor identifier.
        Password (str): Securely stored credential for login.
        Username (str): Unique handle for login.
        FirstName (str): The instructor's given name.
        LastName (str): The instructor's family name.
        email (str): Instructor's primary contact address.
        Specialization (str): The academic field of expertise.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO INSTRUCTOR (AM, Password, Username, FirstName, LastName, email, Specialization) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (AM, Password, Username, FirstName, LastName, email, Specialization)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding instructor: {e}")
        return False
    finally:
        conn.close()

def getProfessor(AM):
    """
    Retrieves an instructor record by their registration number.

    Args:
        AM (str): The unique instructor identifier.

    Returns:
        dict: The instructor record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INSTRUCTOR WHERE AM = ?", (AM,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listProfessors():
    """
    Retrieves all instructor records from the database.

    Returns:
        list: A list of dictionaries representing all instructors.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INSTRUCTOR")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateProfessor(AM, **kwargs):
    """
    Updates an existing instructor record, ignoring invalid keys.

    Args:
        AM (str): The unique instructor identifier.
        **kwargs: Column names and their new values.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    # Filter kwargs against the whitelist.
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

def deleteProfessor(AM):
    """
    Deletes an instructor record from the database.

    Args:
        AM (str): The unique instructor identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
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
