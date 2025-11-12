import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { NgIf, NgFor, DatePipe } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

interface Assessment {
  name: string;
  score: number;
}

interface Certification {
  name: string;
  completion: number;
}

interface Course {
  name: string;
}

interface EmployeeDetail {
  employeeId: string;
  name: string;
  email: string;
  designation: string;
  assessmentProgress: number;
  certificationProgress: number;
  coursesProgress: number;
  assessments: Assessment[];
  certifications: Certification[];
  courses: Course[];
  skills: string[];
  joiningDate: string;
  manager: string;
}

@Component({
  selector: 'app-employee-details-dialog',
  templateUrl: './employee-details-dialog.component.html',
  styleUrls: ['./employee-details-dialog.component.css'],
  standalone: true,
  imports: [
    MatIconModule,
    MatProgressBarModule,
    DatePipe,
    NgIf,
    NgFor,
    HttpClientModule,
    MatProgressSpinnerModule
  ],
})
export class EmployeeDetailsDialogComponent implements OnInit {
  employeeData!: EmployeeDetail | null;
  loading: boolean = false;

  constructor(
    private http: HttpClient,
    public dialogRef: MatDialogRef<EmployeeDetailsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit(): void {
    if (this.data && this.data.employeeId) {
      this.fetchEmployeeDetails(this.data.employeeId);
    }
  }

  fetchEmployeeDetails(empId: string): void {
    this.loading = true;
    const apiUrl = `http://localhost:8000/api/employee/${empId}/all`;

    this.http.get(apiUrl).subscribe({
      next: (response: any) => {
        this.loading = false;
        if (response.success && response.data) {
          const backendData = response.data;

          this.employeeData = {
            employeeId: empId,
            name: '', // Add if backend returns
            email: '',
            designation: '',
            assessmentProgress: this.calculateProgress(backendData.assessments),
            certificationProgress: this.calculateProgress(backendData.certifications),
            coursesProgress: 100, // or calculate if needed
            assessments: backendData.assessments.map((a: any) => ({
              name: a.Assessment_Name,
              score: a.Mark_Secured
            })),
            certifications: backendData.certifications.map((c: any) => ({
              name: c.Certification_Name,
              completion: c.Mark_Secured
            })),
            courses: backendData.courses.map((course: any) => ({
              name: course.Course_Name
            })),
            skills: [],
            joiningDate: '',
            manager: ''
          };
        } else {
          this.employeeData = null;
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Error fetching employee details:', err);
        this.employeeData = null;
      }
    });
  }

  calculateProgress(items: any[]): number {
    if (!items || items.length === 0) return 0;
    const total = items.reduce((sum, item) => sum + (item.Mark_Secured || 0), 0);
    return Math.round(total / items.length);
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
