import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Employee {
  Employee_ID: string;
  Employee_Name: string;
  Employee_Email: string;
  Designation: string;
  POD_ID: number;
  POD: string;
  Batch_Code: number;
  assessment?: number;
  course_completion_percent ?: number;
  certification_completion_percent ?: number;
  assessment_completion_percent ?: number;
}

export interface EmployeeResponse {
  success: boolean;
  message: string;
  data: Employee[];
}

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  getEmployeesByBatch(batchCode: number): Observable<EmployeeResponse> {
    return this.http.get<EmployeeResponse>(`${this.apiUrl}/employees/batch/${batchCode}`);
  }

  getAllEmployees(): Observable<EmployeeResponse> {
    return this.http.get<EmployeeResponse>(`${this.apiUrl}/employees/get-all`);
  }

  getEmployeeById(employeeId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/employees/${employeeId}`);
  }
}