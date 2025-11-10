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
  private readonly USERS_KEY = 'registeredUsers';

  constructor(private router: Router) {
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
    return new Observable(observer => {
      setTimeout(() => {
        const users = this.getAllUsers();
        
        if (users.find(u => u.email === signupData.email)) {
          observer.error({ message: 'Email already registered' });
          return;
        }

        const newUser: User & { password: string } = {
          id: Date.now().toString(),
          email: signupData.email,
          firstName: signupData.firstName,
          lastName: signupData.lastName,
          role: signupData.role,
          employeeId: signupData.employeeId,
          department: signupData.department,
          designation: signupData.designation,
          password: signupData.password
        };

        this.saveUser(newUser);

        const { password, ...userWithoutPassword } = newUser;
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(userWithoutPassword));
        this.currentUserSubject.next(userWithoutPassword);

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
