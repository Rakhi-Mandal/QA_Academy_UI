# academy_Backend/routes/dashboard.py - FINAL COMPLETE VERSION
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
 
from database.connection import get_db_connection, close_db_connection
 
# Optional: If you have custom models, keep these imports
try:
    from models.employee import get_employee_dashboard, get_employee_deadline_items, get_employee_calendar
except Exception:
    get_employee_dashboard = None
    get_employee_deadline_items = None
    get_employee_calendar = None
 
router = APIRouter(tags=["dashboard"])
 
# Setup upload directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
 
 
# ==========================================
# 1. DASHBOARD STATS
# ==========================================
@router.get("/dashboard")
def dashboard(employee_id: str):
    """
    Get KPI tiles for the logged-in employee.
    Returns: total assignments, certifications, courses, completed count, remaining count
    """
    if not employee_id:
        raise HTTPException(status_code=400, detail="employee_id is required")
 
    # Try custom model function first
    if get_employee_dashboard:
        try:
            data = get_employee_dashboard(employee_id)
            return JSONResponse(content={"success": True, "data": data})
        except Exception:
            pass
 
    # Fallback to direct DB query
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(dictionary=True)
   
    try:
        # Get POD_ID for the employee
        cur.execute(
            "SELECT p.POD_ID FROM employee_record e LEFT JOIN pod p ON e.POD_ID = p.POD_ID WHERE e.Employee_ID = %s",
            (employee_id,),
        )
        row = cur.fetchone()
        pod_id = row.get("POD_ID") if row else None
 
        if not pod_id:
            return JSONResponse(
                content={
                    "success": True,
                    "data": {
                        "total_assignments": 0,
                        "total_certifications": 0,
                        "total_courses": 0,
                        "completed_total": 0,
                        "remaining_total": 0,
                    },
                }
            )
 
        # Count total items
        cur.execute("SELECT COUNT(*) AS cnt FROM assessment_table")
        total_assignments = int(cur.fetchone().get("cnt", 0))
 
        cur.execute("SELECT COUNT(*) AS cnt FROM certification_table")
        total_certifications = int(cur.fetchone().get("cnt", 0))
 
        cur.execute("SELECT COUNT(*) AS cnt FROM courses_table")
        total_courses = int(cur.fetchone().get("cnt", 0))
 
        # Count completed items for this employee
        cur.execute(
            """
            SELECT
              (SELECT COUNT(*) FROM assessment_record WHERE Employee_ID=%s) AS a_cnt,
              (SELECT COUNT(*) FROM certification_record WHERE Employee_ID=%s) AS c_cnt,
              (SELECT COUNT(*) FROM courses_record WHERE Employee_ID=%s) AS co_cnt
            """,
            (employee_id, employee_id, employee_id),
        )
        comp = cur.fetchone()
        completed_total = int(comp.get("a_cnt", 0)) + int(comp.get("c_cnt", 0)) + int(comp.get("co_cnt", 0))
 
        assigned_total = total_assignments + total_certifications + total_courses
        remaining_total = max(0, assigned_total - completed_total)
 
        data = {
            "total_assignments": total_assignments,
            "total_certifications": total_certifications,
            "total_courses": total_courses,
            "completed_total": completed_total,
            "remaining_total": remaining_total,
        }
        return JSONResponse(content={"success": True, "data": data})
   
    finally:
        cur.close()
        close_db_connection(conn)
 
 
