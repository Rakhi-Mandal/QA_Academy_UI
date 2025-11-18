from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import os # For deleting the file path
from database.queries import (
    RECORD_EXISTS, GET_ALL_CERTIFICATION_RECORDS, GET_RECORD_BY_ID,
    GET_RECORDS_BY_EMPLOYEE, GET_RECORDS_BY_CERTIFICATION,
    CREATE_CERTIFICATION_RECORD, UPDATE_CERTIFICATION_RECORD,
    DELETE_CERTIFICATION_RECORD, GET_DOCUMENT_PATH,
    GET_RECENT_CERTIFICATION_RECORDS # Used for recent activity
)
 
def record_exists(record_id: int) -> bool:
    """Check if a certification record exists by Record_ID."""
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(RECORD_EXISTS, (record_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"💥 Error in record_exists: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
def get_all_certification_records() -> List[Dict]:
    """Fetch all certification records and serialize data types."""
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(GET_ALL_CERTIFICATION_RECORDS)
        records = cursor.fetchall()
       
        # --- FIX: Serialization for datetime and Decimal ---
        serialized_records = []
        for record in records:
            record_copy = record.copy()
           
            # 1. Handle DATETIME (Upload_Time)
            upload_time = record_copy.get('Upload_Time')
            if isinstance(upload_time, datetime):
                record_copy['Upload_Time'] = upload_time.isoformat()
           
            # 2. Handle DECIMAL (Mark_Secured)
            mark_secured = record_copy.get('Mark_Secured')
            if isinstance(mark_secured, Decimal):
                record_copy['Mark_Secured'] = float(mark_secured)
           
            serialized_records.append(record_copy)
       
        return serialized_records
        # ---------------------------------------------------
       
    except Exception as e:
        print(f"Error fetching all certification records: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
 
def get_record_by_id(record_id: int) -> Optional[Dict]:
    """Fetch a specific certification record by Record_ID and serialize data types."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn: return None
       
        cursor = conn.cursor(dictionary=True)
        # Assuming GET_RECORD_BY_ID is correctly defined in database/queries.py
        cursor.execute(GET_RECORD_BY_ID, (record_id,))
        record = cursor.fetchone()
       
        # --- NEW DEBUGGING PRINT ---
        if record:
            print(f"DEBUG: Record fetched successfully for ID {record_id}. Keys: {list(record.keys())}")
        else:
            print(f"DEBUG: No record found in DB for ID {record_id}")
        # ---------------------------
 
        if not record:
            return None
       
        # --- CRITICAL: Serialization Fix (Ensure keys match DB exactly) ---
        record_copy = record.copy()
       
        # 1. Handle DATETIME (Upload_Time)
        upload_time = record_copy.get('Upload_Time') # Must match DB column name exactly
        if isinstance(upload_time, datetime):
            record_copy['Upload_Time'] = upload_time.isoformat()
       
        # 2. Handle DECIMAL (Mark_Secured)
        mark_secured = record_copy.get('Mark_Secured') # Must match DB column name exactly
        if isinstance(mark_secured, Decimal):
            record_copy['Mark_Secured'] = float(mark_secured)
           
        return record_copy # Return the correctly serialized dictionary
 
    except Exception as e:
        print(f"💥 Error in get_record_by_id: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
   
def get_records_by_employee(employee_id: str) -> List[Dict]:
    conn = None
    cursor = None
    records = [] # Initialize for safe serialization/return
 
    try:
        conn = get_db_connection()
        if not conn: return records
       
        cursor = conn.cursor(dictionary=True)
        cursor.execute(GET_RECORDS_BY_EMPLOYEE, (employee_id,))
        records = cursor.fetchall()
       
        # --- CRITICAL: Serialization Logic Must Be Present Here ---
        serialized_records = []
        for record in records:
            record_copy = record.copy()
           
            # 1. Handle DATETIME (Upload_Time)
            if isinstance(record_copy.get('Upload_Time'), datetime):
                record_copy['Upload_Time'] = record_copy['Upload_Time'].isoformat()
           
            # 2. Handle DECIMAL (Mark_Secured)
            if isinstance(record_copy.get('Mark_Secured'), Decimal):
                record_copy['Mark_Secured'] = float(record_copy['Mark_Secured'])
           
            serialized_records.append(record_copy)
 
        return serialized_records
       
    except Exception as e:
        print(f"💥 Error in get_records_by_employee: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close() # CRITICAL FIX
 
def get_records_by_certification(certification_id: str) -> List[Dict]:
    """Fetch all records for a specific Certification_ID."""
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(GET_RECORDS_BY_CERTIFICATION, (certification_id,))
        # NOTE: Serialization logic needs to be added here too if this method is used by a router
        return cursor.fetchall()
    except Exception as e:
        print(f"💥 Error in get_records_by_certification: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close() # CRITICAL FIX
 
def create_record(data: dict) -> Optional[Dict]:
    """Insert a new certification record and return the created data."""
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    try:
        cursor = conn.cursor()
        # Data preparation (Upload_Time handled by Python/DB default)
        now = datetime.now()
        params = (
            now,
            data.get('document'),
            data['mark_secured'],
            data['certification_id'],
            data['employee_id']
        )
       
        cursor.execute(CREATE_CERTIFICATION_RECORD, params)
        conn.commit()
        last_id = cursor.lastrowid
       
        return get_record_by_id(last_id)
    except Exception as e:
        print(f"💥 Error in create_record: {e}")
        if conn: conn.rollback()
        return None
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
def update_record(record_id: int, data: dict) -> bool:
    """Update certification record details."""
    conn = get_db_connection()
    if not conn: return False
    cursor = None
   
    # Prepare dynamic update query parameters
    updates = []
    params = []
   
    if 'document' in data and data['document'] is not None:
        updates.append("Document = %s")
        params.append(data['document'])
    if 'mark_secured' in data and data['mark_secured'] is not None:
        updates.append("Mark_Secured = %s")
        params.append(data['mark_secured'])
    if 'certification_id' in data and data['certification_id'] is not None:
        updates.append("Certification_ID = %s")
        params.append(data['certification_id'])
    if 'employee_id' in data and data['employee_id'] is not None:
        updates.append("Employee_ID = %s")
        params.append(data['employee_id'])
             
    if not updates:
        return True # Nothing to update
 
    params.append(record_id)
   
    try:
        cursor = conn.cursor()
        # NOTE: Using string formatting for SET clause is generally okay for UPDATEs
        # where the column list is dynamic, but ensure inputs are sanitized.
        query = f"UPDATE certification_record SET {', '.join(updates)} WHERE Record_ID = %s"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"💥 Error in update_record: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
def get_document_path(record_id: int) -> Optional[str]:
    """Get the document path for a specific record."""
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(GET_DOCUMENT_PATH, (record_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"💥 Error in get_document_path: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
def delete_record(record_id: int) -> Tuple[bool, str]:
    """Delete a certification record by ID and related document file."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    cursor = None
   
    # 1. Get path before deletion
    document_path = get_document_path(record_id)
   
    try:
        cursor = conn.cursor()
        cursor.execute(DELETE_CERTIFICATION_RECORD, (record_id,))
       
        if cursor.rowcount == 0:
            return False, f"Record with ID '{record_id}' not found."
           
        conn.commit()
       
        # 2. Attempt to delete the file after successful DB deletion
        if document_path and os.path.exists(document_path):
            os.remove(document_path)
            print(f"🗑️ Deleted file: {document_path}")
 
        return True, "Certification record deleted successfully."
    except Exception as e:
        print(f"💥 Error in delete_record: {e}")
        if conn: conn.rollback()
        return False, f"Error deleting record: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn: close_db_connection(conn)
 
 
def get_last_n_certification_records(limit: int = 2) -> List[Dict]:
    """Fetch the N most recent certification records with joins and serialize types."""
   
    # --- CRITICAL FIX: Initialize variables outside the try block ---
    conn = None
    cursor = None
   
    try:
        conn = get_db_connection() # conn is assigned here
        if not conn:
            # If connection fails, conn is None, and we immediately return
            return []
       
        cursor = conn.cursor(dictionary=True) # cursor is assigned here
        cursor.execute(GET_RECENT_CERTIFICATION_RECORDS)
        records = cursor.fetchall()
       
        # ... (Serialization logic for datetime and Decimal here) ...
        # (This remains the same)
       
        serialized_records = []
        for record in records:
            record_copy = record.copy()
           
            # 1. Handle DATETIME (Upload_Time)
            # ... (datetime conversion logic) ...
            if isinstance(record_copy.get('Upload_Time'), datetime):
                record_copy['Upload_Time'] = record_copy['Upload_Time'].isoformat()
           
            # 2. Handle DECIMAL (Mark_Secured)
            # ... (Decimal conversion logic) ...
            if isinstance(record_copy.get('Mark_Secured'), Decimal):
                record_copy['Mark_Secured'] = float(record_copy['Mark_Secured'])
           
            serialized_records.append(record_copy)
 
        return serialized_records
 
    except Exception as e:
        print(f"Error fetching recent certification records: {e}")
        return []
       
    finally:
        # Check if they were successfully assigned (i.e., not None) before closing
        if cursor:
            cursor.close()
        if conn:
            close_db_connection(conn)
 