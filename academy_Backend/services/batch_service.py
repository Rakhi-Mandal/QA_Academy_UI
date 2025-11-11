from fastapi import HTTPException
from models import batch as batch_db


def get_all_batches(include_stats: bool = False):
    """Get all batches with optional statistics"""
    try:
        if include_stats:
            batches = batch_db.get_batches_with_stats()
        else:
            batches = batch_db.get_all_batches()
        
        return {
            "success": True,
            "data": batches,
            "total": len(batches)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching batches: {str(e)}")

def get_batch_count():
    """Get total count of batches"""
    try:
        count = batch_db.get_batch_count()
        
        return {
            "success": True,
            "total": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching batch count: {str(e)}")