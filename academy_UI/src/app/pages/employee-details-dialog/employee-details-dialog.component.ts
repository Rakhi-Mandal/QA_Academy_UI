import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { NgIf, NgFor, DatePipe } from '@angular/common';
interface Assessment {
  name: string;
  score: number;
}

interface Certification {
  name: string;
  completion: number;
}

interface EmployeeDetail {
  employeeId: string;
  name: string;
  email: string;
  designation: string;
  assessmentProgress: number;
  certificationProgress: number;
  assessments: Assessment[];
  certifications: Certification[];
  projects: string[];
  skills: string[];
  joiningDate: string;
  manager: string;
}

@Component({
  selector: 'app-employee-details-dialog',
  templateUrl: './employee-details-dialog.component.html',
  styleUrls: ['./employee-details-dialog.component.css'],
  imports: [MatIconModule, MatProgressBarModule, DatePipe, NgIf, NgFor],
   standalone: true,
})
export class EmployeeDetailsDialogComponent implements OnInit {
  employeeData!: EmployeeDetail | null;

  private dummyEmployees: EmployeeDetail[] = [
 {
    employeeId: 'FS001',
    name: 'Aarav Mehta',
    email: 'aarav.mehta@company.com',
    designation: 'QA Engineer',
    assessmentProgress: 85,
    certificationProgress: 90,
    assessments: [
      { name: 'Functional Testing', score: 88 },
      { name: 'Regression Testing', score: 80 },
      { name: 'API Automation', score: 86 }
    ],
    certifications: [
      { name: 'ISTQB Foundation', completion: 100 },
      { name: 'Postman API Expert', completion: 80 }
    ],
    projects: ['Customer Portal QA', 'Mobile App Regression'],
    skills: ['Selenium', 'Postman', 'Jira', 'TestRail'],
    joiningDate: '2021-04-18',
    manager: 'Priya Sharma'
  },
  {
    employeeId: 'FS002',
    name: 'Diya Nair',
    email: 'diya.nair@company.com',
    designation: 'Automation Engineer',
    assessmentProgress: 78,
    certificationProgress: 82,
    assessments: [
      { name: 'Playwright Fundamentals', score: 80 },
      { name: 'Web Automation', score: 75 },
      { name: 'CI/CD Integration', score: 78 }
    ],
    certifications: [
      { name: 'Certified Playwright Engineer', completion: 100 },
      { name: 'Azure DevOps Associate', completion: 65 }
    ],
    projects: ['E-Commerce Test Suite', 'DevOps Automation Setup'],
    skills: ['Playwright', 'TypeScript', 'GitHub Actions', 'Allure'],
    joiningDate: '2022-02-10',
    manager: 'Rajat Bansal'
  },
  {
    employeeId: 'FS003',
    name: 'Kabir Singh',
    email: 'kabir.singh@company.com',
    designation: 'Test Lead',
    assessmentProgress: 92,
    certificationProgress: 88,
    assessments: [
      { name: 'Leadership & Strategy', score: 95 },
      { name: 'Test Planning', score: 90 },
      { name: 'Risk-Based Testing', score: 92 }
    ],
    certifications: [
      { name: 'Agile Testing Professional', completion: 100 },
      { name: 'Certified Test Manager', completion: 80 }
    ],
    projects: ['Banking App QA', 'Automation Governance'],
    skills: ['Leadership', 'Test Strategy', 'Agile QA', 'Appium'],
    joiningDate: '2020-08-25',
    manager: 'Amit Verma'
  },
  {
    employeeId: 'FS004',
    name: 'Meera Kapoor',
    email: 'meera.kapoor@company.com',
    designation: 'QA Analyst',
    assessmentProgress: 67,
    certificationProgress: 60,
    assessments: [
      { name: 'Manual Testing Basics', score: 70 },
      { name: 'Defect Management', score: 60 },
      { name: 'Exploratory Testing', score: 65 }
    ],
    certifications: [
      { name: 'QA Fundamentals', completion: 50 },
      { name: 'Agile Beginner', completion: 70 }
    ],
    projects: ['Healthcare Portal', 'Internal QA Dashboard'],
    skills: ['Manual Testing', 'Confluence', 'Jira', 'Documentation'],
    joiningDate: '2023-06-14',
    manager: 'Nisha Tandon'
  },
  {
    employeeId: 'FS005',
    name: 'Rohan Patel',
    email: 'rohan.patel@company.com',
    designation: 'Automation Architect',
    assessmentProgress: 95,
    certificationProgress: 98,
    assessments: [
      { name: 'Framework Design', score: 96 },
      { name: 'Microservices Testing', score: 94 },
      { name: 'CI/CD Optimization', score: 95 }
    ],
    certifications: [
      { name: 'AWS Certified DevOps Engineer', completion: 100 },
      { name: 'Selenium Architect Expert', completion: 95 }
    ],
    projects: ['Enterprise Automation Platform', 'Cloud Integration Testing'],
    skills: ['Architecture', 'Docker', 'Kubernetes', 'Jenkins', 'Python'],
    joiningDate: '2019-01-22',
    manager: 'Vikram Singh'
  }
  ];

  constructor(
    public dialogRef: MatDialogRef<EmployeeDetailsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit(): void {
    this.fetchEmployeeDetails(this.data.employeeId);
  }

  fetchEmployeeDetails(empId: string): void {
    this.employeeData = this.dummyEmployees.find(e => e.employeeId === empId) || null;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
