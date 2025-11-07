from fastapi import APIRouter, Query, Path
from schemas.certification import CertificationCreate, CertificationUpdate
from services import certification_service

router = APIRouter()


@router.get("/get-all")
def get_all_certifications():
    """
    Get all certifications

    Returns:
    - List of all certifications
    """
    return certification_service.get_all_certifications()


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
    - **deadline_date**: Deadline date (optional, format: YYYY-MM-DD)
    - **link**: Certification link/URL (optional)

    Returns:
    - Created certification details
    """
    return certification_service.create_certification(
        certification.certification_id,
        certification.name,
        certification.deadline_date,
        certification.link
    )


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
    - **name**: Updated certification name (required)
    - **deadline_date**: Updated deadline date (optional)
    - **link**: Updated certification link (optional)

    Returns:
    - Updated certification details
    """
    return certification_service.update_certification(
        certification_id,
        certification.name,
        certification.deadline_date,
        certification.link
    )


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
