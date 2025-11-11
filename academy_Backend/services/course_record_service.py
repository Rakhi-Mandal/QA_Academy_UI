"""
Course Record Service - Business logic
"""
import os
from typing import Dict
from fastapi import UploadFile
from models import course_record as record_model
from models import courses as courses_model
from schemas.course_record import CourseRecordCreate, CourseRecordUpdate
from utils.response import success_response, error_response
from utils.validators import validate_file_extension, sanitize_filename
from config import settings


def get_all_course_records() -> Dict:
    """
    Get all course records
    
    Returns:
        JSON response with course record list
    """
    try:
        records = record_model.get_all_course_records()
        
        if records is None:
            return error_response(
                message="Failed to retrieve course records",
                status_code=500
            )
        
        return success_response(
            data=records,
            message=f"Retrieved {len(records)} course record(s) successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=f"Error retrieving course records: {str(e)}",
            status_code=500
        )


def get_record_by_id(record_id: int) -> Dict:
    """
    Get course record by ID
    
    Args:
        record_id: Record ID
        
    Returns:
        JSON response with course record data
    """
    try:
        # Check if record exists
        if not record_model.record_exists(record_id):
            return error_response(
                message=f"Course record with ID '{record_id}' not found",
                status_code=404
            )
        
        # Get record
        record = record_model.get_record_by_id(record_id)
        
        if not record:
            return error_response(
                message="Failed to retrieve course record",
                status_code=500
            )
        
        return success_response(
            data=record,
            message="Course record retrieved successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error retrieving course record: {str(e)}",
            status_code=500
        )


def get_records_by_employee(employee_id: str) -> Dict:
    """
    Get all course records for an employee
    
    Args:
        employee_id: Employee ID
        
    Returns:
        JSON response with employee's course records
    """
    try:
        records = record_model.get_records_by_employee(employee_id)
        
        if records is None:
            return error_response(
                message="Failed to retrieve course records",
                status_code=500
            )
        
        return success_response(
            data=records,
            message=f"Retrieved {len(records)} course record(s) for employee {employee_id}",
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=f"Error retrieving employee course records: {str(e)}",
            status_code=500
        )


def get_records_by_course(course_id: str) -> Dict:
    """
    Get all records for a specific course
    
    Args:
        course_id: Course ID
        
    Returns:
        JSON response with course records
    """
    try:
        # Check if course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        records = record_model.get_records_by_course(course_id)
        
        if records is None:
            return error_response(
                message="Failed to retrieve course records",
                status_code=500
            )
        
        return success_response(
            data=records,
            message=f"Retrieved {len(records)} record(s) for course {course_id}",
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=f"Error retrieving course records: {str(e)}",
            status_code=500
        )


def create_record(record_data: CourseRecordCreate) -> Dict:
    """
    Create new course record
    
    Args:
        record_data: Course record creation data
        
    Returns:
        JSON response with created record
    """
    try:
        # Validate course exists
        if not courses_model.course_exists(record_data.course_id):
            return error_response(
                message=f"Course with ID '{record_data.course_id}' not found",
                status_code=404
            )
        
        # Check if employee already completed this course
        if record_model.employee_completed_course(record_data.employee_id, record_data.course_id):
            return error_response(
                message="Employee has already completed this course",
                status_code=409
            )
        
        # Create record
        record_id = record_model.create_record(
            record_data.course_id,
            record_data.employee_id,
            record_data.completion_datetime.isoformat(),
            None  # No document initially
        )
        
        if not record_id:
            return error_response(
                message="Failed to create course record",
                status_code=500
            )
        
        # Retrieve created record
        created_record = record_model.get_record_by_id(record_id)
        
        return success_response(
            data=created_record,
            message="Course record created successfully",
            status_code=201
        )
    
    except Exception as e:
        return error_response(
            message=f"Error creating course record: {str(e)}",
            status_code=500
        )


