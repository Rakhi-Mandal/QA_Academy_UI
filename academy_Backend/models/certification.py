from database.connection import get_db_connection, close_db_connection
from database.queries import (
    CERTIFICATION_EXISTS, GET_ALL_CERTIFICATIONS, GET_CERTIFICATION_BY_ID,
    GET_CERTIFICATIONS_WITH_STATS, CREATE_CERTIFICATION, UPDATE_CERTIFICATION_BY_ID,
    DELETE_CERTIFICATION_BY_ID, CHECK_CERTIFICATION_RECORDS,GET_CERTIFICATION_COUNT
)
from typing import List, Dict, Optional, Tuple

def certification_exists(certification_id: str) -> bool:
    """Check if a certification exists by ID."""
    conn = get_db_connection()
    if not conn: return False
    # ... (Implementation uses CERTIFICATION_EXISTS query)
    try:
        cursor = conn.cursor()
        # Uses a dedicated query for fast existence check
        cursor.execute(CERTIFICATION_EXISTS, (certification_id,)) 
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking existence: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(conn)

def get_all_certifications(include_stats: bool) -> List[Dict]:
    """Fetch all certifications, optionally with statistics."""
    conn = get_db_connection()
    if not conn: return [] # <--- Returns empty list if connection fails
    try:
        cursor = conn.cursor(dictionary=True)
        query = GET_CERTIFICATIONS_WITH_STATS if include_stats else GET_ALL_CERTIFICATIONS
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching certifications: {e}") # <--- Check your console for this error!
        return [] # <--- Returns empty list if the query execution fails
    finally:
        cursor.close()
        close_db_connection(conn)


def get_certification_by_id(certification_id: str) -> Optional[Dict]:
    """Fetch a specific certification by ID."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        # Assumes GET_CERTIFICATION_BY_ID is: SELECT * FROM certification_table WHERE Certification_ID = %s
        cursor.execute(GET_CERTIFICATION_BY_ID, (certification_id,)) 
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching certification by ID: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(conn)

def create_certification(certification_id: str, name: str, link: Optional[str]) -> bool:
    """Insert a new certification."""
    conn = get_db_connection()
    if not conn: return False
    # ... (Implementation uses CREATE_CERTIFICATION query)
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_CERTIFICATION, (certification_id, name, link))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error creating certification: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(conn)

def update_certification(certification_id: str, name: str, link: Optional[str]) -> bool:
    """Update certification details."""
    conn = get_db_connection()
    if not conn: return False
    # ... (Implementation uses UPDATE_CERTIFICATION_BY_ID query)
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_CERTIFICATION_BY_ID, (name, link, certification_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating certification: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(conn)

def delete_certification(certification_id: str) -> Tuple[bool, str]:
    """Delete a certification after checking for existing records."""
    conn = get_db_connection()
    if not conn: 
        return False, "Database connection failed."
    # ... (Implementation uses CHECK_CERTIFICATION_RECORDS and DELETE_CERTIFICATION_BY_ID)
    try:
        cursor = conn.cursor()
        cursor.execute(CHECK_CERTIFICATION_RECORDS, (certification_id,))
        record_count = cursor.fetchone()[0]
        
        if record_count > 0:
            return False, f"Cannot delete certification; {record_count} existing records found."
            
        cursor.execute(DELETE_CERTIFICATION_BY_ID, (certification_id,))
        success = cursor.rowcount > 0
        conn.commit()
        
        if not success:
            return False, f"Certification with ID '{certification_id}' not found for deletion."
            
        return True, "Certification deleted successfully."
        
    except Exception as e:
        print(f"Error deleting certification: {e}")
        conn.rollback()
        return False, f"Error deleting certification: {str(e)}"
    finally:
        cursor.close()
        close_db_connection(conn)

def certification_has_records(certification_id: str) -> Tuple[bool, int]:
    """Check if any certification records exist for this certification ID."""
    conn = get_db_connection()
    if not conn: return (False, 0)
    try:
        cursor = conn.cursor()
        # Uses CHECK_CERTIFICATION_RECORDS query: SELECT COUNT(*) FROM certification_record WHERE Certification_ID = %s
        cursor.execute(CHECK_CERTIFICATION_RECORDS, (certification_id,))
        count = cursor.fetchone()[0]
        return (count > 0, count)
    except Exception as e:
        print(f"Error checking records: {e}")
        return (False, 0)
    finally:
        cursor.close()
        close_db_connection(conn)

def get_certification_count() -> int:
    """Fetch the total count of certifications."""
    conn = get_db_connection()
    if not conn: return 0
    try:
        cursor = conn.cursor()
        cursor.execute(GET_CERTIFICATION_COUNT)
        # Fetchone()[0] gets the single integer count from the result tuple
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error fetching certification count: {e}")
        return 0
    finally:
        cursor.close()
        close_db_connection(conn)
