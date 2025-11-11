from fastapi import APIRouter, Query, Path
from services import batch_service

router = APIRouter()


@router.get("/get-all")
def get_all_batches(
    include_stats: bool = Query(
        False, 
        description="Include student count statistics (total_students)"
    )
):
    """
    Get all batches
    
    Query Parameters:
    - **include_stats**: Include statistics (default: False)
    
    Returns:
    - List of all batches
    """
    return batch_service.get_all_batches(include_stats=include_stats)