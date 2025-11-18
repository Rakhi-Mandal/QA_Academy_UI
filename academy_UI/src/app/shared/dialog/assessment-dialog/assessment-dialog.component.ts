import { Component } from '@angular/core';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AdminDashboardService } from '../../services/admin-dashboard.service';

@Component({
  selector: 'app-assessment-dialog',
  imports: [CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,],
  templateUrl: './assessment-dialog.component.html',
  styleUrl: './assessment-dialog.component.css'
})
export class AssessmentDialogComponent {
  assessmentForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<AssessmentDialogComponent>,
    private dashboardService: AdminDashboardService
  ) {
    this.assessmentForm = this.fb.group({
      assessment_id: ['', Validators.required],
      link: ['', [Validators.required]],
      name: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.assessmentForm.valid) {
      const newAssessment = this.assessmentForm.value;
      console.log(newAssessment);


      this.dashboardService.createAssessment(newAssessment).subscribe({
        next: (response: any) => {
          console.log('✅ Assessment created successfully:', response);
          alert(`Assessment "${newAssessment.name}" created successfully!`);
        },
        error: (err: any) => {
          console.error('❌ Error creating assessment:', err);
          alert(`Failed to create assessment: ${err.message}`);
        }
      });

    }
  }
}