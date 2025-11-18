"""
QE Academy Backend API
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import assessment
from routes import batch
from routes import pod
from routes import courses
from routes import course_record
from routes import employee
from routes import user_routes
from dotenv import load_dotenv
from routes import dashboard
from routes import certification
from routes import certification_record
from fastapi import APIRouter
import os
from config import settings
from routes import assessment_record


# Create uploads directories if they don't exist
os.makedirs("uploads/assessments", exist_ok=True)
os.makedirs("uploads/certifications", exist_ok=True)

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="QE Academy API",
    description="Backend API for QE Academy Employee Training Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads folder for file serving
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Import and register routers
# from routes import batch, employee, assessment, certification, assessment_record, certification_record, file
# app.include_router(batch.router, prefix="/api/batches", tags=["Batches"])
# app.include_router(employee.router, prefix="/api/employees", tags=["Employees"])
# app.include_router(assessment.router, prefix="/api/assessments", tags=["Assessments"])
# app.include_router(certification.router, prefix="/api/certifications", tags=["Certifications"])
# app.include_router(assessment_record.router, prefix="/api/assessment-records", tags=["Assessment Records"])
# app.include_router(certification_record.router, prefix="/api/certification-records", tags=["Certification Records"])
# app.include_router(file.router, prefix="/api/files", tags=["Files"])

@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information"""
    return {
        "message": "QE Academy Backend API",
        "status": "Running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Register Assessment Routes
app.include_router(
    assessment.router,
    prefix="/api/assessments",
    tags=["Assessments"]
)

app.include_router(
    assessment_record.router,
    prefix="/api/assessment-records",
    tags=["Assessment Records"]
)

app.include_router(
    employee.router,
    prefix="/api/employees",
    tags=["Employees"]
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

app.include_router(batch.router, prefix="/api/batches")
 
app.include_router(pod.router, prefix="/api/pods", tags=["PODs"])

# Register User Routes
app.include_router(
    user_routes.router,
    prefix="/api/users",
    tags=["Users"]
)

# Register Course Routes
app.include_router(
    courses.router,
    prefix="/api/courses",
    tags=["Courses"]
)

# Register Course Record Routes
app.include_router(
    course_record.router,
    prefix="/api/course-records",
    tags=["Course Records"]
)

app.include_router(
    employee.router, 
    prefix="/api/employee", 
    tags=["Employee"]
)
# Register Certification Routes
app.include_router(
    certification.router,
    prefix="/api/certifications",
    tags=["Certifications"]
)
 
# Register Certification Record Routes
app.include_router(
    certification_record.router,
    prefix="/api/certification-records",
    tags=["Certification Records"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development
    )