# ==========================================
# 2. GET FILTERED ITEMS (WITH BACKEND FILTER)
# ==========================================
@router.get("/items")
def items(employee_id: str, filter: Optional[str] = "all"):
    """
    Return tasks for the employee's POD with BACKEND FILTERING.
    filter: 'all' | 'assessments' | 'certifications' | 'courses'
    """
    if not employee_id:
        raise HTTPException(status_code=400, detail="employee_id required")
 
    filter_clean = (filter or "all").strip().lower()
   
    # ✅ Map frontend filter names to backend Task_Type values
    filter_map = {
        "all": None,
        "assessments": "Assessment",
        "certifications": "Certification",
        "courses": "Course"
    }
   
    task_type_filter = filter_map.get(filter_clean)
    print(f"🔍 Filter: '{filter_clean}' -> Task_Type: '{task_type_filter}'")
 
    # Try custom model function first
    if get_employee_deadline_items:
        try:
            rows = get_employee_deadline_items(employee_id, filter_clean)
            for r in rows:
                if "effective_deadline" in r and hasattr(r["effective_deadline"], "isoformat"):
                    r["effective_deadline"] = r["effective_deadline"].isoformat()
            return {"success": True, "total": len(rows), "data": rows}
        except Exception:
            pass
 
    # Fallback to direct DB query
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(dictionary=True)
   
    try:
        # Get POD_ID and Batch_Code
        cur.execute(
            "SELECT p.POD_ID, p.Batch_Code FROM employee_record e JOIN pod p ON e.POD_ID = p.POD_ID WHERE e.Employee_ID = %s",
            (employee_id,),
        )
        pod_row = cur.fetchone()
       
        if not pod_row or not pod_row.get("POD_ID"):
            print(f"⚠️ No POD found for employee {employee_id}")
            return {"success": True, "total": 0, "data": []}
       
        pod_id = pod_row.get("POD_ID")
        batch_code = pod_row.get("Batch_Code")
        print(f"📦 POD_ID: {pod_id}, Batch: {batch_code}")
 
        # Check if pod_deadline table exists
        try:
            db_name = getattr(conn, "database", None)
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM information_schema.tables WHERE table_schema = %s AND table_name = 'pod_deadline'",
                (db_name,)
            )
            has_pod_deadline = bool(cur.fetchone().get('cnt'))
        except Exception:
            has_pod_deadline = False
 
        # Build query with Task_Type filter in WHERE clause
        if has_pod_deadline:
            sql = """
            SELECT DISTINCT
                t.Task_Slno,
                t.Task_ID,
                t.Task_Type,
                COALESCE(a.Name, c.Name, co.Name) AS title,
                COALESCE(a.Link, c.Link, co.Link) AS link,
                CASE
                  WHEN t.Task_Type = 'Assessment' AND ar.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type = 'Certification' AND cr.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type = 'Course' AND cor.Record_ID IS NOT NULL THEN 'completed'
                  ELSE 'assigned'
                END AS status,
                CASE
                  WHEN t.Task_Type = 'Assessment' AND ar.Record_ID IS NOT NULL THEN 1
                  WHEN t.Task_Type = 'Certification' AND cr.Record_ID IS NOT NULL THEN 1
                  WHEN t.Task_Type = 'Course' AND cor.Record_ID IS NOT NULL THEN 1
                  ELSE 0
                END AS is_completed,
                COALESCE(pd.Deadline_Date, t.Deadline_Date) AS effective_deadline,
                ar.Upload_Time AS assessment_upload_time,
                ar.Mark_Secured AS assessment_marks,
                cr.Upload_Time AS certification_upload_time,
                cr.Mark_Secured AS certification_marks,
                cor.Completion_Datetime AS course_completion_time
            FROM deadline_table t
            LEFT JOIN pod_deadline pd ON pd.Task_Slno = t.Task_Slno AND pd.POD_ID = %s
            LEFT JOIN assessment_table a ON (t.Task_Type='Assessment' AND t.Task_ID = a.Assessment_ID)
            LEFT JOIN certification_table c ON (t.Task_Type='Certification' AND t.Task_ID = c.Certification_ID)
            LEFT JOIN courses_table co ON (t.Task_Type='Course' AND t.Task_ID = co.Courses_ID)
            LEFT JOIN assessment_record ar ON (t.Task_Type='Assessment' AND t.Task_ID = ar.Assessment_ID AND ar.Employee_ID = %s)
            LEFT JOIN certification_record cr ON (t.Task_Type='Certification' AND t.Task_ID = cr.Certification_ID AND cr.Employee_ID = %s)
            LEFT JOIN courses_record cor ON (t.Task_Type='Course' AND t.Task_ID = cor.Course_ID AND cor.Employee_ID = %s)
            WHERE t.Batch_Code = %s
            """
            params = [pod_id, employee_id, employee_id, employee_id, batch_code]
        else:
            sql = """
            SELECT DISTINCT
                t.Task_Slno,
                t.Task_ID,
                t.Task_Type,
                COALESCE(a.Name, c.Name, co.Name) AS title,
                COALESCE(a.Link, c.Link, co.Link) AS link,
                CASE
                  WHEN t.Task_Type = 'Assessment' AND ar.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type = 'Certification' AND cr.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type = 'Course' AND cor.Record_ID IS NOT NULL THEN 'completed'
                  ELSE 'assigned'
                END AS status,
                CASE
                  WHEN t.Task_Type = 'Assessment' AND ar.Record_ID IS NOT NULL THEN 1
                  WHEN t.Task_Type = 'Certification' AND cr.Record_ID IS NOT NULL THEN 1
                  WHEN t.Task_Type = 'Course' AND cor.Record_ID IS NOT NULL THEN 1
                  ELSE 0
                END AS is_completed,
                t.Deadline_Date AS effective_deadline,
                ar.Upload_Time AS assessment_upload_time,
                ar.Mark_Secured AS assessment_marks,
                cr.Upload_Time AS certification_upload_time,
                cr.Mark_Secured AS certification_marks,
                cor.Completion_Datetime AS course_completion_time
            FROM deadline_table t
            LEFT JOIN assessment_table a ON (t.Task_Type='Assessment' AND t.Task_ID = a.Assessment_ID)
            LEFT JOIN certification_table c ON (t.Task_Type='Certification' AND t.Task_ID = c.Certification_ID)
            LEFT JOIN courses_table co ON (t.Task_Type='Course' AND t.Task_ID = co.Courses_ID)
            LEFT JOIN assessment_record ar ON (t.Task_Type='Assessment' AND t.Task_ID = ar.Assessment_ID AND ar.Employee_ID = %s)
            LEFT JOIN certification_record cr ON (t.Task_Type='Certification' AND t.Task_ID = cr.Certification_ID AND cr.Employee_ID = %s)
            LEFT JOIN courses_record cor ON (t.Task_Type='Course' AND t.Task_ID = cor.Course_ID AND cor.Employee_ID = %s)
            WHERE t.Batch_Code = %s
            """
            params = [employee_id, employee_id, employee_id, batch_code]
 
        # ✅ Add Task_Type filter if specified
        if task_type_filter:
            sql += " AND t.Task_Type = %s"
            params.append(task_type_filter)
 
        # Add sorting
        sql += " ORDER BY is_completed DESC, effective_deadline ASC"
 
        print(f"🔍 Executing with params: {params}")
        cur.execute(sql, tuple(params))
        rows = cur.fetchall() or []
        print(f"📊 Returned {len(rows)} rows")
 
        # Process rows
        for r in rows:
            # Normalize deadline date
            if "effective_deadline" in r and hasattr(r["effective_deadline"], "isoformat"):
                r["effective_deadline"] = r["effective_deadline"].isoformat()
           
            # Add completion time and marks
            if r.get("is_completed"):
                if r.get("Task_Type") == "Assessment" and r.get("assessment_upload_time"):
                    r["Upload_Time"] = r["assessment_upload_time"].isoformat() if hasattr(r["assessment_upload_time"], "isoformat") else r["assessment_upload_time"]
                    r["Mark_Secured"] = r.get("assessment_marks")
                elif r.get("Task_Type") == "Certification" and r.get("certification_upload_time"):
                    r["Upload_Time"] = r["certification_upload_time"].isoformat() if hasattr(r["certification_upload_time"], "isoformat") else r["certification_upload_time"]
                    r["Mark_Secured"] = r.get("certification_marks")
                elif r.get("Task_Type") == "Course" and r.get("course_completion_time"):
                    r["Completion_Datetime"] = r["course_completion_time"].isoformat() if hasattr(r["course_completion_time"], "isoformat") else r["course_completion_time"]
           
            # Clean up temp fields
            r.pop("assessment_upload_time", None)
            r.pop("assessment_marks", None)
            r.pop("certification_upload_time", None)
            r.pop("certification_marks", None)
            r.pop("course_completion_time", None)
           
            r["is_completed"] = int(r.get("is_completed") or 0)
            r["completed"] = bool(r["is_completed"])
 
        print(f"✅ Returning {len(rows)} filtered rows")
        return {"success": True, "total": len(rows), "data": rows}
   
    finally:
        cur.close()
        close_db_connection(conn)
 
 
