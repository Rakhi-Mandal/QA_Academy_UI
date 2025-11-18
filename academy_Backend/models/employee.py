from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional
from database import queries

def get_all_employees() -> List[Dict]:
    """Get all employee records"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code
            FROM employee_record
            ORDER BY Employee_Name
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        return employees
    except Exception as e:
        print(f"Error in get_all_employees: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employee_by_id(employee_id: str) -> Optional[Dict]:
    """Get specific employee record"""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code
            FROM employee_record
            WHERE Employee_ID = %s
        """
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()
        return employee
    except Exception as e:
        print(f"Error in get_employee_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employees_by_batch(batch_code: int) -> List[Dict]:
    """Get employees by Batch_Code (join pod and employee_record)"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
WITH total_counts AS (
    SELECT 
        COUNT(*) AS total_assessments
        FROM assessment_table
    ),
    cert_counts AS (
        SELECT 
        COUNT(*) AS total_certifications
        FROM certification_table
    ),
    course_counts AS (
        SELECT 
        COUNT(*) AS total_courses
        FROM courses_table
    ),
employee_counts AS (
    SELECT 
        e.Employee_ID,
        e.Employee_Name,
        e.Employee_Email,
        e.Designation,
        p.POD,
        p.Batch_Code,
        COUNT(DISTINCT ar.Assessment_ID) AS assessment_count,
        COUNT(DISTINCT cr.Certification_ID) AS certification_count,
        COUNT(DISTINCT cor.Course_ID) AS course_count
    FROM employee_record e
    INNER JOIN pod p ON e.POD_ID = p.POD_ID
    LEFT JOIN assessment_record ar ON e.Employee_ID = ar.Employee_ID
    LEFT JOIN certification_record cr ON e.Employee_ID = cr.Employee_ID
    LEFT JOIN courses_record cor ON e.Employee_ID = cor.Employee_ID
    WHERE p.Batch_Code = %s
    GROUP BY e.Employee_ID, e.Employee_Name, e.Employee_Email, e.Designation, p.POD, p.Batch_Code
)
SELECT 
    ec.Employee_ID,
    ec.Employee_Name,
    ec.Employee_Email,
    ec.Designation,
    ec.POD,
    ec.Batch_Code,
    ROUND((ec.assessment_count / NULLIF(t.total_assessments, 0)) * 100, 2) AS assessment_completion_percent,
    ROUND((ec.certification_count / NULLIF(c.total_certifications, 0)) * 100, 2) AS certification_completion_percent,
    ROUND((ec.course_count / NULLIF(crs.total_courses, 0)) * 100, 2) AS course_completion_percent
FROM employee_counts ec
CROSS JOIN total_counts t
CROSS JOIN cert_counts c
CROSS JOIN course_counts crs
ORDER BY ec.Employee_ID;

        """
        cursor.execute(query, (batch_code,))
        employees = cursor.fetchall()
        return employees
    except Exception as e:
        print(f"Error in get_employees_by_batch: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_employee(employee_id: str, employee_name: str, employee_email: str, designation: str, pod_id: int, user_id: int) -> bool:
    """Create new employee record"""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO employee_record (Employee_ID, Employee_Name, Employee_Email, Designation, POD_ID, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (employee_id, employee_name, employee_email, designation, pod_id, user_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in create_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)



def update_employee(employee_id, employee_name, employee_email, designation, batch_code):
    """Update an existing employee record"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in update_employee")
        return False

    try:
        cursor = connection.cursor()
        query = """
            UPDATE employee_record
            SET Employee_Name = %s,
                Employee_Email = %s,
                Designation = %s,
                Batch_Code = %s
            WHERE Employee_ID = %s
        """
        print("🧠 Query:", query)
        print("🧠 Values:", (employee_name, employee_email, designation, batch_code, employee_id))

        cursor.execute(query, (employee_name, employee_email, designation, batch_code, employee_id))
        connection.commit()

        print("✅ Rows affected:", cursor.rowcount)
        return cursor.rowcount > 0
    except Exception as e:
        print("❌ Error in update_employee:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_employee(employee_id: str) -> bool:
    """Delete employee record"""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = "DELETE FROM employee_record WHERE Employee_ID = %s"
        cursor.execute(query, (employee_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in delete_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


# ✅ FIXED CERTIFICATION QUERY
def get_employee_certifications(employee_id: str) -> List[Dict]:
    """Get all certifications for an employee"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                cr.Record_ID,
                cr.Employee_ID,
                cr.Certification_ID,
                ct.Name AS Certification_Name,
                cr.Mark_Secured
            FROM certification_record cr
            JOIN certification_table ct ON cr.Certification_ID = ct.Certification_ID
            WHERE cr.Employee_ID = %s
        """
        print("🧠 Running get_employee_certifications for", employee_id)
        cursor.execute(query, (employee_id,))
        certifications = cursor.fetchall()
        print("✅ certifications result:", certifications)
        return certifications
    except Exception as e:
        print(f"Error in get_employee_certifications: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


# ✅ FIXED ASSESSMENT QUERY
def get_employee_assessments(employee_id: str) -> List[Dict]:
    """Get all assessments for an employee"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                ar.Record_ID,
                ar.Employee_ID,
                ar.Assessment_ID,
                at.Name AS Assessment_Name,
                ar.Mark_Secured
            FROM assessment_record ar
            JOIN assessment_table at ON ar.Assessment_ID = at.Assessment_ID
            WHERE ar.Employee_ID = %s
        """
        print("🧠 Running get_employee_assessments for", employee_id)
        cursor.execute(query, (employee_id,))
        assessments = cursor.fetchall()
        print("✅ assessments result:", assessments)
        return assessments
    except Exception as e:
        print(f"Error in get_employee_assessments: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employee_courses(employee_id: str) -> List[Dict]:
    """Get all courses for an employee"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                cor.Record_ID,
                cor.Employee_ID,
                cor.Course_ID,
                ct.Name AS Course_Name
            FROM courses_record cor
            JOIN courses_table ct ON cor.Course_ID = ct.Courses_ID
            WHERE cor.Employee_ID = %s
        """
        print(f"🧠 Running get_employee_courses for Employee_ID: {employee_id}")
        cursor.execute(query, (employee_id,))
        courses = cursor.fetchall()
        print("✅ courses result:", courses)
        return courses
    except Exception as e:
        print(f"❌ Error in get_employee_courses: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)



def get_employee_all_records(employee_id: str) -> Dict:
    """Get all records (certifications, assessments, courses) for an employee"""
    return {
        "certifications": get_employee_certifications(employee_id),
        "assessments": get_employee_assessments(employee_id),
        "courses": get_employee_courses(employee_id)
    }

        
def get_employee_by_user_id(user_id: int):
    """Fetch employee details from employee_record table using user_id"""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT * FROM employee_record
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        return result
    except Exception as e:
        print(f"Error in get_employee_by_user_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)
def get_employee_count() -> int:
    """Get total count of employees"""
    connection = get_db_connection()
    if not connection:
        return 0
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) AS total_employees FROM employee_record"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error in get_employee_count: {e}")
        return 0
    finally:
        cursor.close()
        close_db_connection(connection)


def get_top_performers() -> List[Dict]:
    """Get top performers based on assessment + certification percentage"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_TOP_PERFORMERS)
        performers = cursor.fetchall()
        return performers
    except Exception as e:
        print(f"Error in get_top_performers: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)