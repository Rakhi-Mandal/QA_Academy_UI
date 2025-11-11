# ---------------- Certification Queries ----------------


CERTIFICATION_EXISTS = "SELECT 1 FROM certification_table WHERE Certification_ID = %s"

GET_ALL_CERTIFICATIONS = "SELECT Certification_ID, Name, Link FROM certification_table"

GET_CERTIFICATION_BY_ID = "SELECT Certification_ID, Name, Link FROM certification_table WHERE Certification_ID = %s"

# Includes a LEFT JOIN to count records for 'include_stats=True'
GET_CERTIFICATIONS_WITH_STATS = """
    SELECT
        c.Certification_ID,
        c.Name,
        c.Link,
        COUNT(cr.Record_ID) AS Total_Completed
    FROM certification_table c
    LEFT JOIN certification_record cr ON c.Certification_ID = cr.Certification_ID
    GROUP BY c.Certification_ID, c.Name, c.Link
    ORDER BY c.Certification_ID
"""

CREATE_CERTIFICATION = """
    INSERT INTO certification_table (Certification_ID, Name, Link)
    VALUES (%s, %s, %s)
"""

UPDATE_CERTIFICATION_BY_ID = """
    UPDATE certification_table SET Name = %s, Link = %s
    WHERE Certification_ID = %s
"""

DELETE_CERTIFICATION_BY_ID = "DELETE FROM certification_table WHERE Certification_ID = %s"

# Check for existing child records before deletion attempt
CHECK_CERTIFICATION_RECORDS = "SELECT COUNT(*) FROM certification_record WHERE Certification_ID = %s"

# Assuming your record table is named 'certification_record' as previously implied
CHECK_CERTIFICATION_RECORDS = "SELECT COUNT(*) FROM certification_record WHERE Certification_ID = %s"

# ---------- CERTIFICATION RECORD QUERIES ----------

GET_ALL_CERTIFICATION_RECORDS = """
    SELECT 
        Record_ID, Upload_Time, Document, Mark_Secured, 
        Certification_ID, Employee_ID
    FROM certification_record
"""

GET_RECORD_BY_ID = """
    SELECT 
        Record_ID, Upload_Time, Document, Mark_Secured, 
        Certification_ID, Employee_ID
    FROM certification_record
    WHERE Record_ID = %s
"""

GET_RECORDS_BY_EMPLOYEE = """
    SELECT 
        Record_ID, Upload_Time, Document, Mark_Secured, 
        Certification_ID, Employee_ID
    FROM certification_record
    WHERE Employee_ID = %s
    ORDER BY Upload_Time DESC
"""

GET_RECORDS_BY_CERTIFICATION = """
    SELECT 
        Record_ID, Upload_Time, Document, Mark_Secured, 
        Certification_ID, Employee_ID
    FROM certification_record
    WHERE Certification_ID = %s
    ORDER BY Upload_Time DESC
"""

CREATE_CERTIFICATION_RECORD = """
    INSERT INTO certification_record
        (Upload_Time, Document, Mark_Secured, Certification_ID, Employee_ID)
    VALUES (%s, %s, %s, %s, %s)
"""

UPDATE_CERTIFICATION_RECORD = """
    UPDATE certification_record
    SET 
        Document = %s,
        Mark_Secured = %s,
        Certification_ID = %s,
        Employee_ID = %s
    WHERE Record_ID = %s
"""

DELETE_CERTIFICATION_RECORD = """
    DELETE FROM certification_record WHERE Record_ID = %s
"""

RECORD_EXISTS = """
    SELECT 1 FROM certification_record WHERE Record_ID = %s
"""

GET_DOCUMENT_PATH = """
    SELECT Document FROM certification_record WHERE Record_ID = %s
"""
GET_CERTIFICATION_COUNT = "SELECT COUNT(Certification_ID) FROM certification_table"

GET_RECENT_CERTIFICATION_RECORDS = """
    SELECT 
        cr.Record_ID, cr.Upload_Time, cr.Document, cr.Mark_Secured, 
        cr.Certification_ID, cr.Employee_ID,
        c.Name AS Certification_Name  -- Fetch certification name for activity feed
    FROM certification_record cr
    JOIN certification_table c ON cr.Certification_ID = c.Certification_ID
    ORDER BY cr.Upload_Time DESC
    LIMIT 3
# ============================================
# COURSES QUERIES
# ============================================

GET_ALL_COURSES = """
    SELECT 
        Courses_ID,
        Name,
        Link
    FROM courses_table
