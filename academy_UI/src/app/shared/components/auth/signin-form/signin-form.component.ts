import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { LabelComponent } from '../../form/label/label.component';
import { CheckboxComponent } from '../../form/input/checkbox.component';
import { InputFieldComponent } from '../../form/input/input-field.component';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-signin-form',
  imports: [
    CommonModule,
    LabelComponent,
    CheckboxComponent,
    InputFieldComponent,
    RouterModule,
    FormsModule,
  ],
  templateUrl: './signin-form.component.html',
  styles: ``
})
export class SigninFormComponent implements OnInit {

  showPassword = false;
  isChecked = false;

  email = '';
  password = '';
  errorMessage = '';
  successMessage = '';
  isLoading = false;

  constructor(
    private authService: AuthService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['registered'] === 'true') {
        this.successMessage = 'Registration successful! Please login with your credentials.';
      }
    });
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSignIn() {
    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter both email and password';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login({ email: this.email, password: this.password })
      .subscribe({
        next: (success) => {
          this.isLoading = false;
          // Router navigation is handled by AuthService
        },
        error: (error) => {
          this.isLoading = false;
          this.errorMessage = error.message || 'Login failed. Please try again.';
        }
      });
  }
}
