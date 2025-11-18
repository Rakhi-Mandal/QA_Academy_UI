// src/app/shared/services/dashboard.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface DashboardStats {
  total_assignments: number;
  total_certifications: number;
  total_courses: number;
  completed_total: number;
  remaining_total: number;
}

export interface DeadlineItem {
  Task_Slno: number;
  Task_ID: string;
  Task_Type: 'Assessment' | 'Certification' | 'Course';
  title: string;
  link?: string;
  status: 'assigned' | 'completed';
  effective_deadline: string;
}

export interface CalendarEvent {
  id: number;
  title: string;
  type: 'Assessment' | 'Certification' | 'Course';
  start: string;
  status: 'assigned' | 'completed';
}

export interface SubmitTaskRequest {
  marks_scored?: number;
  notes?: string;
  file?: File;
}

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private baseUrl = '/api/dashboard';

  constructor(private http: HttpClient) {}

  /**
   * Get employee ID from localStorage
   * Tries multiple possible key names for flexibility
   */
  private getEmployeeId(): string | null {
    try {
      const raw = localStorage.getItem('currentUser');
      if (!raw) return null;
      const obj = JSON.parse(raw);
      return obj.employeeId || obj.employee_id || obj.Employee_ID || obj.id || null;
    } catch (error) {
      console.error('Error parsing currentUser from localStorage:', error);
      return null;
    }
  }

  /**
   * Get dashboard KPI statistics
   */
  getDashboard(employeeId?: string): Observable<{ success: boolean; data: DashboardStats }> {
    const empId = employeeId || this.getEmployeeId();
    if (!empId) {
      return throwError(() => new Error('Employee ID not found'));
    }

    const params = new HttpParams().set('employee_id', empId);
    return this.http.get<{ success: boolean; data: DashboardStats }>(
      `${this.baseUrl}/dashboard`,
      { params }
    ).pipe(
      catchError(error => {
        console.error('Error fetching dashboard:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get filtered items (all, Assessment, Certification, or Course)
   */
  getItems(
    filter: string = 'all',
    employeeId?: string
  ): Observable<{ success: boolean; total: number; data: DeadlineItem[] }> {
    const empId = employeeId || this.getEmployeeId();
    if (!empId) {
      return throwError(() => new Error('Employee ID not found'));
    }

    const params = new HttpParams()
      .set('employee_id', empId)
      .set('filter', filter);

    return this.http.get<{ success: boolean; total: number; data: DeadlineItem[] }>(
      `${this.baseUrl}/items`,
      { params }
    ).pipe(
      catchError(error => {
        console.error('Error fetching items:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get calendar events within a date range
   */
  getCalendar(
    fromDate?: string,
    toDate?: string,
    employeeId?: string
  ): Observable<{ success: boolean; data: CalendarEvent[] }> {
    const empId = employeeId || this.getEmployeeId();
    if (!empId) {
      return throwError(() => new Error('Employee ID not found'));
    }

    let params = new HttpParams().set('employee_id', empId);
    if (fromDate) params = params.set('from_date', fromDate);
    if (toDate) params = params.set('to_date', toDate);

    return this.http.get<{ success: boolean; data: CalendarEvent[] }>(
      `${this.baseUrl}/calendar`,
      { params }
    ).pipe(
      catchError(error => {
        console.error('Error fetching calendar:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get single item details by Task_Slno
   */
  getItem(taskSlno: number): Observable<{ success: boolean; data: DeadlineItem }> {
    return this.http.get<{ success: boolean; data: DeadlineItem }>(
      `${this.baseUrl}/item/${taskSlno}`
    ).pipe(
      catchError(error => {
        console.error(`Error fetching item ${taskSlno}:`, error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Submit a task with optional marks, notes, and file upload
   */
  submitTask(
    taskSlno: number,
    request: SubmitTaskRequest,
    employeeId?: string
  ): Observable<{ success: boolean; message: string }> {
    const empId = employeeId || this.getEmployeeId();
    if (!empId) {
      return throwError(() => new Error('Employee ID not found'));
    }

    const formData = new FormData();
    formData.append('employee_id', empId);
    
    if (request.marks_scored !== null && request.marks_scored !== undefined) {
      formData.append('marks_scored', String(request.marks_scored));
    }
    
    if (request.notes) {
      formData.append('notes', request.notes);
    }
    
    if (request.file) {
      formData.append('file', request.file, request.file.name);
    }

    return this.http.post<{ success: boolean; message: string }>(
      `${this.baseUrl}/submit/${taskSlno}`,
      formData
    ).pipe(
      catchError(error => {
        console.error(`Error submitting task ${taskSlno}:`, error);
        return throwError(() => error);
      })
    );
  }
}