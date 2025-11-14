
from models import assessment as assessment_model
from schemas.assessment import AssessmentCreate, AssessmentUpdate, AssessmentResponse, AssessmentWithStats
from utils.response import success_response, error_response
from typing import Dict


def get_all_assessments(include_stats: bool = False) -> Dict:
    """
    Get all assessments with optional statistics
    
    Args:
        include_stats: If True, include completion statistics
        
    Returns:
        JSON response with assessments list
    """
    try:
        if include_stats:
            assessments = assessment_model.get_assessments_with_stats()
        else:
            assessments = assessment_model.get_all_assessments()
        
        if assessments is None:
            return error_response(
                message="Failed to retrieve assessments",
                status_code=500
            )
        
        return success_response(
            data=assessments,
            message=f"Retrieved {len(assessments)} assessment(s) successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving assessments: {str(e)}",
            status_code=500
        )


def get_assessment_by_id(assessment_id: str) -> Dict:
    """
    Get specific assessment by ID
    
    Args:
        assessment_id: Assessment ID to retrieve
        
    Returns:
        JSON response with assessment data
    """
    try:
        # Check if assessment exists
        if not assessment_model.assessment_exists(assessment_id):
            return error_response(
                message=f"Assessment with ID '{assessment_id}' not found",
                status_code=404
            )
        
        # Get assessment
        assessment = assessment_model.get_assessment_by_id(assessment_id)
        
        if not assessment:
            return error_response(
                message="Failed to retrieve assessment",
                status_code=500
            )
        
        return success_response(
            data=assessment,
            message="Assessment retrieved successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving assessment: {str(e)}",
            status_code=500
        )


def create_assessment(assessment_data: AssessmentCreate) -> Dict:
    """
    Create new assessment
    
    Args:
        assessment_data: Assessment creation data
        
    Returns:
        JSON response with created assessment
    """
    try:
        # Check if assessment already exists
        if assessment_model.assessment_exists(assessment_data.assessment_id):
            return error_response(
                message=f"Assessment with ID '{assessment_data.assessment_id}' already exists",
                status_code=409
            )
        
        # Create assessment
        success = assessment_model.create_assessment(
            assessment_id=assessment_data.assessment_id,
            name=assessment_data.name,
            link=assessment_data.link
        )
        
        if not success:
            return error_response(
                message="Failed to create assessment",
                status_code=500
            )
        
        # Get created assessment
        created_assessment = assessment_model.get_assessment_by_id(assessment_data.assessment_id)
        
        return success_response(
            data=created_assessment,
            message="Assessment created successfully",
            status_code=201
        )
    
    except Exception as e:
        return error_response(
            message=f"Error creating assessment: {str(e)}",
            status_code=500
        )


def update_assessment(assessment_id: str, assessment_data: AssessmentUpdate) -> Dict:
    """
    Update existing assessment
    
    Args:
        assessment_id: Assessment ID to update
        assessment_data: Updated assessment data
        
    Returns:
        JSON response with updated assessment
    """
    try:
        # Check if assessment exists
        if not assessment_model.assessment_exists(assessment_id):
            return error_response(
                message=f"Assessment with ID '{assessment_id}' not found",
                status_code=404
            )
        
        # Update assessment
        success = assessment_model.update_assessment(
            assessment_id=assessment_id,
            name=assessment_data.name,
            link=assessment_data.link
        )
        
        if not success:
            return error_response(
                message="Failed to update assessment",
                status_code=500
            )
        
        # Get updated assessment
        updated_assessment = assessment_model.get_assessment_by_id(assessment_id)
        
        return success_response(
            data=updated_assessment,
            message="Assessment updated successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error updating assessment: {str(e)}",
            status_code=500
        )


def delete_assessment(assessment_id: str) -> Dict:
    """
    Delete assessment
    
    Args:
        assessment_id: Assessment ID to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        # Check if assessment exists
        if not assessment_model.assessment_exists(assessment_id):
            return error_response(
                message=f"Assessment with ID '{assessment_id}' not found",
                status_code=404
            )
        
        # Delete assessment
        success, message = assessment_model.delete_assessment(assessment_id)
        
        if not success:
            # Check if it's because of existing records
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
            data={"assessment_id": assessment_id},
            message="Assessment deleted successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error deleting assessment: {str(e)}",
            status_code=500
        )
    
def get_assessment_count() -> Dict:
    try:
        count = assessment_model.get_assessment_count()
        return success_response(
            data={"total_assessments": count},
            message="Assessment count retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=f"Error retrieving assessment count: {str(e)}",
            status_code=500
        )
