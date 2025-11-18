from models import certification as model 
from schemas.certification import CertificationCreate, CertificationUpdate
from utils.response import success_response, error_response
from typing import Dict

def get_all_certifications(include_stats: bool = False) -> Dict:
    """Get all certifications with optional statistics."""
    try:
        certifications = model.get_all_certifications(include_stats=include_stats)
        if certifications is None:
            return error_response(message="Failed to retrieve certifications", status_code=500)

        return success_response(
            data=certifications,
            message=f"Retrieved {len(certifications)} certification(s) successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error retrieving certifications: {str(e)}", status_code=500)

# services/certification_service.py (Verification)

def get_certification_by_id(certification_id: str) -> Dict:
    """Get specific certification by ID."""
    try:
        # Note: You can remove the separate certification_exists check if you handle None from the model fetch
        certification = model.get_certification_by_id(certification_id) 
        
        if not certification:
            return error_response(message=f"Certification ID '{certification_id}' not found", status_code=404)
        
        return success_response(data=certification, message="Certification retrieved successfully", status_code=200)

    except Exception as e:
        return error_response(message=f"Error retrieving certification: {str(e)}", status_code=500)


def create_certification(certification_data: CertificationCreate) -> Dict:
    """Create new certification."""
    try:
        if model.certification_exists(certification_data.certification_id):
            return error_response(message=f"Certification ID '{certification_data.certification_id}' already exists", status_code=409)

        success = model.create_certification(
            certification_id=certification_data.certification_id,
            name=certification_data.name,
            link=certification_data.link
        )

        if not success:
            return error_response(message="Failed to create certification", status_code=500)

        # Retrieve the newly created record for the response
        created_certification = model.get_certification_by_id(certification_data.certification_id)
        return success_response(data=created_certification, message="Certification created successfully", status_code=201)

    except Exception as e:
        return error_response(message=f"Error creating certification: {str(e)}", status_code=500)

def update_certification(certification_id: str, certification_data: CertificationUpdate) -> Dict:
    """Update existing certification."""
    try:
        current_data = model.get_certification_by_id(certification_id) 
        if not current_data:
            return error_response(message=f"Certification ID '{certification_id}' not found", status_code=404)

        updated_data = certification_data.model_dump(exclude_unset=True)
        
        # Merge updated data with current data
        name = updated_data.get('name', current_data['Name'])
        link = updated_data.get('link', current_data['Link'])
        
        success = model.update_certification(
            certification_id=certification_id,
            name=name,
            link=link
        )

        if not success:
            return error_response(message="Failed to update certification (no rows affected)", status_code=500)

        updated_certification = model.get_certification_by_id(certification_id)
        return success_response(data=updated_certification, message="Certification updated successfully", status_code=200)

    except Exception as e:
        return error_response(message=f"Error updating certification: {str(e)}", status_code=500)


def delete_certification(certification_id: str) -> Dict:
    """Delete certification, handling foreign key constraints."""
    try:
        # Model handles the existence check and record check internally
        success, message = model.delete_certification(certification_id)

        if not success and "not found" in message:
            return error_response(message=message, status_code=404)
        elif not success and "existing records" in message:
            # Conflict status code for foreign key violation
            return error_response(message=message, status_code=409) 
        elif not success:
            return error_response(message=message, status_code=500)

        return success_response(
            data={"certification_id": certification_id},
            message=message,
            status_code=200
        )
    except Exception as e:
        return error_response(message=f"Error deleting certification: {str(e)}", status_code=500)
    
 