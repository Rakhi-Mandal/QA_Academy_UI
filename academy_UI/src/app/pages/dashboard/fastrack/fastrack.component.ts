import { Component, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AddEmployeeDialogComponent } from '../../add-employee-dialog/add-employee-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { EmployeeDetailsDialogComponent } from '../../employee-details-dialog/employee-details-dialog.component';
@Component({
  selector: 'app-fastrack',
  standalone: true,
  templateUrl: './fastrack.component.html',
  styleUrls: ['./fastrack.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatCardModule,
    MatProgressBarModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatPaginatorModule,
    MatSelectModule,
    MatTooltipModule
  ]
})
export class FastrackComponent implements OnInit, AfterViewInit {

  displayedColumns = ['slNo', 'employeeId', 'name', 'email', 'designation', 'assessment', 'certification', 'action'];
  dataSource = new MatTableDataSource<any>([]);
  designations: string[] = [];
  
  constructor(public dialog: MatDialog) {}

  @ViewChild(MatPaginator) paginator!: MatPaginator;

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
    const employees = [
      { employeeId: 'FS001', name: 'Aarav Mehta', email: 'aarav.mehta@company.com', designation: 'QA Engineer', assessment: 85, certification: 90 },
  { employeeId: 'FS002', name: 'Diya Nair', email: 'diya.nair@company.com', designation: 'Automation Engineer', assessment: 78, certification: 82 },
  { employeeId: 'FS003', name: 'Kabir Singh', email: 'kabir.singh@company.com', designation: 'Test Lead', assessment: 92, certification: 88 },
  { employeeId: 'FS004', name: 'Meera Kapoor', email: 'meera.kapoor@company.com', designation: 'QA Analyst', assessment: 67, certification: 60 },
  { employeeId: 'FS005', name: 'Rohan Patel', email: 'rohan.patel@company.com', designation: 'Automation Architect', assessment: 95, certification: 98 },
  { employeeId: 'E005', name: 'Ethan', email: 'ethan@xyz.com', designation: 'Developer', assessment: 40, certification: 60 },
  { employeeId: 'E006', name: 'Fiona', email: 'fiona@xyz.com', designation: 'Manager', assessment: 88, certification: 85 },
  { employeeId: 'E007', name: 'George', email: 'george@xyz.com', designation: 'QA', assessment: 55, certification: 50 },
  { employeeId: 'E008', name: 'Hannah', email: 'hannah@xyz.com', designation: 'Developer', assessment: 65, certification: 75 },
  { employeeId: 'E009', name: 'Ian', email: 'ian@xyz.com', designation: 'QA', assessment: 35, certification: 45 },
  { employeeId: 'E010', name: 'Jasmine', email: 'jasmine@xyz.com', designation: 'Manager', assessment: 95, certification: 92 }
 ];

    this.dataSource.data = employees;
    this.designations = [ ...new Set(employees.map(e => e.designation))];
  }

  applyFilters() {
    const data = this.dataSource.data.filter(emp => {
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

    this.dataSource.data = data;
    this.dataSource.paginator = this.paginator;
  }

  refreshData() {
    this.loadAllData();
    this.dataSource.paginator = this.paginator;
    this.applyFilters()
  }

   openAddDialog() {
    const dialogRef = this.dialog.open(AddEmployeeDialogComponent, {
      width: '70%',
      height: '60%',
      panelClass: 'custom-dialog-container',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.dataSource.data = [...this.dataSource.data, result];
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
