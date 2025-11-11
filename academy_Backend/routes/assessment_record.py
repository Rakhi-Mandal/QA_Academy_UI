from fastapi import APIRouter, Path, UploadFile, File, Form
from schemas.assessment_record import AssessmentRecordCreate, AssessmentRecordUpdate
from services import assessment_record_service
import os
from datetime import datetime

router = APIRouter()


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


@router.post("/")
def create_record(record: AssessmentRecordCreate):
    """Create new assessment record"""
    return assessment_record_service.create_record(record)


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
