"""
Database Connection Management
Handles MySQL database connections
"""
import mysql.connector
from mysql.connector import Error
from config import settings

def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        connection: MySQL connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def close_db_connection(connection):
    """
    Close database connection safely
    
    Args:
        connection: MySQL connection object
    """
    if connection and connection.is_connected():
        connection.close()

def execute_query(query: str, params: tuple = None, fetch: str = "all"):
    """
    Execute a database query with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: 'all', 'one', or 'none' for SELECT queries
        
    Returns:
        Query results or None
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch == "all":
            result = cursor.fetchall()
        elif fetch == "one":
            result = cursor.fetchone()
        else:
            connection.commit()
            result = cursor.lastrowid
            
        cursor.close()
        return result
        
    except Error as e:
        print(f"Error executing query: {e}")
        return None
        
    finally:
        close_db_connection(connection)