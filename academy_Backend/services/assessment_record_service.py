from models import assessment_record as record_model
from schemas.assessment_record import AssessmentRecordCreate, AssessmentRecordUpdate
from utils.response import success_response, error_response
from typing import Dict
import os
from datetime import datetime


def get_all_records() -> Dict:
    try:
        records = record_model.get_all_records()
        return success_response(records, "Records retrieved successfully", 200)
    except Exception as e:
        return error_response(f"Error retrieving records: {str(e)}", 500)


def get_record_by_id(record_id: int) -> Dict:
    try:
        record = record_model.get_record_by_id(record_id)
        if not record:
            return error_response("Record not found", 404)
        return success_response(record, "Record retrieved successfully", 200)
    except Exception as e:
        return error_response(f"Error retrieving record: {str(e)}", 500)


def get_records_by_employee(employee_id: str) -> Dict:
    try:
        records = record_model.get_records_by_employee(employee_id)
        return success_response(records, "Employee records retrieved successfully", 200)
    except Exception as e:
        return error_response(f"Error retrieving employee records: {str(e)}", 500)


def create_record_with_file(record_data, document):
    """Save uploaded file and create record in DB"""
    try:
        uploads_dir = "uploads/assessments"
        os.makedirs(uploads_dir, exist_ok=True)

        # Create a safe filename
        safe_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{document.filename}"
        file_path = os.path.join(uploads_dir, safe_filename)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(document.file.read())

        # Store record in DB
        success = record_model.create_record(
            upload_time=record_data["upload_time"],
            document=file_path.replace("\\", "/"),
            mark_secured=record_data["mark_secured"],
            assessment_id=record_data["assessment_id"],
            employee_id=record_data["employee_id"]
        )

        if not success:
            return error_response("Failed to create assessment record", 500)

        return success_response(None, "Assessment record created successfully", 201)

    except Exception as e:
        return error_response(f"Error creating assessment record: {str(e)}", 500)

def update_record(record_id: int, record_data: AssessmentRecordUpdate) -> Dict:
    try:
        success = record_model.update_record(
            record_id=record_id,
            document=record_data.document,
            mark_secured=record_data.mark_secured
        )
        if not success:
            return error_response("Record not found or update failed", 404)
        return success_response(None, "Record updated successfully", 200)
    except Exception as e:
        return error_response(f"Error updating record: {str(e)}", 500)


def delete_record(record_id: int) -> Dict:
    try:
        success = record_model.delete_record(record_id)
        if not success:
            return error_response("Record not found", 404)
        return success_response(None, "Record deleted successfully", 200)
    except Exception as e:
        return error_response(f"Error deleting record: {str(e)}", 500)

def get_recent_records(limit: int = 2):
    try:
        records = record_model.get_recent_records(limit)
        return success_response(records, "Recent records fetched successfully", 200)
    except Exception as e:
        return error_response(f"Error fetching recent records: {str(e)}", 500)
