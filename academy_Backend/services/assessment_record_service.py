from models import assessment_record as record_model
from schemas.assessment_record import AssessmentRecordCreate, AssessmentRecordUpdate
from utils.response import success_response, error_response
from typing import Dict


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


def create_record(record_data: AssessmentRecordCreate) -> Dict:
    try:
        success = record_model.create_record(
            upload_time=record_data.upload_time,
            document=record_data.document,
            mark_secured=record_data.mark_secured,
            assessment_id=record_data.assessment_id,
            employee_id=record_data.employee_id
        )
        if not success:
            return error_response("Failed to create record", 500)
        return success_response(None, "Record created successfully", 201)
    except Exception as e:
        return error_response(f"Error creating record: {str(e)}", 500)


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
