"""
Application Constants
"""

# File Upload Constants
ALLOWED_FILE_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Upload Folders
ASSESSMENT_UPLOAD_FOLDER = "uploads/assessments"
CERTIFICATION_UPLOAD_FOLDER = "uploads/certifications"

# Response Messages
MSG_SUCCESS = "Operation completed successfully"
MSG_CREATED = "Resource created successfully"
MSG_UPDATED = "Resource updated successfully"
MSG_DELETED = "Resource deleted successfully"
MSG_NOT_FOUND = "Resource not found"
MSG_ALREADY_EXISTS = "Resource already exists"
MSG_INVALID_INPUT = "Invalid input data"
MSG_DB_ERROR = "Database error occurred"
MSG_FILE_TOO_LARGE = f"File size exceeds {MAX_FILE_SIZE_MB}MB limit"
MSG_INVALID_FILE_TYPE = "Invalid file type. Allowed types: PDF, JPG, JPEG, PNG"