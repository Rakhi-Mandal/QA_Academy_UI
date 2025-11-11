from models import certification_record as model
from schemas.certification_record import (
    CertificationRecordCreate,
    CertificationRecordUpdate,
    CertificationRecordResponse
)
from utils.response import success_response, error_response
from typing import Dict, List

def get_all_certification_records() -> Dict:
    """Get all certification records."""
    try:
        records = model.get_all_certification_records()
        
        if records is None:
            return error_response(message="Failed to retrieve records", status_code=500)

        return success_response(
            data=records,
            message=f"Retrieved {len(records)} certification record(s) successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving certification records: {str(e)}", status_code=500)

def get_record_by_id(record_id: int) -> Dict:
    """Get specific certification record by ID, handling serialization error."""
    try:
        # --- MODIFICATION: REMOVE redundant model.record_exists check ---
        # Relying on the single fetch to determine existence
        record = model.get_record_by_id(record_id)
        
        if record is None:
            # If the model returns None (meaning it was not found), return 404
            return error_response(message=f"Record with ID '{record_id}' not found", status_code=404)
        
        # Success: The record object (which is already serialized in the model)
        return success_response(data=record, message="Record retrieved successfully", status_code=200)
    
    except Exception as e:
        # If any other error occurs (like connection failure), return 500
        return error_response(message=f"Error retrieving record: {str(e)}", status_code=500)

def get_records_by_employee(employee_id: str) -> Dict:
    """Get all records for a specific employee."""
    try:
        records = model.get_records_by_employee(employee_id)
        if records is None:
            return error_response(message="Failed to retrieve records by employee", status_code=500)

        return success_response(
            data=records,
            message=f"Retrieved {len(records)} record(s) for employee {employee_id}",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving records: {str(e)}", status_code=500)

def get_records_by_certification(certification_id: str) -> Dict:
    """Get all records for a specific certification."""
    try:
        records = model.get_records_by_certification(certification_id)
        if records is None:
            return error_response(message="Failed to retrieve records by certification", status_code=500)

        return success_response(
            data=records,
            message=f"Retrieved {len(records)} record(s) for certification {certification_id}",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving records: {str(e)}", status_code=500)

def create_record(data: CertificationRecordCreate) -> Dict:
    """Create new certification record."""
    try:
        # Convert pydantic model to dictionary for the model layer
        record_data = data.model_dump()
        
        created_record = model.create_record(record_data)

        if not created_record:
            return error_response(message="Failed to create record", status_code=500)

        return success_response(data=created_record, message="Record created successfully", status_code=201)
    except Exception as e:
        return error_response(message=f"Error creating record: {str(e)}", status_code=500)

def update_record(record_id: int, data: CertificationRecordUpdate) -> Dict:
    """Update existing certification record."""
    try:
        if not model.record_exists(record_id):
            return error_response(message=f"Record with ID '{record_id}' not found", status_code=404)

        # Convert pydantic model to dictionary, excluding unset fields
        record_data = data.model_dump(exclude_unset=True)
        
        success = model.update_record(record_id, record_data)

        if not success:
            return error_response(message="Failed to update record", status_code=500)

        updated_record = model.get_record_by_id(record_id)
        return success_response(data=updated_record, message="Record updated successfully", status_code=200)

    except Exception as e:
        return error_response(message=f"Error updating record: {str(e)}", status_code=500)

def delete_record(record_id: int) -> Dict:
    """Delete certification record."""
    try:
        success, message = model.delete_record(record_id)

        if not success and "not found" in message:
            return error_response(message=message, status_code=404)
        elif not success:
            return error_response(message=message, status_code=500)

        return success_response(
            data={"record_id": record_id},
            message=message,
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error deleting record: {str(e)}", status_code=500)
    
def get_recent_certification_activity() -> Dict:
    """Get the 3 most recent certification completions for the dashboard."""
    try:
        # Calls the model function
        records = model.get_last_n_certification_records(limit=3)
        
        if records is None:
            return error_response(message="Failed to retrieve recent activity records", status_code=500)

        return success_response(
            data=records,
            message=f"Retrieved {len(records)} recent certification activities successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving recent activity: {str(e)}", status_code=500)
    
def get_records_by_employee_service(employee_id: str) -> Dict:
    """Get all certification records for a specific employee ID."""
    try:
        # Calls the model function which fetches the records
        records = model.get_records_by_employee(employee_id)
        
        if records is None:
            # This generally means a critical DB error occurred in the model layer
            return error_response(message="Failed to retrieve records by employee due to internal error", status_code=500)
        
        if not records:
            # If the list is empty, it's still a success, but we indicate zero records found
            return success_response(
                data=[],
                message=f"No certification records found for employee {employee_id}",
                status_code=200
            )

        return success_response(
            data=records,
            message=f"Retrieved {len(records)} record(s) for employee {employee_id} successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving records by employee: {str(e)}", status_code=500)