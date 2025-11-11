"""
Courses Model - Database operations
Uses centralized queries from queries.py
"""
from database.connection import get_db_connection, close_db_connection
from database import queries
from typing import List, Dict, Optional
import datetime


def get_all_courses() -> List[Dict]:
    """Get all courses from database"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in get_all_courses()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        print("📄 Executing query: GET_ALL_COURSES")
        cursor.execute(queries.GET_ALL_COURSES)
        courses = cursor.fetchall()

        # ✅ Convert date objects to ISO strings
        # for c in courses:
        #     if isinstance(c.get("Deadline_Date"), (datetime.date, datetime.datetime)):
        #         c["Deadline_Date"] = c["Deadline_Date"].isoformat()

        print(f"📊 Total rows fetched: {len(courses)}")
        return courses

    except Exception as e:
        print(f"💥 Error in get_all_courses: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_course_by_id(course_id: str) -> Optional[Dict]:
    """Get specific course by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_COURSE_BY_ID, (course_id,))
        course = cursor.fetchone()

        # if course and isinstance(course.get("Deadline_Date"), (datetime.date, datetime.datetime)):
        #     course["Deadline_Date"] = course["Deadline_Date"].isoformat()

        return course

    except Exception as e:
        print(f"Error in get_course_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_courses_with_stats() -> List[Dict]:
    """Get all courses with completion statistics"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_COURSES_WITH_COMPLETION_COUNT)
        courses = cursor.fetchall()

        # for c in courses:
        #     if isinstance(c.get("Deadline_Date"), (datetime.date, datetime.datetime)):
        #         c["Deadline_Date"] = c["Deadline_Date"].isoformat()

        return courses
    except Exception as e:
        print(f"Error in get_courses_with_stats: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_course(courses_id: str, name: str, link: Optional[str] = None) -> bool:
    """Create new course"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO courses_table (Courses_ID, Name, Link)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (courses_id, name, link))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in create_course: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_course(courses_id: str, name: str,  link: Optional[str] = None) -> bool:
    """Update existing course"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
            UPDATE courses_table 
            SET Name = %s, Link = %s
            WHERE Courses_ID = %s
        """
        cursor.execute(query, (name, link, courses_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in update_course: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_course(courses_id: str) -> tuple:
    """Delete course"""
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()

        # Check if course has records
        cursor.execute(queries.CHECK_COURSE_HAS_RECORDS, (courses_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            return False, "Cannot delete course with existing records"
        
        # Delete course
        delete_query = "DELETE FROM courses_table WHERE Courses_ID = %s"
        cursor.execute(delete_query, (courses_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return True, "Course deleted successfully"
        return False, "Course not found"
        
    except Exception as e:
        print(f"Error in delete_course: {e}")
        connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
        close_db_connection(connection)


def course_exists(courses_id: str) -> bool:
    """Check if course exists"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(queries.CHECK_COURSE_EXISTS, (courses_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in course_exists: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def course_has_records(courses_id: str) -> bool:
    """Check if course has records"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(queries.CHECK_COURSE_HAS_RECORDS, (courses_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in course_has_records: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)

def get_course_count() -> List[Dict]:
    """Get all courses from database"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in get_course_count()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        print("📄 Executing query: COURSES_COUNT")
        cursor.execute(queries.COURSES_COUNT)
        courses = cursor.fetchall()


        print(f"📊 Total rows : {len(courses)}")
        return courses

    except Exception as e:
        print(f"💥 Error in get_course_count: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)