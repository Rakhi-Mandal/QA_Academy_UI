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
  lname = '';
  email = '';
  password = '';
  role: 'admin' | 'employee' = 'employee';
  employeeId = '';
  department = '';
  designation = '';
  
  errorMessage = '';
  isLoading = false;

  constructor(private authService: AuthService) {}

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSignUp() {
    if (!this.fname || !this.lname || !this.email || !this.password) {
      this.errorMessage = 'Please fill in all required fields';
      return;
    }

    if (!this.isChecked) {
      this.errorMessage = 'Please agree to the Terms and Conditions';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.signup({
      firstName: this.fname,
      lastName: this.lname,
      email: this.email,
      password: this.password,
      role: this.role,
      employeeId: this.employeeId || undefined,
      department: this.department || undefined,
      designation: this.designation || undefined
    }).subscribe({
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
