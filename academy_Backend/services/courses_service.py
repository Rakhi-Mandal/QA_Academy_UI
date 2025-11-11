"""
Courses Service - Business logic
"""
from models import courses as courses_model
from schemas.courses import CourseCreate, CourseUpdate
from utils.response import success_response, error_response
from typing import Dict


def get_all_courses(include_stats: bool = False) -> Dict:
    """
    Get all courses with optional statistics
    
    Args:
        include_stats: If True, include completion statistics
        
    Returns:
        JSON response with courses list
    """
    try:
        if include_stats:
            courses = courses_model.get_courses_with_stats()
        else:
            courses = courses_model.get_all_courses()
        
        if courses is None:
            return error_response(
                message="Failed to retrieve courses",
                status_code=500
            )
        
        return success_response(
            data=courses,
            message=f"Retrieved {len(courses)} course(s) successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving courses: {str(e)}",
            status_code=500
        )


def get_course_by_id(course_id: str) -> Dict:
    """
    Get specific course by ID
    
    Args:
        course_id: Course ID to retrieve
        
    Returns:
        JSON response with course data
    """
    try:
        # Check if course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        # Get course
        course = courses_model.get_course_by_id(course_id)
        
        if not course:
            return error_response(
                message="Failed to retrieve course",
                status_code=500
            )
        
        return success_response(
            data=course,
            message="Course retrieved successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving course: {str(e)}",
            status_code=500
        )


def create_course(course_data: CourseCreate) -> Dict:
    """
    Create new course with auto-incremented ID
    
    Args:
        course_data: Course creation data (name and link only)
        
    Returns:
        JSON response with created course
    """
    try:
        # Get next auto-incremented course ID
        next_course_id = courses_model.get_next_course_id()
        
        if not next_course_id:
            return error_response(
                message="Failed to generate course ID",
                status_code=500
            )

        # Create course
        success = courses_model.create_course(
            courses_id=next_course_id,
            name=course_data.name,
            link=course_data.link
        )

        if not success:
            return error_response(
                message="Failed to create course",
                status_code=500
            )

        # Retrieve created course
        created_course = courses_model.get_course_by_id(next_course_id)

        return success_response(
            data=created_course,
            message=f"Course created successfully with ID: {next_course_id}",
            status_code=201
        )

    except Exception as e:
        return error_response(
            message=f"Error creating course: {str(e)}",
            status_code=500
        )


def update_course(course_id: str, course_data: CourseUpdate) -> Dict:
    """
    Update existing course
    
    Args:
        course_id: Course ID to update
        course_data: Updated course data
        
    Returns:
        JSON response with updated course
    """
    try:
        # Check if course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        # Update course
        success = courses_model.update_course(
            courses_id=course_id,
            name=course_data.name,
            link=course_data.link
        )
        
        if not success:
            return error_response(
                message="Failed to update course",
                status_code=500
            )
        
        # Retrieve updated course
        updated_course = courses_model.get_course_by_id(course_id)
        
        return success_response(
            data=updated_course,
            message="Course updated successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error updating course: {str(e)}",
            status_code=500
        )


def delete_course(course_id: str) -> Dict:
    """
    Delete course
    
    Args:
        course_id: Course ID to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        # Check if course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        # Check if course has records
        if courses_model.course_has_records(course_id):
            return error_response(
                message="Cannot delete course with existing completion records",
                status_code=409
            )
        
        # Delete course
        success, message = courses_model.delete_course(course_id)
        
        if not success:
            return error_response(
                message=message,
                status_code=500
            )
        
        return success_response(
            data={"courses_id": course_id},
            message="Course deleted successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error deleting course: {str(e)}",
            status_code=500
        )


def get_course_with_employees(course_id: str) -> Dict:
    """
    Get course with list of employees who completed it
    
    Args:
        course_id: Course ID
        
    Returns:
        JSON response with course and employee list
    """
    try:
        # Check if course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        # Get course details
        course = courses_model.get_course_by_id(course_id)
        
        # Get employees who completed this course
        from models import course_record as record_model
        employees = record_model.get_records_by_course(course_id)
        
        return success_response(
            data={
                "course": course,
                "employees": employees,
                "total_completed": len(employees) if employees else 0
            },
            message="Course details with employees retrieved successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving course details: {str(e)}",
            status_code=500
        )


def get_course_count() -> Dict:
    """
    Get total course count
    
    Returns:
        JSON response with total course count
    """
    try:
        # Fetch course count from model
        total_courses = courses_model.get_course_count()

        # Build and return success response
        return success_response(
            data={"total_courses": total_courses},
            message="Course count retrieved successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving course count: {str(e)}",
            status_code=500
        )


def get_recent_completions(limit: int = 2) -> Dict:
    """
    Get recent course completions with course name and employee name
    
    Args:
        limit: Number of recent completions to retrieve (default: 2)
        
    Returns:
        JSON response with recent completions (Course_Name, Employee_Name, Completion_Datetime)
    """
    try:
        # Fetch recent completions from model
        recent_completions = courses_model.get_recent_course_completions(limit)

        # Build and return success response
        return success_response(
            data=recent_completions,
            message=f"Retrieved {len(recent_completions)} recent completion(s) successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving recent completions: {str(e)}",
            status_code=500
        )