import { Component, Inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { CalendarItem, FileAttachment } from '../../models/calendar.models';

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
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatIconModule
  ],
  templateUrl: './form-submission-dialog.component.html',
  styleUrls: ['./form-submission-dialog.component.scss']
})
export class FormSubmissionDialogComponent {

  // FIX 1: Add missing form group
  submissionForm: FormGroup = new FormGroup({
    score: new FormControl(null, [Validators.required, Validators.min(0)]),
    submissionNotes: new FormControl('')
  });

  // FIX 2: Add missing uploadedFiles array
  uploadedFiles: FileAttachment[] = [];

  constructor(
    public dialogRef: MatDialogRef<FormSubmissionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { item: CalendarItem },
    private cdr: ChangeDetectorRef
  ) {}

  // ---- File Upload Logic ----
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      const reader = new FileReader();
      reader.onload = (e) => {
        const attachment: FileAttachment = {
          id: `file_${Date.now()}`,
          name: file.name,
          size: file.size,
          type: file.type,
          mimeType: file.type,
          data: e.target?.result as string,
          url: '',
          uploadedAt: new Date(),
          file: file
        };

        this.uploadedFiles.push(attachment);
        this.cdr.markForCheck();
      };

      reader.readAsDataURL(file);
      input.value = '';
    }
  }

  removeFile(index: number): void {
    this.uploadedFiles.splice(index, 1);
    this.cdr.markForCheck();
  }

  // ---- Dialog Actions ----
  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    const result: SubmissionResult = {
      score: this.submissionForm.get('score')?.value,
      submissionNotes: this.submissionForm.get('submissionNotes')?.value || null,
      attachments: this.uploadedFiles
    };

    this.dialogRef.close(result);
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }
}
 