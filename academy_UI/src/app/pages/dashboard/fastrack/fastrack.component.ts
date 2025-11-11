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
  selector: 'app-fastrack',
  standalone: true,
  templateUrl: './fastrack.component.html',
  styleUrls: ['./fastrack.component.scss'],
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
  ]
})
export class FastrackComponent implements OnInit, AfterViewInit {

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

  selectedBatch = 1; // Default batch
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
    
    // Replace with your actual batch code
    this.employeeService.getEmployeesByBatch(this.selectedBatch).subscribe({
      next: (response) => {
        console.log('API Response:', response);
        
        if (response.success && response.data) {
          // Map API response to match your table structure
          const employees = response.data.map(emp => ({
            employeeId: emp.Employee_ID,
            name: emp.Employee_Name,
            email: emp.Employee_Email,
            designation: emp.Designation,
            podId: emp.POD_ID,
            pod: emp.POD,
            batchCode: emp.Batch_Code,
            assessment: emp.assessment || 0, // Default to 0 if not available
            certification: emp.certification || 0 // Default to 0 if not available
          }));

          this.allEmployees = [...employees];
          this.dataSource.data = [...employees];
          this.designations = [...new Set(employees.map(e => e.designation))];
          
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

  // Method to change batch dynamically
  onBatchChange(batchCode: number) {
    this.selectedBatch = batchCode;
    this.loadAllData();
  }

  applyFilters() {
    const filteredData = this.allEmployees.filter(emp => {
      const designationMatch = this.selectedDesignation === 'All' || emp.designation === this.selectedDesignation;
      const assessmentMatch =
        this.selectedAssessment === 'All' ||
        (this.selectedAssessment === 'Below 50%' && emp.assessment < 50) ||
        (this.selectedAssessment === '50%-80%' && emp.assessment >= 50 && emp.assessment <= 80) ||
        (this.selectedAssessment === 'Above 80%' && emp.assessment > 80);
      const certificationMatch =
        this.selectedCertification === 'All' ||
        (this.selectedCertification === 'Below 50%' && emp.certification < 50) ||
        (this.selectedCertification === '50%-80%' && emp.certification >= 50 && emp.certification <= 80) ||
        (this.selectedCertification === 'Above 80%' && emp.certification > 80);

      return designationMatch && assessmentMatch && certificationMatch;
    });

    this.dataSource.data = filteredData;
    
    if (this.paginator) {
      this.paginator.firstPage();
    }
  }

  refreshData() {
    this.selectedDesignation = 'All';
    this.selectedAssessment = 'All';
    this.selectedCertification = 'All';
    this.loadAllData();
    if (this.paginator) {
      this.paginator.firstPage();
    }
  }

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
