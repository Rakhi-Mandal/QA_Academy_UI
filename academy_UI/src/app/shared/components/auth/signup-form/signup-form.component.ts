import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { LabelComponent } from '../../form/label/label.component';
import { CheckboxComponent } from '../../form/input/checkbox.component';
import { InputFieldComponent } from '../../form/input/input-field.component';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';


@Component({
  selector: 'app-signup-form',
  imports: [
    CommonModule,
    LabelComponent,
    CheckboxComponent,
    InputFieldComponent,
    RouterModule,
    FormsModule,
  ],
  templateUrl: './signup-form.component.html',
  styles: ``
})
export class SignupFormComponent {

  showPassword = false;
  isChecked = false;

  fname = '';
  email = '';
  password = '';
  role: 'admin' | 'employee' = 'employee';
  employeeId = '';
  designation = '';
  podId: number = 1;
  
  errorMessage = '';
  isLoading = false;

  constructor(private authService: AuthService) {}

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSignUp() {
    if (!this.fname || !this.email || !this.password) {
      this.errorMessage = 'Please fill in all required fields';
      return;
    }

    if (this.role === 'employee' && (!this.employeeId?.trim() || !this.designation?.trim())) {
      this.errorMessage = 'Please fill in all employee fields (Employee ID and Designation are required)';
      return;
    }

    if (!this.isChecked) {
      this.errorMessage = 'Please agree to the Terms and Conditions';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const nameParts = this.fname.trim().split(' ');
    const firstName = nameParts[0] || this.fname;
    const lastName = nameParts.slice(1).join(' ') || '';

    const signupData = {
      firstName: firstName,
      lastName: lastName,
      email: this.email.trim(),
      password: this.password,
      role: this.role,
      employeeId: this.employeeId?.trim() || undefined,
      designation: this.designation?.trim() || undefined,
      podId: this.podId
    };

    console.log('Signup data being sent:', signupData);

    this.authService.signup(signupData).subscribe({
      next: (success) => {
        this.isLoading = false;
        // Router navigation is handled by AuthService
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.message || 'Sign up failed. Please try again.';
      }
    });
  }
}
