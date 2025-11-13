import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';

// ============= Interfaces =============

export interface RecentAssessment {
  Employee_Name: string;
  Assessment_Name: string;
  Upload_Time: string;
}

export interface RecentCourseCompletion {
  Course_Name: string;
  Employee_Name: string;
  Completion_Datetime: string;
}

export interface EmployeeCreate {
  user_id: string;
  pod_id: string;
  employee_name: string;
  employee_id: string;
  employee_email: string;
  designation: string;
}

export interface AssessmentCreate {
  assessment_id: string;
  name: string;
  link?: string;
}

export interface CertificationCreate {
  certification_id: string;
  name: string;
  link?: string;
}

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

// ============= Service =============

@Injectable({
  providedIn: 'root'
})
export class AdminDashboardService {
  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {
    console.log('🔧 AdminDashboardService initialized');
  }

  // ============= Recent Activities =============

  /**
   * Fetch recent assessment submissions
   * @param limit Number of records to fetch (default: 2)
   */
  getRecentAssessments(limit: number = 2): Observable<RecentAssessment[]> {
    const url = `${this.baseUrl}/assessment-records/recent?limit=${limit}`;
    console.log('🌐 Fetching recent assessments:', url);
    
    return this.http.get<ApiResponse<RecentAssessment[]>>(url).pipe(
      map(response => response.data),
      tap(data => console.log('📥 Recent assessments:', data)),
      catchError(this.handleError)
    );
  }

  /**
   * Fetch recent course completions
   * @param limit Number of records to fetch (default: 2)
   */
  getRecentCourseCompletions(limit: number = 2): Observable<RecentCourseCompletion[]> {
    const url = `${this.baseUrl}/coursess/recent-completions?limit=${limit}`;
    console.log('🌐 Fetching recent course completions:', url);
    
    return this.http.get<ApiResponse<RecentCourseCompletion[]>>(url).pipe(
      map(response => {
        console.log('📦 Raw API response:', response);
        return response.data;
      }),
      tap(data => console.log('📥 Recent course completions:', data)),
      catchError((error) => {
        console.error('❌ Course completions error:', error);
        console.error('Error status:', error.status);
        console.error('Error message:', error.message);
        console.error('Full error:', JSON.stringify(error, null, 2));
        return this.handleError(error);
      })
    );
  }

  // ============= Assessment Operations =============

  /**
   * Create a new assessment
   * @param assessmentData Assessment details
   */
  createAssessment(assessmentData: AssessmentCreate): Observable<any> {
    const url = `${this.baseUrl}/assessments/create-assessment`;
    console.log('🌐 Creating assessment:', url, assessmentData);
    
    return this.http.post<ApiResponse<any>>(url, assessmentData).pipe(
      tap(response => console.log('✅ Assessment created:', response)),
      catchError(this.handleError)
    );
  }

  // ============= Certification Operations =============

  /**
   * Create a new certification
   * @param certificationData Certification details
   */
  createCertification(certificationData: CertificationCreate): Observable<any> {
    const url = `${this.baseUrl}/certifications/create-certification`;
    console.log('🌐 Creating certification:', url, certificationData);
    
    return this.http.post<ApiResponse<any>>(url, certificationData).pipe(
      tap(response => console.log('✅ Certification created:', response)),
      catchError(this.handleError)
    );
  }

/**
 * Create a new POD
 * @param podData POD details
 */
createPod(podData: { pod_id: string; pod: string; batch_code: string }): Observable<any> {
  const url = `${this.baseUrl}/pods/create-pod`;
  console.log('🌐 Creating POD:', url, podData);

  return this.http.post<ApiResponse<any>>(url, podData).pipe(
    tap(response => console.log('✅ POD created successfully:', response)),
    catchError(this.handleError)
  );
}


/**
 * Fetch total employee count
 */
getEmployeeCount(): Observable<number> {
  const url = `${this.baseUrl}/employees/count`;
  console.log('🌐 Fetching employee count:', url);

  return this.http.get<ApiResponse<{ total_employees: number }>>(url).pipe(
    map(response => response.data?.total_employees ?? 0),
    tap(count => console.log('👥 Employee count:', count)),
    catchError(this.handleError)
  );
}

/**
 * Fetch total number of certifications
 */
getCertificationCount(): Observable<number> {
  const url = `${this.baseUrl}/certifications/count`;
  console.log('🌐 Fetching certification count:', url);

  return this.http.get<{ success: boolean; message: string; total: number }>(url).pipe(
    map(response => response.total ?? 0),
    tap(count => console.log('🏆 Certification count:', count)),
    catchError(this.handleError)
  );
}

getBatchCount(): Observable<number> {
  const url = `${this.baseUrl}/batches/count`;
  return this.http.get<{ success: boolean; message: string; total: number }>(url).pipe(
    map(response => response.total ?? 0),
    catchError(error => {
      console.error('❌ Error fetching batch count:', error);
      return of(0);
    })
  );
}


  // ============= Error Handling =============

  private handleError(error: HttpErrorResponse): Observable<never> {
    console.error('🚫 HTTP Error:', error);
    
    let errorMessage = 'An error occurred';
    
    if (error.status === 0) {
      errorMessage = 'Network error - please check if the backend is running';
    } else if (error.status === 404) {
      errorMessage = `Resource not found - URL: ${error.url}`;
    } else if (error.status === 409) {
      errorMessage = error.error?.message || 'Resource already exists';
    } else if (error.status === 500) {
      errorMessage = error.error?.message || 'Server error occurred';
    } else {
      errorMessage = error.error?.message || error.message;
    }
    
    return throwError(() => new Error(errorMessage));
  }
}