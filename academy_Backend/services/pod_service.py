from fastapi import HTTPException
from models import pod as pod_db
from schemas.pod import PODCreate


def get_all_pods():
    """Get all PODs"""
    try:
        pods = pod_db.get_all_pods()
        
        return {
            "success": True,
            "data": pods,
            "total": len(pods)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching PODs: {str(e)}")


def get_pods_by_batch(batch_code: str):
    """Get all PODs for a specific batch"""
    try:
        # Check if batch exists
        if not pod_db.batch_exists(batch_code):
            raise HTTPException(status_code=404, detail=f"Batch '{batch_code}' not found")
        
        pods = pod_db.get_pods_by_batch(batch_code)
        
        return {
            "success": True,
            "data": pods,
            "total": len(pods),
            "batch_code": batch_code
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching PODs: {str(e)}")

def get_pod_by_id(pod_id: str):
    """Get specific POD by ID"""
    try:
        pod = pod_db.get_pod_by_id(pod_id)
        
        if not pod:
            raise HTTPException(status_code=404, detail=f"POD '{pod_id}' not found")
        
        return {
            "success": True,
            "data": pod
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching POD: {str(e)}")


def create_pod(pod: PODCreate):
    """Create new POD"""
    try:
        # Check if POD already exists
        if pod_db.pod_exists(pod.pod_id):
            raise HTTPException(status_code=400, detail=f"POD '{pod.pod_id}' already exists")
        
        # Create POD
        success, message = pod_db.create_pod(
            pod_id=pod.pod_id,
            pod_name=pod.pod,
            batch_code=pod.batch_code
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        # Fetch and return created POD
        created_pod = pod_db.get_pod_by_id(pod.pod_id)
        return {
            "success": True,
            "message": message,
            "data": created_pod
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating POD: {str(e)}")


def get_employees_by_pod(pod_id: str):
    """Return employee list and total count for a given POD"""
    try:
        employees = pod_db.get_employees_by_pod(pod_id)
        
        if not employees:
            raise HTTPException(status_code=404, detail=f"No employees found for POD '{pod_id}'")
        
        return {
            "POD_ID": pod_id,
            "total_employees": len(employees),
            "employees": employees
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employees for POD: {str(e)}")
