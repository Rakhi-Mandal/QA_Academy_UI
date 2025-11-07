import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CalendarItem, FileAttachment } from '../../models/calendar.models';

export interface DialogData {
  item: CalendarItem;
}

export interface SubmissionResult {
  score: number | null;
  attachments: FileAttachment[];
  submissionNotes: string | null;
}

@Component({
  selector: 'app-form-submission-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './form-submission-dialog.component.html',
  styleUrls: ['./form-submission-dialog.component.scss']
})
export class FormSubmissionDialogComponent {
  submissionForm: FormGroup;
  uploadedFiles: FileAttachment[] = [];
  maxFileSize = 5 * 1024 * 1024;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<FormSubmissionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {
    this.submissionForm = this.fb.group({
      score: [null, [Validators.min(0), Validators.max(100)]],
      submissionNotes: ['']
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      if (file.size > this.maxFileSize) {
        alert('File size exceeds 5MB limit');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        const fileAttachment: FileAttachment = {
          name: file.name,
          size: file.size,
          mimeType: file.type,
          data: e.target?.result as string,
          uploadedAt: new Date()
        };
        this.uploadedFiles.push(fileAttachment);
      };
      reader.readAsDataURL(file);
    }
  }

  removeFile(index: number): void {
    this.uploadedFiles.splice(index, 1);
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.submissionForm.valid) {
      const result: SubmissionResult = {
        score: this.submissionForm.value.score,
        attachments: this.uploadedFiles,
        submissionNotes: this.submissionForm.value.submissionNotes
      };
      this.dialogRef.close(result);
    }
  }
}