# ==========================================
# 3. GET CALENDAR ITEMS
# ==========================================
@router.get("/calendar")
def calendar(employee_id: str, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """Get calendar items for the employee."""
    if not employee_id:
        raise HTTPException(status_code=400, detail="employee_id required")
 
    # Try custom model function first
    if get_employee_calendar:
        try:
            rows = get_employee_calendar(employee_id, from_date, to_date)
            return {"success": True, "data": rows}
        except Exception:
            pass
 
    # Fallback to direct DB query
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(dictionary=True)
   
    try:
        cur.execute(
            "SELECT p.POD_ID, p.Batch_Code FROM employee_record e JOIN pod p ON e.POD_ID = p.POD_ID WHERE e.Employee_ID = %s",
            (employee_id,)
        )
        pod_row = cur.fetchone()
       
        if not pod_row or not pod_row.get("POD_ID"):
            return {"success": True, "data": []}
       
        pod_id = pod_row.get("POD_ID")
        batch_code = pod_row.get("Batch_Code")
 
        # Check pod_deadline existence
        try:
            db_name = getattr(conn, "database", None)
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM information_schema.tables WHERE table_schema = %s AND table_name = 'pod_deadline'",
                (db_name,)
            )
            has_pod_deadline = bool(cur.fetchone().get('cnt'))
        except Exception:
            has_pod_deadline = False
 
        if has_pod_deadline:
            sql = """
            SELECT DISTINCT
                t.Task_Slno as id,
                COALESCE(a.Name, c.Name, co.Name) AS title,
                t.Task_Type as type,
                COALESCE(pd.Deadline_Date, t.Deadline_Date) AS start,
                CASE
                  WHEN t.Task_Type='Assessment' AND ar.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type='Certification' AND cr.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type='Course' AND cor.Record_ID IS NOT NULL THEN 'completed'
                  ELSE 'assigned'
                END AS status
            FROM deadline_table t
            LEFT JOIN pod_deadline pd ON pd.Task_Slno = t.Task_Slno AND pd.POD_ID = %s
            LEFT JOIN assessment_table a ON (t.Task_Type='Assessment' AND t.Task_ID = a.Assessment_ID)
            LEFT JOIN certification_table c ON (t.Task_Type='Certification' AND t.Task_ID = c.Certification_ID)
            LEFT JOIN courses_table co ON (t.Task_Type='Course' AND t.Task_ID = co.Courses_ID)
            LEFT JOIN assessment_record ar ON (t.Task_Type='Assessment' AND t.Task_ID = ar.Assessment_ID AND ar.Employee_ID = %s)
            LEFT JOIN certification_record cr ON (t.Task_Type='Certification' AND t.Task_ID = cr.Certification_ID AND cr.Employee_ID = %s)
            LEFT JOIN courses_record cor ON (t.Task_Type='Course' AND t.Task_ID = cor.Course_ID AND cor.Employee_ID = %s)
            WHERE t.Batch_Code = %s
            """
            params = [pod_id, employee_id, employee_id, employee_id, batch_code]
        else:
            sql = """
            SELECT DISTINCT
                t.Task_Slno as id,
                COALESCE(a.Name, c.Name, co.Name) AS title,
                t.Task_Type as type,
                t.Deadline_Date AS start,
                CASE
                  WHEN t.Task_Type='Assessment' AND ar.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type='Certification' AND cr.Record_ID IS NOT NULL THEN 'completed'
                  WHEN t.Task_Type='Course' AND cor.Record_ID IS NOT NULL THEN 'completed'
                  ELSE 'assigned'
                END AS status
            FROM deadline_table t
            LEFT JOIN assessment_table a ON (t.Task_Type='Assessment' AND t.Task_ID = a.Assessment_ID)
            LEFT JOIN certification_table c ON (t.Task_Type='Certification' AND t.Task_ID = c.Certification_ID)
            LEFT JOIN courses_table co ON (t.Task_Type='Course' AND t.Task_ID = co.Courses_ID)
            LEFT JOIN assessment_record ar ON (t.Task_Type='Assessment' AND t.Task_ID = ar.Assessment_ID AND ar.Employee_ID = %s)
            LEFT JOIN certification_record cr ON (t.Task_Type='Certification' AND t.Task_ID = cr.Certification_ID AND cr.Employee_ID = %s)
            LEFT JOIN courses_record cor ON (t.Task_Type='Course' AND t.Task_ID = cor.Course_ID AND cor.Employee_ID = %s)
            WHERE t.Batch_Code = %s
            """
            params = [employee_id, employee_id, employee_id, batch_code]
 
        if from_date and to_date:
            if has_pod_deadline:
                sql += " AND (COALESCE(pd.Deadline_Date, t.Deadline_Date) BETWEEN %s AND %s)"
            else:
                sql += " AND (t.Deadline_Date BETWEEN %s AND %s)"
            params.extend([from_date, to_date])
 
        sql += " ORDER BY start"
        cur.execute(sql, tuple(params))
        rows = cur.fetchall() or []
 
        for r in rows:
            if "start" in r and hasattr(r["start"], "isoformat"):
                r["start"] = r["start"].isoformat()
            r["completed"] = (r.get("status") == "completed")
 
        return {"success": True, "data": rows}
   
    finally:
        cur.close()
        close_db_connection(conn)
 
 
