"""
Course Record Routes - API endpoints
"""
from fastapi import APIRouter, Path, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from schemas.course_record import CourseRecordCreate, CourseRecordUpdate
from services import course_record_service
from datetime import datetime

router = APIRouter()


@router.get("/get-all")
def get_all_course_records():
    """
    Get all course records
    
    Returns:
    - List of all course records with course and employee details
    """
    return course_record_service.get_all_course_records()


@router.get("/{record_id}")
def get_record_by_id(
    record_id: int = Path(..., gt=0, description="Course record ID")
):
    """
    Get specific course record by ID
    
    Path Parameters:
    - **record_id**: Unique record identifier
    
    Returns:
    - Course record details
    """
    return course_record_service.get_record_by_id(record_id)


@router.get("/employee/{employee_id}")
def get_records_by_employee(
    employee_id: str = Path(..., description="Employee ID")
):
    """
    Get all course records for a specific employee
    
    Path Parameters:
    - **employee_id**: Employee ID
    
    Returns:
    - List of course records for the employee
    """
    return course_record_service.get_records_by_employee(employee_id)


@router.get("/course/{course_id}")
def get_records_by_course(
    course_id: str = Path(..., description="Course ID")
):
    """
    Get all records for a specific course
    
    Path Parameters:
    - **course_id**: Course ID
    
    Returns:
    - List of employees who completed the course
    """
    return course_record_service.get_records_by_course(course_id)


@router.post("/create-record")
def create_record(record: CourseRecordCreate):
    """
    Create new course record (without file)
    
    Request Body:
    - **course_id**: Course ID (required)
    - **employee_id**: Employee ID (required)
    - **completion_datetime**: Completion date and time (ISO format)
    
    Example:
    {
        "course_id": "C01",
        "employee_id": "FS452",
        "completion_datetime": "2024-11-15T14:30:00"
    }
    
    Returns:
    - Created course record
    """
    return course_record_service.create_record(record)


@router.post("/upload")
async def upload_course_record(
    file: UploadFile = File(..., description="Course completion document (PDF, JPG, PNG)"),
    course_id: str = Form(..., description="Course ID"),
    employee_id: str = Form(..., description="Employee ID"),
    completion_datetime: str = Form(..., description="Completion datetime (YYYY-MM-DDTHH:MM:SS)")
):
    """
    Create course record with file upload
    
    Form Data:
    - **file**: Document file (PDF, JPG, JPEG, PNG - max 5MB)
    - **course_id**: Course ID
    - **employee_id**: Employee ID
    - **completion_datetime**: Completion datetime (ISO format: 2024-11-15T14:30:00)
    
    Returns:
    - Created course record with document
    """
    return course_record_service.create_record_with_file(
        file=file,
        course_id=course_id,
        employee_id=employee_id,
        completion_datetime=completion_datetime
    )


@router.put("/{record_id}")
def update_record(
    record_id: int = Path(..., gt=0, description="Course record ID"),
    record: CourseRecordUpdate = None
):
    """
    Update course record
    
    Path Parameters:
    - **record_id**: Record ID to update
    
    Request Body:
    - **completion_datetime**: Updated completion datetime (optional)
    
    Returns:
    - Updated course record
    """
    return course_record_service.update_record(record_id, record)


@router.delete("/{record_id}")
def delete_record(
    record_id: int = Path(..., gt=0, description="Course record ID")
):
    """
    Delete course record
    
    Path Parameters:
    - **record_id**: Record ID to delete
    
    Note:
    - Associated document file will also be deleted
    
    Returns:
    - Deletion confirmation
    """
    return course_record_service.delete_record(record_id)


@router.get("/{record_id}/download")
def download_document(
    record_id: int = Path(..., gt=0, description="Course record ID")
):
    """
    Download course completion document
    
    Path Parameters:
    - **record_id**: Record ID
    
    Returns:
    - File download
    """
    file_path, error = course_record_service.get_document_download_path(record_id)
    
    if error:
        return error
    
    return FileResponse(
        path=file_path,
        filename=file_path.split("\\")[-1],  # Windows path
        media_type='application/octet-stream'
    )