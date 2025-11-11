"""
Courses Service - Business logic (WITH Deadline Management)
"""
from models import courses as courses_model
# from models import deadline as deadline_model
from schemas.courses import CourseCreate, CourseUpdate
from utils.response import success_response, error_response
from typing import Dict


def get_all_courses(include_stats: bool = False, batch_code: int = None) -> Dict:
    """
    Get all courses with optional statistics and deadlines
    
    Args:
        include_stats: If True, include completion statistics
        batch_code: If provided, include deadlines for this batch
        
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
        
        # If batch_code provided, add deadline info for each course
        # if batch_code:
        #     for course in courses:
        #         deadline = deadline_model.get_deadline_by_task_and_batch(
        #             course['Courses_ID'], 
        #             'Course', 
        #             batch_code
        #         )
        #         course['deadline'] = deadline['Deadline_Date'] if deadline else None
        
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


def get_course_by_id(course_id: str, batch_code: int = None) -> Dict:
    """
    Get specific course by ID with optional deadline info
    
    Args:
        course_id: Course ID to retrieve
        batch_code: If provided, include deadline for this batch
        
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
        
        # Get all deadlines for this course
        # deadlines = deadline_model.get_deadlines_by_task(course_id, 'Course')
        # course['deadlines'] = deadlines
        
        # # If specific batch requested, add that deadline
        # if batch_code:
        #     deadline = deadline_model.get_deadline_by_task_and_batch(
        #         course_id, 
        #         'Course', 
        #         batch_code
        #     )
        #     course['deadline'] = deadline['Deadline_Date'] if deadline else None
        
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
    Create new course (no deadlines)
    """
    try:
        # Check if course already exists
        if courses_model.course_exists(course_data.courses_id):
            return error_response(
                message=f"Course with ID '{course_data.courses_id}' already exists",
                status_code=409
            )

        # Create course
        success = courses_model.create_course(
            courses_id=course_data.courses_id,
            name=course_data.name,
            link=course_data.link
        )

        if not success:
            return error_response(
                message="Failed to create course",
                status_code=500
            )

        # ✅ FIX: call the function correctly
        created_course = courses_model.get_course_by_id(course_data.courses_id)

        return success_response(
            data=created_course,
            message="Course created successfully",
            status_code=201
        )

    except Exception as e:
        return error_response(
            message=f"Error creating course: {str(e)}",
            status_code=500
        )
    
    except Exception as e:
        return error_response(
            message=f"Error creating course: {str(e)}",
            status_code=500
        )


def update_course(course_id: str, course_data: CourseUpdate) -> Dict:
    """
    Update existing course (deadlines updated separately)
    
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
            # deadline_date=None,  # Not updated here
            link=course_data.link
        )
        
        if not success:
            return error_response(
                message="Failed to update course",
                status_code=500
            )
        
        # Retrieve updated course
        updated_course = courses_model.get_course_by_id(course_id)
        # deadlines = deadline_model.get_deadlines_by_task(course_id, 'Course')
        # updated_course['deadlines'] = deadlines
        
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
    Delete course (and all its deadlines)
    
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
        
        # Delete all deadlines for this course
        # deadline_model.delete_all_deadlines_for_task(course_id, 'Course')
        
        # Delete course
        success, message = courses_model.delete_course(course_id)
        
        if not success:
            return error_response(
                message=message,
                status_code=500
            )
        
        return success_response(
            data={"courses_id": course_id},
            message="Course and all deadlines deleted successfully",
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
        
        # Get deadlines
        # deadlines = deadline_model.get_deadlines_by_task(course_id, 'Course')
        # course['deadlines'] = deadlines
        
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

def get_course_count(include_stats: bool = False) -> Dict:
    """
    Get total course count
    
    Args:
        include_stats: (Future use) Include additional statistics
    
    Returns:
        JSON response with total course count
    """
    try:
        # Fetch course count from model
        courses = courses_model.get_course_count()  # returns list of dicts
        
        if not courses:
            return error_response(
                message="Failed to retrieve course count",
                status_code=500
            )
        
        # Extract the actual count value (since fetchall() returns a list)
        total_courses = courses[0]["total_courses"]

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
