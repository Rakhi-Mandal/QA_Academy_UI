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

@Component({
  selector: 'app-mastery-program',
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
  templateUrl: './mastery-program.component.html',
  styleUrl: './mastery-program.component.scss'
})
export class MasteryProgramComponent implements OnInit, AfterViewInit {

  displayedColumns = ['slNo', 'employeeId', 'name', 'email', 'designation', 'assessment', 'certification', 'action'];
  dataSource = new MatTableDataSource<any>([]);
  allEmployees: any[] = [];
  designations: string[] = [];
  isLoading = false;
  
  constructor(
    public dialog: MatDialog,
    private employeeService: EmployeeService,
    private snackBar: MatSnackBar
  ) {}

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  selectedBatch = 3; // Default batch
  selectedDesignation = 'All';
  selectedAssessment = 'All';
  selectedCertification = 'All';

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

          // Reset paginator to first page after loading new data
          if (this.paginator) {
            this.paginator.firstPage();
          }

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

  /** 🔄 Refresh Data */
  refreshData() {
    this.selectedDesignation = 'All';
    this.selectedAssessment = 'All';
    this.selectedCertification = 'All';
    this.loadAllData();
    if (this.paginator) this.paginator.firstPage();
  }

  /** 🔍 Apply Filters */
  applyFilters() {
    const filteredData = this.allEmployees.filter(emp => {
      const designationMatch = this.selectedDesignation === 'All' || emp.designation === this.selectedDesignation;
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

      return designationMatch && assessmentMatch && certificationMatch;
    });

    this.dataSource.data = filteredData;
    if (this.paginator) this.paginator.firstPage();
  }

  /** 🔄 Change batch dynamically */
  onBatchChange(batchCode: number) {
    this.selectedBatch = batchCode;
    this.loadAllData();
  }

  // Helper method to calculate serial number for display
  getSerialNumber(index: number): number {
    if (this.paginator) {
      return (this.paginator.pageIndex * this.paginator.pageSize) + index + 1;
    }
    return index + 1;
  }

  /** ➕ Add Employee Dialog */
  openAddDialog() {
    const dialogRef = this.dialog.open(AddEmployeeDialogComponent, {
      width: '70%',
      height: '60%',
      panelClass: 'custom-dialog-container',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.allEmployees = [...this.allEmployees, result];
        this.applyFilters();
      }
    });
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

