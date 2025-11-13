from fastapi import APIRouter, Path, Query
from schemas.certification import CertificationCreate, CertificationUpdate
from services import certification_service
from models import certification as certification_model

router = APIRouter()

@router.get("/count")
def get_certification_count():
    """
    Get total number of certifications
    """
    count = certification_model.get_certification_count()
    return {
        "success": True,
        "message": "Total certifications fetched successfully",
        "total": count
    }

@router.get("/get-all")
def get_all_certifications(
    include_stats: bool = Query(
        False,
        description="Include completion statistics for certifications (total_completed, average_score)"
    )
):
    """
    Get all certifications

    Query Parameters:
    - **include_stats**: Include statistics (default: False)

    Returns:
    - List of all certifications
    """
    return certification_service.get_all_certifications(include_stats=include_stats)


@router.get("/{certification_id}")
def get_certification_by_id(
    certification_id: str = Path(..., description="Certification ID to retrieve")
):
    """
    Get specific certification by ID

    Path Parameters:
    - **certification_id**: Unique certification identifier

    Returns:
    - Certification details
    """
    return certification_service.get_certification_by_id(certification_id)


@router.post("/create-certification")
def create_certification(certification: CertificationCreate):
    """
    Create new certification

    Request Body:
    - **certification_id**: Unique certification ID
    - **name**: Certification name (required)
    - **link**: Certification link (optional)

    Returns:
    - Created certification details
    """
    return certification_service.create_certification(certification)


@router.put("/{certification_id}")
def update_certification(
    certification_id: str = Path(..., description="Certification ID to update"),
    certification: CertificationUpdate = None
):
    """
    Update existing certification

    Path Parameters:
    - **certification_id**: Certification ID to update

    Request Body:
    - **name**: Updated certification name
    - **link**: Updated certification link

    Returns:
    - Updated certification details
    """
    return certification_service.update_certification(certification_id, certification)


@router.delete("/{certification_id}")
def delete_certification(
    certification_id: str = Path(..., description="Certification ID to delete")
):
    """
    Delete certification

    Path Parameters:
    - **certification_id**: Certification ID to delete

    Note:
    - Cannot delete certification if it has existing records

    Returns:
    - Deletion confirmation
    """
    return certification_service.delete_certification(certification_id)