def create_record_with_file(
    file: UploadFile,
    course_id: str,
    employee_id: str,
    completion_datetime: str
) -> Dict:
    """
    Create course record with file upload
    
    Args:
        file: Uploaded file
        course_id: Course ID
        employee_id: Employee ID
        completion_datetime: Completion datetime (ISO format string)
        
    Returns:
        JSON response with created record
    """
    try:
        # Validate course exists
        if not courses_model.course_exists(course_id):
            return error_response(
                message=f"Course with ID '{course_id}' not found",
                status_code=404
            )
        
        # Check if employee already completed this course
        if record_model.employee_completed_course(employee_id, course_id):
            return error_response(
                message="Employee has already completed this course",
                status_code=409
            )
        
        # Validate file extension
        if not validate_file_extension(file.filename, settings.ALLOWED_EXTENSIONS):
            return error_response(
                message="Invalid file type. Allowed types: PDF, JPG, JPEG, PNG",
                status_code=400
            )
        
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.MAX_FILE_SIZE:
            return error_response(
                message=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE / (1024*1024)}MB",
                status_code=400
            )
        
        # Generate filename
        sanitized_filename = sanitize_filename(file.filename)
        filename = f"{employee_id}_Course_{course_id}_{sanitized_filename}"
        
        # Save file
        upload_folder = os.path.join(settings.UPLOAD_FOLDER, "courses")
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Create record with document
        record_id = record_model.create_record(
            course_id,
            employee_id,
            completion_datetime,
            filename
        )
        
        if not record_id:
            # Delete uploaded file if record creation fails
            if os.path.exists(file_path):
                os.remove(file_path)
            return error_response(
                message="Failed to create course record",
                status_code=500
            )
        
        # Retrieve created record
        created_record = record_model.get_record_by_id(record_id)
        
        return success_response(
            data=created_record,
            message="Course record created with document successfully",
            status_code=201
        )
    
    except Exception as e:
        return error_response(
            message=f"Error creating course record with file: {str(e)}",
            status_code=500
        )


def update_record(record_id: int, record_data: CourseRecordUpdate) -> Dict:
    """
    Update course record
    
    Args:
        record_id: Record ID
        record_data: Updated record data
        
    Returns:
        JSON response with updated record
    """
    try:
        # Check if record exists
        if not record_model.record_exists(record_id):
            return error_response(
                message=f"Course record with ID '{record_id}' not found",
                status_code=404
            )
        
        # Update record if completion_datetime is provided
        if record_data.completion_datetime:
            success = record_model.update_record(
                record_id,
                record_data.completion_datetime.isoformat()
            )
            
            if not success:
                return error_response(
                    message="Failed to update course record",
                    status_code=500
                )
        
        # Retrieve updated record
        updated_record = record_model.get_record_by_id(record_id)
        
        return success_response(
            data=updated_record,
            message="Course record updated successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error updating course record: {str(e)}",
            status_code=500
        )


def delete_record(record_id: int) -> Dict:
    """
    Delete course record (and associated file if exists)
    
    Args:
        record_id: Record ID
        
    Returns:
        JSON response confirming deletion
    """
    try:
        # Check if record exists
        if not record_model.record_exists(record_id):
            return error_response(
                message=f"Course record with ID '{record_id}' not found",
                status_code=404
            )
        
        # Delete record (returns document name)
        success, document = record_model.delete_record(record_id)
        
        if not success:
            return error_response(
                message=document,  # Contains error message
                status_code=500
            )
        
        # Delete associated file if exists
        if document:
            file_path = os.path.join(settings.UPLOAD_FOLDER, "courses", document)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"✅ Deleted file: {file_path}")
                except Exception as e:
                    print(f"⚠️ Warning: Could not delete file {file_path}: {e}")
        
        return success_response(
            data={"record_id": record_id},
            message="Course record deleted successfully",
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=f"Error deleting course record: {str(e)}",
            status_code=500
        )


def get_document_download_path(record_id: int) -> tuple:
    """
    Get document download path for a course record
    
    Args:
        record_id: Record ID
        
    Returns:
        Tuple of (file_path, error_response) - one will be None
    """
    try:
        # Check if record exists
        if not record_model.record_exists(record_id):
            return None, error_response(
                message=f"Course record with ID '{record_id}' not found",
                status_code=404
            )
        
        # Get document filename
        document = record_model.get_document_path(record_id)
        
        if not document:
            return None, error_response(
                message="No document found for this record",
                status_code=404
            )
        
        # Build file path
        file_path = os.path.join(settings.UPLOAD_FOLDER, "courses", document)
        
        if not os.path.exists(file_path):
            return None, error_response(
                message="Document file not found on server",
                status_code=404
            )
        
        return file_path, None
    
    except Exception as e:
        return None, error_response(
            message=f"Error retrieving document: {str(e)}",
            status_code=500
        )