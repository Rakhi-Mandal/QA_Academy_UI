import { Component, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AddEmployeeDialogComponent } from '../../add-employee-dialog/add-employee-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { EmployeeDetailsDialogComponent } from '../../employee-details-dialog/employee-details-dialog.component';
import { EmployeeService, Employee } from '../../../shared/services/employee.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-advanced-track',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatTableModule,
    MatCardModule,
    MatProgressBarModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatPaginatorModule,
    MatSelectModule,
    MatTooltipModule,
    MatSnackBarModule
  ],
  templateUrl: './advanced-track.component.html',
  styleUrl: './advanced-track.component.scss'
})
export class AdvancedTrackComponent implements OnInit, AfterViewInit {
  
  displayedColumns = [
    'slNo',
    'employeeId',
    'name',
    'email',
    'designation',
    'assessment_progress',
    'certification_progress',
    'course_progress',
    'action'
  ];

  dataSource = new MatTableDataSource<any>([]);
  allEmployees: any[] = [];
  designations: string[] = [];
  isLoading = false;
  selectedPod = 'All';
pods: string[] = [];


  selectedBatch = 2; // Default batch
  selectedDesignation = 'All';
  selectedAssessment = 'All';
  selectedCertification = 'All';

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    public dialog: MatDialog,
    private employeeService: EmployeeService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.loadAllData();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  loadAllData() {
    this.isLoading = true;

    this.employeeService.getEmployeesByBatch(this.selectedBatch).subscribe({
      next: (response) => {
        console.log('API Response:', response);

        if (response.success && response.data) {
          const employees = response.data.map(emp => ({
            employeeId: emp.Employee_ID,
            name: emp.Employee_Name,
            email: emp.Employee_Email,
            designation: emp.Designation,
            pod: emp.POD,
            batchCode: emp.Batch_Code,
            assessment_progress: emp.assessment_completion_percent || 0,
            certification_progress: emp.certification_completion_percent || 0,
            course_progress: emp.course_completion_percent || 0
          }));

          this.allEmployees = [...employees];
          this.dataSource.data = [...employees];
          this.designations = [...new Set(employees.map(e => e.designation))];
          this.pods = [...new Set(employees.map(e => e.pod))];


          this.snackBar.open('Employees loaded successfully', 'Close', {
            duration: 3000,
            horizontalPosition: 'end',
            verticalPosition: 'top'
          });
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading employees:', error);
        this.snackBar.open('Error loading employees', 'Close', {
          duration: 3000,
          horizontalPosition: 'end',
          verticalPosition: 'top'
        });
        this.isLoading = false;
      }
    });
  }

  refreshData() {
    this.selectedDesignation = 'All';
    this.selectedAssessment = 'All';
    this.selectedCertification = 'All';
    this.loadAllData();
    if (this.paginator) this.paginator.firstPage();
  }

  applyFilters() {
    const filteredData = this.allEmployees.filter(emp => {
  const designationMatch = this.selectedDesignation === 'All' || emp.designation === this.selectedDesignation;
  const podMatch = this.selectedPod === 'All' || emp.pod === this.selectedPod;
  
  const assessmentMatch =
    this.selectedAssessment === 'All' ||
    (this.selectedAssessment === 'Below 50%' && emp.assessment_progress < 50) ||
    (this.selectedAssessment === '50%-80%' && emp.assessment_progress >= 50 && emp.assessment_progress <= 80) ||
    (this.selectedAssessment === 'Above 80%' && emp.assessment_progress > 80);

  const certificationMatch =
    this.selectedCertification === 'All' ||
    (this.selectedCertification === 'Below 50%' && emp.certification_progress < 50) ||
    (this.selectedCertification === '50%-80%' && emp.certification_progress >= 50 && emp.certification_progress <= 80) ||
    (this.selectedCertification === 'Above 80%' && emp.certification_progress > 80);

  return designationMatch && podMatch && assessmentMatch && certificationMatch;
});


    this.dataSource.data = filteredData;
    if (this.paginator) this.paginator.firstPage();
  }

  onBatchChange(batchCode: number) {
    this.selectedBatch = batchCode;
    this.loadAllData();
  }

  openEmployeeDetails(employee: any): void {
    this.dialog.open(EmployeeDetailsDialogComponent, {
      width: '90%',
      height: '70%',
      data: employee,
      panelClass: 'custom-dialog-container'
    });
  }
}
