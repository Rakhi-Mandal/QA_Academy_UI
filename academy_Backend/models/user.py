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
            SELECT user_role
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
