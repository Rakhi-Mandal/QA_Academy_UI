from database.connection import close_db_connection, get_db_connection
from fastapi import APIRouter, Path, UploadFile, File, Form
from schemas.assessment_record import AssessmentRecordCreate, AssessmentRecordUpdate
from services import assessment_record_service
import os
from starlette.concurrency import run_in_threadpool
from datetime import datetime
from typing import Dict, List, Optional

router = APIRouter()

# Static route first
@router.get("/recent")
def get_recent_records(limit: int = 2):
    """Fetch the most recent assessment records (default: 2)"""
    return assessment_record_service.get_recent_records(limit)

@router.get("/")
def get_all_records():
    """Get all assessment records"""
    return assessment_record_service.get_all_records()


@router.get("/{record_id}")
def get_record_by_id(record_id: int = Path(..., description="Record ID")):
    """Get specific assessment record"""
    return assessment_record_service.get_record_by_id(record_id)


@router.get("/employee/{employee_id}")
def get_records_by_employee(employee_id: str = Path(..., description="Employee ID")):
    """Get assessment records for specific employee"""
    return assessment_record_service.get_records_by_employee(employee_id)


@router.post("/create-record", status_code=201)
async def create_assessment_record_api(
    employee_id: str = Form(..., description="Employee ID"),
    assessment_id: str = Form(..., description="Assessment ID"),
    mark_secured: float = Form(..., description="Marks secured"),
    document: UploadFile = File(..., description="Assessment document file (PDF/Image)"),
    upload_time: Optional[str] = Form(None, description="Upload datetime (optional)")
):
    """Create a new assessment record, handling document upload."""
    record_data = {
        "employee_id": employee_id,
        "assessment_id": assessment_id,
        "mark_secured": mark_secured,
        "upload_time": upload_time or datetime.now().isoformat(timespec='seconds')
    }

    result = await run_in_threadpool(
        assessment_record_service.create_record_with_file,
        record_data,
        document   # ✅ pass `document` instead of `file`
    )
    return result

@router.put("/{record_id}")
def update_record(record_id: int, record: AssessmentRecordUpdate):
    """Update existing assessment record"""
    return assessment_record_service.update_record(record_id, record)


@router.delete("/{record_id}")
def delete_record(record_id: int):
    """Delete assessment record"""
    return assessment_record_service.delete_record(record_id)


@router.post("/upload")
async def upload_assessment_document(
    file: UploadFile = File(...),
    assessment_id: str = Form(...),
    employee_id: str = Form(...),
    mark_secured: float = Form(...)
):
    """Upload assessment document"""
    uploads_dir = "uploads/assessments"
    os.makedirs(uploads_dir, exist_ok=True)

    file_path = os.path.join(uploads_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    record_data = AssessmentRecordCreate(
        upload_time=datetime.utcnow(),
        document=file_path,
        mark_secured=mark_secured,
        assessment_id=assessment_id,
        employee_id=employee_id
    )

    return assessment_record_service.create_record(record_data)


# Parameterized route after
@router.get("/{record_id}")
def get_record_by_id(record_id: int = Path(..., description="Record ID")):
    """Get specific assessment record"""
    return assessment_record_service.get_record_by_id(record_id)
