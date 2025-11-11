"""
Courses Routes - API endpoints
"""
from fastapi import APIRouter, Query, Path
from schemas.courses import CourseCreate, CourseUpdate
from services import courses_service

router = APIRouter()


@router.get("/get_all")
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


@router.get("/get_count")
def get_course_count():
    """
    Get total course count
    
    Returns:
    - Total number of courses
    
    Example Response:
    {
        "success": true,
        "data": {
            "total_courses": 25
        },
        "message": "Course count retrieved successfully"
    }
    """
    return courses_service.get_course_count()


@router.get("/recent-completions")
def get_recent_completions(
    limit: int = Query(
        2, 
        ge=1, 
        le=10, 
        description="Number of recent completions to retrieve (1-10)"
    )
):
    """
    Get recent course completions (Course Name and Employee Name only)
    
    Query Parameters:
    - **limit**: Number of recent completions (default: 2, max: 10)
    
    Returns:
    - List of recent course completions with course name and employee name
    
    Example Response:
    {
        "success": true,
        "data": [
            {
                "Course_Name": "Python Basics",
                "Employee_Name": "John Doe",
                "Completion_Datetime": "2024-11-17T16:40:00"
            },
            {
                "Course_Name": "Advanced Python",
                "Employee_Name": "Jane Smith",
                "Completion_Datetime": "2024-11-16T13:15:00"
            }
        ],
        "message": "Retrieved 2 recent completion(s) successfully"
    }
    """
    return courses_service.get_recent_completions(limit=limit)


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
    Create new course with auto-incremented ID
    
    Request Body:
    - **name**: Course name (required)
    - **link**: Course link/URL (optional)
    
    Note: Course ID is auto-generated (C01, C02, C03, etc.)
    
    Example:
    {
        "name": "Python for QA Engineers",
        "link": "https://courses.example.com/python-qa"
    }
    
    Returns:
    - Created course details with auto-generated ID
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
    
    Returns:
    - Deletion confirmation
    """
    return courses_service.delete_course(course_id)


@router.get("/{course_id}/employees")
def get_course_with_employees(
    course_id: str = Path(..., description="Course ID")
):
    """
    Get course details with list of employees who completed it
    
    Path Parameters:
    - **course_id**: Course ID
    
    Returns:
    - Course details and list of employees who completed it
    
    Example Response:
    {
        "success": true,
        "data": {
            "course": {
                "Courses_ID": "C01",
                "Name": "Python Basics",
                "Link": "https://..."
            },
            "employees": [...],
            "total_completed": 15
        }
    }
    """
    return courses_service.get_course_with_employees(course_id)