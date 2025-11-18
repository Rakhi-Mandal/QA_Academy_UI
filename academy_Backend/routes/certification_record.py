from fastapi import APIRouter, Path, Body, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from schemas.certification_record import (
    CertificationRecordCreate, 
    CertificationRecordUpdate, 
    CertificationRecordResponse
) 
from services import certification_record_service
from typing import List, Dict

# Set the router prefix for clarity (Only define router once)
router = APIRouter(prefix="/certification-records", tags=["Certification Records"])

# router = APIRouter(prefix="/certification-records", tags=["Certification Records"])

# PRIORITY 1: GET RECORDS BY EMPLOYEE (SPECIFIC PATH)
@router.get(
    "/employee/{employee_id}", 
    # CRITICAL: Add response model here
    response_model=List[CertificationRecordResponse], 
    response_model_by_alias=False
)
async def get_records_by_employee_api(
    employee_id: str = Path(..., description="The ID of the employee to retrieve records for")
):
    """Get all certification records associated with a given Employee ID."""
    # CRITICAL: Add logic to call the service
    result = await run_in_threadpool(
        certification_record_service.get_records_by_employee_service, 
        employee_id
    )
    return result

# --- GET ALL RECORDS ---
@router.get(
    "/get-all",
    response_model=List[CertificationRecordResponse],
    response_model_by_alias=False
)
async def get_all_certification_records_api():
    """Get all certification records."""
    result = await run_in_threadpool(certification_record_service.get_all_certification_records)
    return result

# --- CREATE RECORD (Handles file upload) ---
@router.post(
    "/create-record",
    status_code=201,
    response_model=CertificationRecordResponse,
    response_model_by_alias=False
)
async def create_certification_record_api(
    employee_id: str = Form(..., description="Employee ID"),
    certification_id: str = Form(..., description="Certification ID"),
    mark_secured: float = Form(..., description="Mark secured"),
    document: UploadFile = File(..., description="Certification document file (PDF/Image)")
):
    """Create a new certification record, handling document upload."""
    record_data = {
        "employee_id": employee_id,
        "certification_id": certification_id,
        "mark_secured": mark_secured
    }
    result = await run_in_threadpool(
        certification_record_service.create_certification_record, 
        record_data, 
        document
    )
    return result

# --- UPDATE RECORD ---
@router.put(
    "/{record_id}",
    response_model=CertificationRecordResponse,
    response_model_by_alias=False
)
async def update_certification_record_api(
    record_id: int = Path(..., description="Record ID to update"),
    update_data: CertificationRecordUpdate = Body(..., description="Fields to update")
):
    """Update details of a certification record."""
    result = await run_in_threadpool(
        certification_record_service.update_certification_record, 
        record_id, 
        update_data
    )
    return result

# --- DELETE RECORD ---
@router.delete(
    "/{record_id}",
    response_model=Dict[str, str]
)
async def delete_certification_record_api(
    record_id: int = Path(..., description="Record ID to delete")
):
    """Delete a certification record by ID (and delete the associated file)."""
    result = await run_in_threadpool(certification_record_service.delete_certification_record, record_id)
    return result

 