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