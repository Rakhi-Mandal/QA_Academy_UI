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


export const routes: Routes = [
  {
    path:'',
    component:AppLayoutComponent,
    children:[
      // Default redirect
      {
        path: '',
        redirectTo: 'admin/track1',
        pathMatch: 'full'
      },
      
      // Admin Routes
      {
        path: 'admin/track1',
        component: FastrackComponent,
        title: 'Fastrack Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/track2',
        component: FastrackComponent,
        title: 'Advanced Track Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/track3',
        component: FastrackComponent,
        title: 'Mastery Program Batch | Admin Dashboard',
        data: { role: 'admin' }
      },
      {
        path: 'admin/calendar',
        component: CalendarComponent,
        title: 'Assessments & Certifications Calendar | Admin Dashboard',
        data: { role: 'admin' }
      },

      // Employee Routes
      {
        path: 'employee/profile',
        component: ProfileComponent,
        title: 'My Profile | Employee Dashboard',
        data: { role: 'employee' }
      },
      {
        path: 'employee/calendar',
        component: EmployeeCalendarComponent,
        title: 'My Assessments & Certifications | Employee Dashboard',
        data: { role: 'employee' }
      },

      // Legacy/Backward Compatible Routes (Redirect to Admin)
      {
        path: 'track1',
        redirectTo: 'admin/track1',
        pathMatch: 'full'
      },
      {
        path: 'track2',
        redirectTo: 'admin/track2',
        pathMatch: 'full'
      },
      {
        path: 'track3',
        redirectTo: 'admin/track3',
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
