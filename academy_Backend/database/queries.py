# queries.py

# ---------------- Certification Queries ----------------

GET_ALL_CERTIFICATIONS = """
    SELECT Certification_ID, Deadline_Date, Name, Link
    FROM certification_table
    ORDER BY Deadline_Date DESC
"""

GET_CERTIFICATION_BY_ID = """
    SELECT Certification_ID, Deadline_Date, Name, Link 
    FROM certification_table
    WHERE Certification_ID = %s
"""

CREATE_CERTIFICATION = """
    INSERT INTO certification_table (Certification_ID, Name, Deadline_Date, Link)
    VALUES (%s, %s, %s, %s)
"""

UPDATE_CERTIFICATION = """
    UPDATE certification_table 
    SET Name = %s, Deadline_Date = %s, Link = %s
    WHERE Certification_ID = %s
"""

DELETE_CERTIFICATION = """
    DELETE FROM certification_table 
    WHERE Certification_ID = %s
"""

CHECK_CERTIFICATION_EXISTS = """
    SELECT COUNT(*) 
    FROM certification_table 
    WHERE Certification_ID = %s
"""

CHECK_CERTIFICATION_HAS_RECORDS = """
    SELECT COUNT(*) 
    FROM certification_record 
    WHERE Certification_ID = %s
"""

GET_CERTIFICATIONS_WITH_STATS = """
    SELECT 
        c.Certification_ID,
        c.Deadline_Date,
        c.Name,
        c.Link,
        COUNT(cr.Record_ID) AS total_completed,
        COALESCE(AVG(cr.Mark_Secured), 0) AS average_score
    FROM certification_table c
    LEFT JOIN certification_record cr ON c.Certification_ID = cr.Certification_ID
    GROUP BY c.Certification_ID, c.Deadline_Date, c.Name, c.Link
    ORDER BY c.Deadline_Date DESC
"""
