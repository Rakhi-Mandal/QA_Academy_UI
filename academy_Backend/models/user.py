from database.connection import get_db_connection, close_db_connection
from typing import Dict, Optional
import datetime
import decimal


def create_user(user_mail: str, user_password: str, user_role: str = "employee") -> bool:
    """Create a new user"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO users (user_mail, user_password, user_role)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_mail, user_password, user_role))
        connection.commit()
        return True

    except Exception as e:
        print(f"Error in create_user: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        close_db_connection(connection)


def get_user_by_email(user_mail: str) -> Optional[Dict]:
    """Fetch user details by email"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, user_mail, user_password, user_role
            FROM users
            WHERE user_mail = %s
        """
        cursor.execute(query, (user_mail,))
        user = cursor.fetchone()

        return user

    except Exception as e:
        print(f"Error in get_user_by_email: {e}")
        return None

    finally:
        cursor.close()
        close_db_connection(connection)

def validate_login(user_mail: str, user_password: str):
    """Validate user login and return role if credentials are valid"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, user_role
            FROM users
            WHERE user_mail = %s AND user_password = %s
        """
        cursor.execute(query, (user_mail, user_password))
        user = cursor.fetchone()
        return user

    except Exception as e:
        print(f"Error validating login: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_all_users():
    """Get all users"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, user_mail, user_role
            FROM users
            ORDER BY user_id
        """
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        return []
    
    finally:
        cursor.close()
        close_db_connection(connection)


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, user_mail, user_role
            FROM users
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user
    
    except Exception as e:
        print(f"Error in get_user_by_id: {e}")
        return None
    
    finally:
        cursor.close()
        close_db_connection(connection)


def update_user(user_id: int, user_password: str, user_role: str) -> bool:
    """Update user password and/or role"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
            UPDATE users
            SET user_password = %s, user_role = %s
            WHERE user_id = %s
        """
        cursor.execute(query, (user_password, user_role, user_id))
        connection.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error in update_user: {e}")
        connection.rollback()
        return False
    
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_user(user_id: int) -> bool:
    """Delete a user"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error in delete_user: {e}")
        connection.rollback()
        return False
    
    finally:
        cursor.close()
        close_db_connection(connection)
