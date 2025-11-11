"""
Database Connection Module
Handles MySQL database connections and query execution
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_connection():
    """
    Create and return a MySQL database connection
    
    Returns:
        MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root'),
            database=os.getenv('DB_NAME', 'qe_academy'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        if connection.is_connected():
            return connection
        
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


def close_db_connection(connection):
    """
    Close the database connection
    
    Args:
        connection: MySQL connection object to close
    """
    try:
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"Error closing database connection: {e}")


def execute_query(query: str, params: Optional[tuple] = None, fetch: bool = True):
    """
    Execute a SQL query with error handling
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (default: True)
        
    Returns:
        Query results if fetch=True, else number of affected rows
    """
    connection = get_db_connection()
    if not connection:
        return None if fetch else 0
    
    try:
        cursor = connection.cursor(dictionary=True) if fetch else connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            return results
        else:
            connection.commit()
            return cursor.rowcount
            
    except Error as e:
        print(f"Error executing query: {e}")
        if not fetch:
            connection.rollback()
        return None if fetch else 0
        
    finally:
        cursor.close()
        close_db_connection(connection)