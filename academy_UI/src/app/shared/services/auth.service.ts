// import { Injectable } from '@angular/core';
// import { Router } from '@angular/router';
// import { BehaviorSubject, Observable } from 'rxjs';
// import { HttpClient } from '@angular/common/http';
// import { map, catchError } from 'rxjs/operators';
// import { User, LoginCredentials, SignupData } from '../models/user.model';

// @Injectable({
//   providedIn: 'root'
// })
// export class AuthService {
//   private currentUserSubject: BehaviorSubject<User | null>;
//   public currentUser: Observable<User | null>;
//   private readonly STORAGE_KEY = 'currentUser';
//   private readonly API_URL = 'http://127.0.0.1:8000/api';

//   constructor(
//     private router: Router,
//     private http: HttpClient
//   ) {
//     const storedUser = localStorage.getItem(this.STORAGE_KEY);
//     this.currentUserSubject = new BehaviorSubject<User | null>(
//       storedUser ? JSON.parse(storedUser) : null
//     );
//     this.currentUser = this.currentUserSubject.asObservable();
//   }

//   public get currentUserValue(): User | null {
//     return this.currentUserSubject.value;
//   }

//   public get isAuthenticated(): boolean {
//     return this.currentUserSubject.value !== null;
//   }

//   public get isAdmin(): boolean {
//     return this.currentUserValue?.role === 'admin';
//   }

//   public get isEmployee(): boolean {
//     return this.currentUserValue?.role === 'employee';
//   }

//   login(credentials: LoginCredentials): Observable<boolean> {
//   return new Observable(observer => {
//     this.http.post<any>(`${this.API_URL}/users/login`, {
//       user_mail: credentials.email,
//       user_password: credentials.password
//     }).subscribe({
//       next: (response) => {
//         console.log('Login response:', response);

//         if (response.success && response.data) {
//           const user: User = {
//             id: response.data.user_id.toString(),       // user_id from user table
//             email: credentials.email, 
//             firstName: credentials.email.split('@')[0],
//             lastName: '',
//             role: response.data.user_role as 'admin' | 'employee',
//             employeeId: response.data.employee_id ?? ''  // employee_id from employee table
//           };

//           // Save in Local Storage
//           localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
//           this.currentUserSubject.next(user);

//           // Navigate based on role
//           if (user.role === 'admin') {
//             this.router.navigate(['/admin/dashboard']);
//           } else {
//             this.router.navigate(['/employee/profile']);
//           }

//           observer.next(true);
//           observer.complete();

//         } else {
//           observer.error({ message: response.message || 'Invalid email or password' });
//         }
//       },
//       error: (error) => {
//         console.error('Login error:', error);
//         observer.error({ message: 'Invalid email or password' });
//       }
//     });
//   });
// }


//   signup(signupData: SignupData & { password: string; podId?: number }): Observable<boolean> {
//     return new Observable(observer => {
//       // Prepare payload for backend API
//       const userPayload = {
//         user_mail: signupData.email,
//         user_password: signupData.password,
//         user_role: signupData.role,
//         employee_id: signupData.employeeId || null,
//         employee_name: `${signupData.firstName} ${signupData.lastName}`.trim(),
//         designation: signupData.designation || null,
//         pod_id: signupData.podId || null
//       };

//       console.log('Signup payload to backend:', userPayload);

//       // Call backend API to create user (and employee if role is employee)
//       this.http.post<any>(`${this.API_URL}/users/create`, userPayload).subscribe({
//         next: (response) => {
//           console.log('Backend registration response:', response);
          
//           if (response.success) {
//             // Registration successful
//             this.router.navigate(['/signin'], {
//               queryParams: { registered: 'true' }
//             });
//             observer.next(true);
//             observer.complete();
//           } else {
//             observer.error({ message: response.message || 'Registration failed' });
//           }
//         },
//         error: (error) => {
//           console.error('Registration error:', error);
          
//           // Check for duplicate email error
//           if (error.error && error.error.message) {
//             observer.error({ message: error.error.message });
//           } else if (error.status === 500 && error.error && error.error.detail) {
//             // Handle MySQL duplicate entry error
//             if (error.error.detail.includes('Duplicate entry')) {
//               observer.error({ message: 'This email is already registered. Please use a different email or login.' });
//             } else {
//               observer.error({ message: 'Registration failed. Please try again.' });
//             }
//           } else {
//             observer.error({ message: 'Registration failed. Please try again.' });
//           }
//         }
//       });
//     });
//   }

//   logout(): void {
//     localStorage.removeItem(this.STORAGE_KEY);
//     this.currentUserSubject.next(null);
//     this.router.navigate(['/signin']);
//   }

//   getUserById(id: string): User | null {
//     // In a real app, this would make an API call
//     return this.currentUserValue?.id === id ? this.currentUserValue : null;
//   }
// }
// ---------------------------------------------
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
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
      this.http.post<any>(`${this.API_URL}/users/login`, {
        user_mail: credentials.email,
        user_password: credentials.password
      }).subscribe({
        next: (response) => {
          console.log('Login response:', response);

          if (response.success && response.data) {
            // Create user object with ALL required fields
            const user: User = {
              id: response.data.user_id?.toString() || response.data.id?.toString() || '',
              email: credentials.email,
              firstName: response.data.employee_name?.split(' ')[0] || credentials.email.split('@')[0],
              lastName: response.data.employee_name?.split(' ').slice(1).join(' ') || '',
              role: response.data.user_role as 'admin' | 'employee',
              
              // IMPORTANT: Ensure employeeId is properly set
              // Try multiple possible field names from backend
              employeeId: response.data.employee_id 
                || response.data.Employee_ID 
                || response.data.employeeId
                || response.data.user_id?.toString()
                || response.data.id?.toString()
                || ''
            };

            console.log('Parsed user object:', user);

            // Validate that employeeId is set for employees
            if (user.role === 'employee' && !user.employeeId) {
              console.error('WARNING: Employee ID is missing from login response');
              // Fallback: use user_id as employeeId
              user.employeeId = user.id;
            }

            // Save to localStorage
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

  /**
   * Utility method to get employee ID with fallback logic
   */
  getEmployeeId(): string | null {
    const user = this.currentUserValue;
    if (!user) return null;

    // Try multiple possible field names
    return user.employeeId 
      || (user as any).employee_id 
      || (user as any).Employee_ID 
      || user.id 
      || null;
  }

  /**
   * Update current user's employeeId (useful for fixing missing IDs)
   */
  updateEmployeeId(employeeId: string): void {
    const user = this.currentUserValue;
    if (user) {
      const updatedUser = { ...user, employeeId };
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedUser));
      this.currentUserSubject.next(updatedUser);
      console.log('Updated employeeId:', employeeId);
    }
  }
}