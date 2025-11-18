import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AdminDashboardService } from '../../services/admin-dashboard.service';

@Component({
  selector: 'app-pod-dialog',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './pod-dialog.component.html',
  styleUrl: './pod-dialog.component.css'
})
export class PodDialogComponent {
  podForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<PodDialogComponent>,
    private dashboardService: AdminDashboardService
  ) {
    this.podForm = this.fb.group({
      pod_id: ['', Validators.required],
      pod: ['', Validators.required],
      batch_code: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.podForm.valid) {
      const newPod = this.podForm.value;
      console.log('📤 Sending POD data:', newPod);

      this.dashboardService.createPod(newPod).subscribe({
        next: (response) => {
          console.log('✅ POD created successfully:', response);
          alert(`POD "${newPod.pod}" created successfully!`);
          this.dialogRef.close(response);
        },
        error: (err) => {
          console.error('❌ Error creating POD:', err);
          alert(`Failed to create POD: ${err.message}`);
        }
      });
    }
  }
}
