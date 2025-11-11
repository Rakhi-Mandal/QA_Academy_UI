from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional, Tuple
import datetime


def get_all_batches() -> List[Dict]:
    """Get all batches from database"""
    connection = get_db_connection()
    if not connection:
        print("Database connection failed in get_all_batches()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Batch_Code, Batch_Name
            FROM batch_table
        """
        print("📄 Executing query:", query)
        cursor.execute(query)
        batches = cursor.fetchall()

        print(f"🔍 Total rows fetched: {len(batches)}")
        return batches

    except Exception as e:
        print(f"💥 Error in get_all_batches: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)

def get_batch_count() -> int:
    """Get total count of batches"""
    connection = get_db_connection()
    if not connection:
        print("Database connection failed in get_batch_count()")
        return 0
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM batch_table"
        print("📄 Executing query:", query)
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0] if result else 0
        
        print(f"🔍 Total batches: {count}")
        return count

    except Exception as e:
        print(f"💥 Error in get_batch_count: {e}")
        return 0
    finally:
        cursor.close()
        close_db_connection(connection)