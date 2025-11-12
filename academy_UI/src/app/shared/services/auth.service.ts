import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { map, catchError, switchMap } from 'rxjs/operators';
import { User, LoginCredentials, SignupData } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;
  private readonly STORAGE_KEY = 'currentUser';
  private readonly EMPLOYEE_ID_KEY = 'employeeId';
  private readonly apiUrl = 'http://127.0.0.1:8000/api';

  // Admin credentials
  private readonly ADMIN_EMAIL = 'admin@feuji.com';
  private readonly ADMIN_PASSWORD = 'admin1';

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
    // Check if admin login
    if (credentials.email === this.ADMIN_EMAIL && credentials.password === this.ADMIN_PASSWORD) {
      const adminUser: User = {
        id: 'admin-1',
        email: this.ADMIN_EMAIL,
        firstName: 'Admin',
        lastName: 'User',
        role: 'admin'
      };

      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(adminUser));
      this.currentUserSubject.next(adminUser);
      this.router.navigate(['/admin/dashboard']);
      
      return of(true);
    }

    // Otherwise, check if employee exists in backend
    return this.http.get<any>(`${this.apiUrl}/employees/get-all`).pipe(
      map(response => {
        if (response.success && response.data) {
          const employee = response.data.find((emp: any) => 
            emp.Employee_Email.toLowerCase() === credentials.email.toLowerCase()
          );

          if (employee) {
            // Extract first and last name from Employee_Name
            const nameParts = employee.Employee_Name.split(' ');
            const firstName = nameParts[0] || 'Employee';
            const lastName = nameParts.slice(1).join(' ') || '';

            const employeeUser: User = {
              id: employee.Employee_ID,
              email: employee.Employee_Email,
              firstName: firstName,
              lastName: lastName,
              role: 'employee',
              employeeId: employee.Employee_ID,
              designation: employee.Designation,
              department: 'Engineering' // Default department as backend doesn't provide it
            };

            // Store user data and employee ID
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(employeeUser));
            localStorage.setItem(this.EMPLOYEE_ID_KEY, employee.Employee_ID);
            this.currentUserSubject.next(employeeUser);
            
            this.router.navigate(['/employee/profile']);
            return true;
          } else {
            throw new Error('Invalid email or password');
          }
        } else {
          throw new Error('Unable to verify credentials');
        }
      }),
      catchError(error => {
        console.error('Login error:', error);
        return throwError(() => ({ message: 'Invalid email or password' }));
      })
    );
  }

  getEmployeeId(): string | null {
    return localStorage.getItem(this.EMPLOYEE_ID_KEY);
  }

  signup(signupData: SignupData & { password: string }): Observable<boolean> {
    // For now, signup is disabled as it requires backend integration
    // Return error asking users to contact admin
    return throwError(() => ({ 
      message: 'Please contact your administrator to create an account' 
    }));
  }

  logout(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    localStorage.removeItem(this.EMPLOYEE_ID_KEY);
    this.currentUserSubject.next(null);
    this.router.navigate(['/signin']);
  }

  getUserById(id: string): User | null {
    // In a real app, this would make an API call
    return this.currentUserValue?.id === id ? this.currentUserValue : null;
  }
}
