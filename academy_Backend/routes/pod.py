from fastapi import APIRouter, Query, Path
from schemas.pod import PODCreate
from services import pod_service

router = APIRouter()


@router.get("/get-all")
def get_all_pods():
    """
    Get all PODs

    Returns:
    - List of all PODs with POD_ID, POD, Batch_code
    """
    return pod_service.get_all_pods()


@router.get("/batch/{batch_code}")
def get_pods_by_batch(
    batch_code: str = Path(..., description="Batch code to filter PODs")
):
    """
    Get all PODs for a specific batch

    Path Parameters:
    - **batch_code**: Batch code (Foreign Key)

    Returns:
    - List of PODs belonging to the specified batch
    """
    return pod_service.get_pods_by_batch(batch_code)


@router.post("/create-pod")
def create_pod(pod: PODCreate):
    """
    Create new POD

    Request Body:
    - **pod_id**: Unique POD ID (required)
    - **pod**: POD name (required)
    - **batch_code**: Batch code/Foreign Key (required)

    Note:
    - batch_code must exist in batch_table

    Returns:
    - Created POD details
    """
    return pod_service.create_pod(pod)

@router.get("/{pod_id}/employees")
def get_employees_by_pod(pod_id: str):
    """Get all employees and count under a specific POD"""
    return pod_service.get_employees_by_pod(pod_id)
