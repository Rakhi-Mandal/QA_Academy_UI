import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { User, LoginCredentials, SignupData } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;
  private readonly STORAGE_KEY = 'currentUser';

  constructor(private router: Router) {
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
      // Simulate API call - Replace with actual HTTP call
      setTimeout(() => {
        // Demo users for testing
        const demoUsers: User[] = [
          {
            id: '1',
            email: 'admin@academy.com',
            firstName: 'Admin',
            lastName: 'User',
            role: 'admin'
          },
          {
            id: '2',
            email: 'employee@academy.com',
            firstName: 'John',
            lastName: 'Doe',
            role: 'employee',
            employeeId: 'EMP001',
            department: 'Engineering',
            designation: 'QA Engineer',
            manager: 'Sarah Wilson'
          }
        ];

        const user = demoUsers.find(u => u.email === credentials.email);

        if (user && credentials.password === 'password123') {
          // Store user in localStorage
          localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
          this.currentUserSubject.next(user);

          // Redirect based on role
          if (user.role === 'admin') {
            this.router.navigate(['/admin/dashboard']);
          } else {
            this.router.navigate(['/employee/profile']);
          }

          observer.next(true);
          observer.complete();
        } else {
          observer.error({ message: 'Invalid email or password' });
        }
      }, 500);
    });
  }

  signup(signupData: SignupData): Observable<boolean> {
    return new Observable(observer => {
      // Simulate API call - Replace with actual HTTP call
      setTimeout(() => {
        const newUser: User = {
          id: Date.now().toString(),
          email: signupData.email,
          firstName: signupData.firstName,
          lastName: signupData.lastName,
          role: signupData.role,
          employeeId: signupData.employeeId,
          department: signupData.department,
          designation: signupData.designation
        };

        // Store user in localStorage
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(newUser));
        this.currentUserSubject.next(newUser);

        // Redirect based on role
        if (newUser.role === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        } else {
          this.router.navigate(['/employee/profile']);
        }

        observer.next(true);
        observer.complete();
      }, 500);
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
