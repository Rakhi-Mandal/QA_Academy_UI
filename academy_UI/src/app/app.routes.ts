import { Routes } from '@angular/router';
import { ProfileComponent } from './pages/profile/profile.component';
import { FormElementsComponent } from './pages/forms/form-elements/form-elements.component';
import { AppLayoutComponent } from './shared/layout/app-layout/app-layout.component';
import { LineChartComponent } from './pages/charts/line-chart/line-chart.component';
import { BarChartComponent } from './pages/charts/bar-chart/bar-chart.component';
import { AlertsComponent } from './pages/ui-elements/alerts/alerts.component';
import { SignInComponent } from './pages/auth-pages/sign-in/sign-in.component';
import { SignUpComponent } from './pages/auth-pages/sign-up/sign-up.component';
import { FastrackComponent } from './pages/dashboard/fastrack/fastrack.component';
import { CalendarComponent } from './pages/calendar/calendar.component';
import { EmployeeCalendarComponent } from './pages/employee-calendar/employee-calendar.component';
import { AdminDefaultDashboardComponent } from './pages/admin-default-dashboard/admin-default-dashboard.component';
import { authGuard } from './shared/guards/auth.guard';
import { adminGuard, employeeGuard } from './shared/guards/role.guard';
import { AdvancedTrackComponent } from './pages/dashboard/advanced-track/advanced-track.component';
import { MasteryProgramComponent } from './pages/dashboard/mastery-program/mastery-program.component';


export const routes: Routes = [
  {
    path:'',
    component:AppLayoutComponent,
    canActivate: [authGuard],
    children:[
      // Default redirect
      {
        path: '',
        redirectTo: 'admin/dashboard',
        pathMatch: 'full'
      },
      
      // Admin Routes
      {
        path: 'admin/dashboard',
        component: AdminDefaultDashboardComponent,
        canActivate: [adminGuard],
        title: 'Dashboard Overview | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/track1',
        component: FastrackComponent,
        canActivate: [adminGuard],
        title: 'Fastrack Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/track2',
        component: AdvancedTrackComponent,
        canActivate: [adminGuard],
        title: 'Advanced Track Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/track3',
        component: MasteryProgramComponent,
        canActivate: [adminGuard],
        title: 'Mastery Program Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/calendar',
        component: CalendarComponent,
        canActivate: [adminGuard],
        title: 'Assessments & Certifications Calendar | Admin Dashboard',
        data: { role: 'admin' }
      },

      // Employee Routes
      {
        path: 'employee/profile',
        component: ProfileComponent,
        canActivate: [employeeGuard],
        title: 'My Profile | Employee Dashboard',
        data: { role: 'employee' }
      },
      {
        path: 'employee/calendar',
        component: EmployeeCalendarComponent,
        canActivate: [employeeGuard],
        title: 'My Assessments & Certifications | Employee Dashboard',
        data: { role: 'employee' }
      },
      {
        path: 'track3',
         component: EmployeeCalendarComponent,
        pathMatch: 'full'
      },
      {
        path: 'calendar',
        redirectTo: 'admin/calendar',
        pathMatch: 'full'
      },
      {
        path: 'profile',
        redirectTo: 'employee/profile',
        pathMatch: 'full'
      },

      // Other Routes
      {
        path:'form-elements',
        component:FormElementsComponent,
        title:'Angular Form Elements Dashboard | TailAdmin'
      },
      {
        path:'line-chart',
        component:LineChartComponent,
        title:'Angular Line Chart Dashboard | TailAdmin'
      },
      {
        path:'bar-chart',
        component:BarChartComponent,
        title:'Angular Bar Chart Dashboard | TailAdmin'
      },
      {
        path:'alerts',
        component:AlertsComponent,
        title:'Angular Alerts Dashboard | TailAdmin'
      },
      
    ]
  },
  // Auth Pages
  {
    path:'signin',
    component:SignInComponent,
    title:'Sign In | TailAdmin'
  },
  {
    path:'signup',
    component:SignUpComponent,
    title:'Sign Up | TailAdmin'
  }
];