"""

GET_COURSE_BY_ID = """
    SELECT 
        Courses_ID,
        Name,
        Link
    FROM courses_table
    WHERE Courses_ID = %s
"""

GET_COURSES_WITH_COMPLETION_COUNT = """
    SELECT 
        c.Courses_ID,
        c.Name,
        c.Link,
        COUNT(cr.Record_ID) AS total_completed
    FROM courses_table c
    LEFT JOIN courses_record cr ON c.Courses_ID = cr.Course_ID
    GROUP BY c.Courses_ID, c.Name, c.Link
"""

CHECK_COURSE_EXISTS = """
    SELECT COUNT(*) as count
    FROM courses_table
    WHERE Courses_ID = %s
"""

CHECK_COURSE_HAS_RECORDS = """
    SELECT COUNT(*) as count
    FROM courses_record
    WHERE Course_ID = %s
"""

COURSES_COUNT = """
    SELECT COUNT(*) AS total_courses
    FROM courses_table
"""

# ============================================
# COURSE RECORD QUERIES
# ============================================

GET_ALL_COURSE_RECORDS = """
    SELECT 
        cr.Record_ID,
        cr.Completion_Datetime,
        cr.Document,
        cr.Course_ID,
        c.Name as Course_Name,
        cr.Employee_ID,
        e.Employee_Name
    FROM courses_record cr
    LEFT JOIN courses_table c ON cr.Course_ID = c.Courses_ID
    LEFT JOIN employee_record e ON cr.Employee_ID = e.Employee_ID
    ORDER BY cr.Completion_Datetime DESC
"""

GET_COURSE_RECORD_BY_ID = """
    SELECT 
        cr.Record_ID,
        cr.Completion_Datetime,
        cr.Document,
        cr.Course_ID,
        c.Name as Course_Name,
        c.Link as Course_Link,
        cr.Employee_ID,
        e.Employee_Name,
        e.Employee_Email
    FROM courses_record cr
    LEFT JOIN courses_table c ON cr.Course_ID = c.Courses_ID
    LEFT JOIN employee_record e ON cr.Employee_ID = e.Employee_ID
    WHERE cr.Record_ID = %s
"""

GET_COURSE_RECORDS_BY_EMPLOYEE = """
    SELECT 
        cr.Record_ID,
        cr.Completion_Datetime,
        cr.Document,
        cr.Course_ID,
        c.Name as Course_Name,
        c.Link as Course_Link
    FROM courses_record cr
    LEFT JOIN courses_table c ON cr.Course_ID = c.Courses_ID
    WHERE cr.Employee_ID = %s
    ORDER BY cr.Completion_Datetime DESC
"""

GET_COURSE_RECORDS_BY_COURSE = """
    SELECT 
        cr.Record_ID,
        cr.Completion_Datetime,
        cr.Document,
        cr.Employee_ID,
        e.Employee_Name,
        e.Employee_Email
    FROM courses_record cr
    LEFT JOIN employee_record e ON cr.Employee_ID = e.Employee_ID
    WHERE cr.Course_ID = %s
    ORDER BY cr.Completion_Datetime DESC
"""

CHECK_COURSE_RECORD_EXISTS = """
    SELECT COUNT(*) as count
    FROM courses_record
    WHERE Record_ID = %s
"""

GET_COURSE_RECORD_DOCUMENT = """
    SELECT Document
    FROM courses_record
    WHERE Record_ID = %s
"""

CHECK_EMPLOYEE_COMPLETED_COURSE = """
    SELECT COUNT(*) as count
    FROM courses_record
    WHERE Employee_ID = %s AND Course_ID = %s
"""

# ============================================
# DASHBOARD QUERIES
# ============================================

GET_RECENT_COURSE_COMPLETIONS = """
    SELECT 
        c.Name as Course_Name,
        e.Employee_Name,
        cr.Completion_Datetime
    FROM courses_record cr
    LEFT JOIN courses_table c ON cr.Course_ID = c.Courses_ID
    LEFT JOIN employee_record e ON cr.Employee_ID = e.Employee_ID
    ORDER BY cr.Completion_Datetime DESC
    LIMIT %s
"""

GET_NEXT_COURSE_ID = """
    SELECT CONCAT('C', LPAD(
        COALESCE(MAX(CAST(SUBSTRING(Courses_ID, 2) AS UNSIGNED)), 0) + 1,
        2, '0')
    ) AS next_id
    FROM courses_table
    WHERE Courses_ID REGEXP '^C[0-9]+'
"""