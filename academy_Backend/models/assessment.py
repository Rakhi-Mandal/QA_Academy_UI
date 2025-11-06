from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional, Tuple
import datetime


def get_all_assessments() -> List[Dict]:
    """Get all assessments from database"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in get_all_assessments()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Assessment_ID, Scheduled_Date, Name, Link
            FROM assessment_table
            ORDER BY Scheduled_Date DESC
        """
        print("📄 Executing query:", query)
        cursor.execute(query)
        assessments = cursor.fetchall()

        # ✅ Convert date objects to ISO strings
        for a in assessments:
            if isinstance(a.get("Scheduled_Date"), (datetime.date, datetime.datetime)):
                a["Scheduled_Date"] = a["Scheduled_Date"].isoformat()

        print(f"🔍 Total rows fetched: {len(assessments)}")
        return assessments

    except Exception as e:
        print(f"💥 Error in get_all_assessments: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_assessment_by_id(assessment_id: str) -> Optional[Dict]:
    """Get specific assessment by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Assessment_ID, Scheduled_Date, Name, Link 
            FROM assessment_table 
            WHERE Assessment_ID = %s
        """
        cursor.execute(query, (assessment_id,))
        assessment = cursor.fetchone()

        if assessment and isinstance(assessment.get("Scheduled_Date"), (datetime.date, datetime.datetime)):
            assessment["Scheduled_Date"] = assessment["Scheduled_Date"].isoformat()

        return assessment

    except Exception as e:
        print(f"Error in get_assessment_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_assessments_with_stats() -> List[Dict]:
    """Get all assessments with completion statistics"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                a.Assessment_ID,
                a.Scheduled_Date,
                a.Name,
                a.Link,
                COUNT(ar.Record_ID) AS total_completed,
                COALESCE(AVG(ar.Mark_Secured), 0) AS average_score
            FROM assessment_table a
            LEFT JOIN assessment_record ar ON a.Assessment_ID = ar.Assessment_ID
            GROUP BY a.Assessment_ID, a.Scheduled_Date, a.Name, a.Link
            ORDER BY a.Scheduled_Date DESC
        """
        cursor.execute(query)
        assessments = cursor.fetchall()

        for a in assessments:
            if isinstance(a.get("Scheduled_Date"), (datetime.date, datetime.datetime)):
                a["Scheduled_Date"] = a["Scheduled_Date"].isoformat()

        return assessments
    except Exception as e:
        print(f"Error in get_assessments_with_stats: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_assessment(assessment_id: str, name: str, scheduled_date: Optional[str] = None, link: Optional[str] = None) -> bool:
    """Create new assessment"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO assessment_table (Assessment_ID, Name, Scheduled_Date, Link)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (assessment_id, name, scheduled_date, link))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in create_assessment: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_assessment(assessment_id: str, name: str, scheduled_date: Optional[str] = None, link: Optional[str] = None) -> bool:
    """Update existing assessment"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
            UPDATE assessment_table 
            SET Name = %s, Scheduled_Date = %s, Link = %s
            WHERE Assessment_ID = %s
        """
        cursor.execute(query, (name, scheduled_date, link, assessment_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in update_assessment: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_assessment(assessment_id: str) -> Tuple[bool, str]:
    """Delete assessment"""
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()

        # Check if assessment has records
        check_query = "SELECT COUNT(*) FROM assessment_record WHERE Assessment_ID = %s"
        cursor.execute(check_query, (assessment_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            return False, "Cannot delete assessment with existing records"
        
        # Delete assessment
        delete_query = "DELETE FROM assessment_table WHERE Assessment_ID = %s"
        cursor.execute(delete_query, (assessment_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return True, "Assessment deleted successfully"
        return False, "Assessment not found"
        
    except Exception as e:
        print(f"Error in delete_assessment: {e}")
        connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
        close_db_connection(connection)


def assessment_exists(assessment_id: str) -> bool:
    """Check if assessment exists"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM assessment_table WHERE Assessment_ID = %s"
        cursor.execute(query, (assessment_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in assessment_exists: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def assessment_has_records(assessment_id: str) -> bool:
    """Check if assessment has records"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM assessment_record WHERE Assessment_ID = %s"
        cursor.execute(query, (assessment_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in assessment_has_records: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)
