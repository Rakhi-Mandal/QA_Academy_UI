from models import certification as certification_model
from schemas.certification import CertificationCreate, CertificationUpdate, CertificationResponse
from utils.response import success_response, error_response
from typing import Dict


def get_all_certifications() -> Dict:
    """
    Get all certifications

    Returns:
        JSON response with certifications list
    """
    try:
        certifications = certification_model.get_all_certifications()

        if certifications is None:
            return error_response(
                message="Failed to retrieve certifications",
                status_code=500
            )

        return success_response(
            data=certifications,
            message=f"Retrieved {len(certifications)} certification(s) successfully",
            status_code=200
        )

    except Exception as e:
        return error_response(
            message=f"Error retrieving certifications: {str(e)}",
            status_code=500
        )


def get_certification_by_id(certification_id: str) -> Dict:
    """
    Get specific certification by ID

    Args:
        certification_id: Certification ID to retrieve

    Returns:
        JSON response with certification data
    """
    try:
        if not certification_model.certification_exists(certification_id):
            return error_response(
                message=f"Certification with ID '{certification_id}' not found",
                status_code=404
            )

        certification = certification_model.get_certification_by_id(certification_id)

        if not certification:
            return error_response(
                message="Failed to retrieve certification",
                status_code=500
            )

        return success_response(
            data=certification,
            message="Certification retrieved successfully",
            status_code=200
        )

    except Exception as e:
        return error_response(
            message=f"Error retrieving certification: {str(e)}",
            status_code=500
        )


def create_certification(certification_data: CertificationCreate) -> Dict:
    """
    Create new certification

    Args:
        certification_data: Certification creation data

    Returns:
        JSON response with created certification
    """
    try:
        if certification_model.certification_exists(certification_data.certification_id):
            return error_response(
                message=f"Certification with ID '{certification_data.certification_id}' already exists",
                status_code=409
            )

        success = certification_model.create_certification(
            certification_id=certification_data.certification_id,
            name=certification_data.name,
            deadline_date=certification_data.deadline_date.isoformat() if certification_data.deadline_date else None,
            link=certification_data.link
        )

        if not success:
            return error_response(
                message="Failed to create certification",
                status_code=500
            )

        created_certification = certification_model.get_certification_by_id(certification_data.certification_id)

        return success_response(
            data=created_certification,
            message="Certification created successfully",
            status_code=201
        )

    except Exception as e:
        return error_response(
            message=f"Error creating certification: {str(e)}",
            status_code=500
        )


def update_certification(certification_id: str, certification_data: CertificationUpdate) -> Dict:
    """
    Update existing certification

    Args:
        certification_id: Certification ID to update
        certification_data: Updated certification data

    Returns:
        JSON response with updated certification
    """
    try:
        if not certification_model.certification_exists(certification_id):
            return error_response(
                message=f"Certification with ID '{certification_id}' not found",
                status_code=404
            )

        success = certification_model.update_certification(
            certification_id=certification_id,
            name=certification_data.name,
            deadline_date=certification_data.deadline_date.isoformat() if certification_data.deadline_date else None,
            link=certification_data.link
        )

        if not success:
            return error_response(
                message="Failed to update certification",
                status_code=500
            )

        updated_certification = certification_model.get_certification_by_id(certification_id)

        return success_response(
            data=updated_certification,
            message="Certification updated successfully",
            status_code=200
        )

    except Exception as e:
        return error_response(
            message=f"Error updating certification: {str(e)}",
            status_code=500
        )


def delete_certification(certification_id: str) -> Dict:
    """
    Delete certification

    Args:
        certification_id: Certification ID to delete

    Returns:
        JSON response confirming deletion
    """
    try:
        if not certification_model.certification_exists(certification_id):
            return error_response(
                message=f"Certification with ID '{certification_id}' not found",
                status_code=404
            )

        success, message = certification_model.delete_certification(certification_id)

        if not success:
            if "existing records" in message.lower():
                return error_response(
                    message=message,
                    status_code=409
                )
            return error_response(
                message=message,
                status_code=500
            )

        return success_response(
            data={"certification_id": certification_id},
            message="Certification deleted successfully",
            status_code=200
        )

    except Exception as e:
        return error_response(
            message=f"Error deleting certification: {str(e)}",
            status_code=500
        )
