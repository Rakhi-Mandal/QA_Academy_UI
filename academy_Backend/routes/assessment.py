
from fastapi import APIRouter, Query, Path
from schemas.assessment import AssessmentCreate, AssessmentUpdate
from services import assessment_service

router = APIRouter()


@router.get("/get-all")
def get_all_assessments(
    include_stats: bool = Query(
        False, 
        description="Include completion statistics (total_completed, average_score)"
    )
):
    """
    Get all assessments
    
    Query Parameters:
    - **include_stats**: Include statistics (default: False)
    
    Returns:
    - List of all assessments
    """
    return assessment_service.get_all_assessments(include_stats=include_stats)


@router.get("/{assessment_id}")
def get_assessment_by_id(
    assessment_id: str = Path(..., description="Assessment ID to retrieve")
):
    """
    Get specific assessment by ID
    
    Path Parameters:
    - **assessment_id**: Unique assessment identifier
    
    Returns:
    - Assessment details
    """
    return assessment_service.get_assessment_by_id(assessment_id)


@router.post("/create-assessment")
def create_assessment(assessment: AssessmentCreate):
    """
    Create new assessment
    
    Request Body:
    - **assessment_id**: Unique assessment ID
    - **name**: Assessment name (required)
    - **link**: Assessment link/URL (optional)
    
    Returns:
    - Created assessment details
    """
    return assessment_service.create_assessment(assessment)


@router.put("/{assessment_id}")
def update_assessment(
    assessment_id: str = Path(..., description="Assessment ID to update"),
    assessment: AssessmentUpdate = None
):
    """
    Update existing assessment
    
    Path Parameters:
    - **assessment_id**: Assessment ID to update
    
    Request Body:
    - **name**: Updated assessment name (required)
    - **scheduled_date**: Updated scheduled date (optional)
    - **link**: Updated assessment link (optional)
    
    Returns:
    - Updated assessment details
    """
    return assessment_service.update_assessment(assessment_id, assessment)


@router.delete("/{assessment_id}")
def delete_assessment(
    assessment_id: str = Path(..., description="Assessment ID to delete")
):
    """
    Delete assessment
    
    Path Parameters:
    - **assessment_id**: Assessment ID to delete
    
    Note:
    - Cannot delete assessment if it has existing records
    
    Returns:
    - Deletion confirmation
    """
    return assessment_service.delete_assessment(assessment_id)