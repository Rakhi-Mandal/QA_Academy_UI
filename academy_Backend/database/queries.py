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
"""