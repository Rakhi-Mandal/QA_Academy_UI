import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { map, catchError } from 'rxjs/operators';
import { User, LoginCredentials, SignupData } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;
  private readonly STORAGE_KEY = 'currentUser';
  private readonly API_URL = 'http://127.0.0.1:8000/api';

  constructor(
    private router: Router,
    private http: HttpClient
  ) {
    const storedUser = localStorage.getItem(this.STORAGE_KEY);
    this.currentUserSubject = new BehaviorSubject<User | null>(
      storedUser ? JSON.parse(storedUser) : null
    );
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  public get isAuthenticated(): boolean {
    return this.currentUserSubject.value !== null;
  }

  public get isAdmin(): boolean {
    return this.currentUserValue?.role === 'admin';
  }

  public get isEmployee(): boolean {
    return this.currentUserValue?.role === 'employee';
  }

  login(credentials: LoginCredentials): Observable<boolean> {
    return new Observable(observer => {
      // Call backend API to validate login
      this.http.post<any>(`${this.API_URL}/users/login`, {
        user_mail: credentials.email,
        user_password: credentials.password
      }).subscribe({
        next: (response) => {
          console.log('Login response:', response);
          
          if (response.success && response.data) {
            // Get user details from backend
            this.http.get<any>(`${this.API_URL}/users/${response.data.user_id || ''}`)
              .subscribe({
                next: (userResponse) => {
                  if (userResponse.success && userResponse.data) {
                    const user: User = {
                      id: userResponse.data.user_id?.toString() || '',
                      email: userResponse.data.user_mail || credentials.email,
                      firstName: credentials.email.split('@')[0], // Extract from email
                      lastName: '',
                      role: response.data.user_role as 'admin' | 'employee'
                    };

                    // Store current session in localStorage
                    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
                    this.currentUserSubject.next(user);

                    // Navigate based on role
                    if (user.role === 'admin') {
                      this.router.navigate(['/admin/dashboard']);
                    } else {
                      this.router.navigate(['/employee/profile']);
                    }

                    observer.next(true);
                    observer.complete();
                  } else {
                    observer.error({ message: 'Unable to fetch user details' });
                  }
                },
                error: (error) => {
                  // Fallback: Just use role from login response
                  const user: User = {
                    id: Date.now().toString(),
                    email: credentials.email,
                    firstName: credentials.email.split('@')[0],
                    lastName: '',
                    role: response.data.user_role as 'admin' | 'employee'
                  };

                  localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
                  this.currentUserSubject.next(user);

                  if (user.role === 'admin') {
                    this.router.navigate(['/admin/dashboard']);
                  } else {
                    this.router.navigate(['/employee/profile']);
                  }

                  observer.next(true);
                  observer.complete();
                }
              });
          } else {
            observer.error({ message: response.message || 'Invalid email or password' });
          }
        },
        error: (error) => {
          console.error('Login error:', error);
          observer.error({ message: 'Invalid email or password' });
        }
      });
    });
  }

  signup(signupData: SignupData & { password: string; podId?: number }): Observable<boolean> {
    return new Observable(observer => {
      // Prepare payload for backend API
      const userPayload = {
        user_mail: signupData.email,
        user_password: signupData.password,
        user_role: signupData.role,
        employee_id: signupData.employeeId || null,
        employee_name: `${signupData.firstName} ${signupData.lastName}`.trim(),
        designation: signupData.designation || null,
        pod_id: signupData.podId || null
      };

      console.log('Signup payload to backend:', userPayload);

      // Call backend API to create user (and employee if role is employee)
      this.http.post<any>(`${this.API_URL}/users/create`, userPayload).subscribe({
        next: (response) => {
          console.log('Backend registration response:', response);
          
          if (response.success) {
            // Registration successful
            this.router.navigate(['/signin'], {
              queryParams: { registered: 'true' }
            });
            observer.next(true);
            observer.complete();
          } else {
            observer.error({ message: response.message || 'Registration failed' });
          }
        },
        error: (error) => {
          console.error('Registration error:', error);
          
          // Check for duplicate email error
          if (error.error && error.error.message) {
            observer.error({ message: error.error.message });
          } else if (error.status === 500 && error.error && error.error.detail) {
            // Handle MySQL duplicate entry error
            if (error.error.detail.includes('Duplicate entry')) {
              observer.error({ message: 'This email is already registered. Please use a different email or login.' });
            } else {
              observer.error({ message: 'Registration failed. Please try again.' });
            }
          } else {
            observer.error({ message: 'Registration failed. Please try again.' });
          }
        }
      });
    });
  }

  logout(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    this.currentUserSubject.next(null);
    this.router.navigate(['/signin']);
  }

  getUserById(id: string): User | null {
    // In a real app, this would make an API call
    return this.currentUserValue?.id === id ? this.currentUserValue : null;
  }
}
