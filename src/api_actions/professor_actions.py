from src.database import getConnection

# Allowed columns for professor updates to prevent SQL errors and protect the primary key.
PROFESSOR_UPDATE_WHITELIST = {"first_name", "last_name", "email", "specialization"}

def addProfessor(registration_number, first_name, last_name, email, specialization):
    """
    Inserts a new professor record into the database.

    Args:
        registration_number (str): The unique professor identifier.
        first_name (str): The professor's given name.
        last_name (str): The professor's family name.
        email (str): Professor's primary contact address.
        specialization (str): The academic field of expertise.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Professors (registration_number, first_name, last_name, email, specialization) VALUES (?, ?, ?, ?, ?)",
            (registration_number, first_name, last_name, email, specialization)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding professor: {e}")
        return False
    finally:
        conn.close()

def getProfessor(registration_number):
    """
    Retrieves a professor record by their registration number.

    Args:
        registration_number (str): The unique professor identifier.

    Returns:
        dict: The professor record as a dictionary, or None if not found.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Professors WHERE registration_number = ?", (registration_number,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def listProfessors():
    """
    Retrieves all professor records from the database.

    Returns:
        list: A list of dictionaries representing all professors.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Professors")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def updateProfessor(registration_number, **kwargs):
    """
    Updates an existing professor record, ignoring invalid keys.

    Args:
        registration_number (str): The unique professor identifier.
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
        values.append(registration_number)
        
        cursor.execute(
            f"UPDATE Professors SET {set_clause} WHERE registration_number = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating professor: {e}")
        return False
    finally:
        conn.close()

def deleteProfessor(registration_number):
    """
    Deletes a professor record from the database.

    Args:
        registration_number (str): The unique professor identifier to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Professors WHERE registration_number = ?", (registration_number,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting professor: {e}")
        return False
    finally:
        conn.close()