# ==========================================
# 4. GET SINGLE ITEM DETAILS
# ==========================================
@router.get("/item/{task_slno}")
def item_detail(task_slno: int):
    """Fetch single deadline row by Task_Slno."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(dictionary=True)
   
    try:
        cur.execute("SELECT * FROM deadline_table WHERE Task_Slno = %s", (task_slno,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        if "Deadline_Date" in row and hasattr(row["Deadline_Date"], "isoformat"):
            row["Deadline_Date"] = row["Deadline_Date"].isoformat()
        return {"success": True, "data": row}
   
    finally:
        cur.close()
        close_db_connection(conn)
 
 
# ==========================================
# 5. SUBMIT TASK (WITH FILE UPLOAD)
# ==========================================
@router.post("/submit/{task_slno}")
async def submit_task(
    task_slno: int,
    employee_id: str = Form(...),
    marks_scored: Optional[float] = Form(None),
    notes: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Submit a task for an employee.
    - Assessment: Requires marks_scored + file
    - Certification: Requires marks_scored + file
    - Course: Optional marks_scored, optional file
    """
    if not employee_id:
        raise HTTPException(status_code=400, detail="employee_id required")
 
    print(f"📥 Submitting task {task_slno} for employee {employee_id}")
    print(f"   Marks: {marks_scored}, Notes: {notes}, File: {file.filename if file else 'None'}")
 
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(dictionary=True)
   
    try:
        # Get task details
        cur.execute("SELECT Task_Slno, Task_ID, Task_Type FROM deadline_table WHERE Task_Slno = %s", (task_slno,))
        task = cur.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
 
        task_type = task["Task_Type"]
        task_id = task["Task_ID"]
       
        print(f"   Task Type: {task_type}, Task ID: {task_id}")
 
        # Save file if provided
        saved_path = None
        if file:
            file_name = f"{employee_id}_{task_slno}_{file.filename}"
            saved_path = os.path.join(UPLOAD_DIR, file_name)
            with open(saved_path, "wb") as f:
                content = await file.read()
                f.write(content)
            print(f"✅ File saved: {saved_path}")
 
        # Insert record based on task type
        try:
            if task_type == "Assessment":
                cur.execute(
                    "INSERT INTO assessment_record (Upload_Time, Document, Mark_Secured, Assessment_ID, Employee_ID) VALUES (NOW(), %s, %s, %s, %s)",
                    (saved_path, marks_scored, task_id, employee_id),
                )
            elif task_type == "Certification":
                cur.execute(
                    "INSERT INTO certification_record (Upload_Time, Document, Mark_Secured, Certification_ID, Employee_ID) VALUES (NOW(), %s, %s, %s, %s)",
                    (saved_path, marks_scored, task_id, employee_id),
                )
            elif task_type == "Course":
                cur.execute(
                    "INSERT INTO courses_record (Completion_Datetime, Document, Course_ID, Employee_ID) VALUES (NOW(), %s, %s, %s)",
                    (saved_path, task_id, employee_id),
                )
            else:
                raise HTTPException(status_code=400, detail="Unsupported Task_Type")
           
            conn.commit()
            print(f"✅ Record inserted successfully")
            return {"success": True, "message": "Submission saved"}
       
        except Exception as e:
            conn.rollback()
            print(f"❌ Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
   
    finally:
        cur.close()
        close_db_connection(conn)