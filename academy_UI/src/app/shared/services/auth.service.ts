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
  private readonly USERS_KEY = 'registeredUsers';
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
    
    this.initializeDemoUsers();
  }

  private initializeDemoUsers(): void {
    const existingUsers = this.getAllUsers();
    if (existingUsers.length === 0) {
      const demoUsers: Array<User & { password: string }> = [
        {
          id: '1',
          email: 'admin@academy.com',
          firstName: 'Admin',
          lastName: 'User',
          role: 'admin',
          password: 'password123'
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
          manager: 'Sarah Wilson',
          password: 'password123'
        }
      ];
      localStorage.setItem(this.USERS_KEY, JSON.stringify(demoUsers));
    }
  }

  private getAllUsers(): Array<User & { password: string }> {
    const usersJson = localStorage.getItem(this.USERS_KEY);
    return usersJson ? JSON.parse(usersJson) : [];
  }

  private saveUser(user: User & { password: string }): void {
    const users = this.getAllUsers();
    const existingIndex = users.findIndex(u => u.email === user.email);
    
    if (existingIndex >= 0) {
      users[existingIndex] = user;
    } else {
      users.push(user);
    }
    
    localStorage.setItem(this.USERS_KEY, JSON.stringify(users));
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
      setTimeout(() => {
        const users = this.getAllUsers();
        const user = users.find(u => u.email === credentials.email);

        if (user && user.password === credentials.password) {
          const { password, ...userWithoutPassword } = user;
          
          localStorage.setItem(this.STORAGE_KEY, JSON.stringify(userWithoutPassword));
          this.currentUserSubject.next(userWithoutPassword);

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

  signup(signupData: SignupData & { password: string }): Observable<boolean> {
    const payload = {
      email: signupData.email,
      password: signupData.password,
      first_name: signupData.firstName,
      last_name: signupData.lastName,
      role: signupData.role,
      employee_id: signupData.employeeId || null,
      department: signupData.department || null,
      designation: signupData.designation || null
    };

    return this.http.post<any>(`${this.API_URL}/users/create`, payload).pipe(
      map(response => {
        if (response.success) {
          const newUser: User = {
            id: response.data.id || Date.now().toString(),
            email: response.data.email,
            firstName: response.data.first_name,
            lastName: response.data.last_name,
            role: response.data.role,
            employeeId: response.data.employee_id,
            department: response.data.department,
            designation: response.data.designation
          };

          localStorage.setItem(this.STORAGE_KEY, JSON.stringify(newUser));
          this.currentUserSubject.next(newUser);

          if (newUser.role === 'admin') {
            this.router.navigate(['/admin/dashboard']);
          } else {
            this.router.navigate(['/employee/profile']);
          }

          return true;
        } else {
          throw new Error(response.message || 'Registration failed');
        }
      }),
      catchError(error => {
        const errorMessage = error.error?.message || error.message || 'Registration failed. Please try again.';
        throw { message: errorMessage };
      })
    );
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
