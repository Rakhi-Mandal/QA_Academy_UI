"""
Courses Routes - API endpoints
"""
from fastapi import APIRouter, Query, Path
from schemas.courses import CourseCreate, CourseUpdate
from services import courses_service

router = APIRouter()


@router.get("/get_all")  # ✅ Changed to match your URL
def get_all_courses(
    include_stats: bool = Query(
        False, 
        description="Include completion statistics (total_completed)"
    )
):
    """
    Get all courses
    
    Query Parameters:
    - **include_stats**: Include statistics (default: False)
    
    Returns:
    - List of all courses
    """
    return courses_service.get_all_courses(include_stats=include_stats)


@router.get("/{course_id}")
def get_course_by_id(
    course_id: str = Path(..., description="Course ID to retrieve")
):
    """
    Get specific course by ID
    
    Path Parameters:
    - **course_id**: Unique course identifier
    
    Returns:
    - Course details
    """
    return courses_service.get_course_by_id(course_id)

@router.post("/create-course")
def create_course(course: CourseCreate):
    """
    Create new course WITH deadlines
    
    Request Body:
    - **courses_id**: Unique course ID (required)
    - **name**: Course name (required)
    - **link**: Course link/URL (optional)
    - **deadlines**: List of deadlines for different batches (required)
      - Each deadline must have: batch_code and deadline_date
    
    Example:
    {
        "courses_id": "C24",
        "name": "Python for QA",
        "link": "https://...",
        "deadlines": [
            {"batch_code": 1, "deadline_date": "2025-12-31"},
            {"batch_code": 2, "deadline_date": "2026-01-31"}
        ]
    }
    
    Returns:
    - Created course details with deadlines
    """
    return courses_service.create_course(course)


@router.put("/{course_id}")
def update_course(
    course_id: str = Path(..., description="Course ID to update"),
    course: CourseUpdate = None
):
    """
    Update existing course
    
    Path Parameters:
    - **course_id**: Course ID to update
    
    Request Body:
    - **name**: Updated course name (required)
    - **link**: Updated course link (optional)
    
    Note: To update deadlines, use the deadline management endpoints
    
    Returns:
    - Updated course details
    """
    return courses_service.update_course(course_id, course)


@router.delete("/{course_id}")
def delete_course(
    course_id: str = Path(..., description="Course ID to delete")
):
    """
    Delete course
    
    Path Parameters:
    - **course_id**: Course ID to delete
    
    Note:
    - Cannot delete course if it has existing records
    - All deadlines for this course will also be deleted
    
    Returns:
    - Deletion confirmation
    """
    return courses_service.delete_course(course_id)


@router.get("/get_count")  # ✅ Changed to match your URL
def get_course_count(
    include_stats: bool = Query(
        False, 
        description="Include completion statistics (total_completed)"
    )
):
    """
    Get all courses
    
    Query Parameters:
    - **include_stats**: Include statistics (default: False)
    
    Returns:
    - List of all courses
    """
    return courses_service.get_course_count(include_stats=include_stats)