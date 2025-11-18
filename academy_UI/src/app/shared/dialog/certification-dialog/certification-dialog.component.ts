import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AdminDashboardService } from '../../services/admin-dashboard.service';

@Component({
  selector: 'app-certification-dialog',
  imports: [  CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule],
  templateUrl: './certification-dialog.component.html',
  styleUrl: './certification-dialog.component.css'
})
export class CertificationDialogComponent {
 certificationForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CertificationDialogComponent>,
    private dashboardService: AdminDashboardService
  ) {
    this.certificationForm = this.fb.group({
      certification_id: ['', Validators.required],
      name: ['', Validators.required],
      link: ['', [Validators.required, Validators.pattern('https?://.+')]]
    });
  }

  onSubmit() {
    if (this.certificationForm.valid) {
      const newCertification = this.certificationForm.value;
      console.log('📤 Sending Certification data:', newCertification);

      this.dashboardService.createCertification(newCertification).subscribe({
        next: (response) => {
          console.log('✅ Certification created successfully:', response);
          alert(`Certification "${newCertification.name}" created successfully!`);
          this.dialogRef.close(response);
        },
        error: (err) => {
          console.error('❌ Error creating certification:', err);
          alert(`Failed to create certification: ${err.message}`);
        }
      });
    }
  }
}
