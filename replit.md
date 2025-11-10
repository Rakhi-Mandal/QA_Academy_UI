# TailAdmin Angular Dashboard

## Overview
This project is a free and open-source Angular admin dashboard template, `TailAdmin Angular Dashboard`, built with Angular, TypeScript, and Tailwind CSS v4. It aims to provide a comprehensive set of UI components, elements, and ready-to-use pages for developing feature-rich back-end dashboards or admin panels. The project includes a complete role-based authentication system for both admin and employee users, offering distinct interfaces and navigation for each role.

## User Preferences
I want to prioritize iterative development. Please ask before making major architectural changes or introducing new libraries. I prefer clear, concise explanations and well-documented code. Ensure all new features are thoroughly tested and that existing functionalities are not regressed. Do not make changes to the `academy_Backend/` folder.

## System Architecture

### Technology Stack
- **Frontend Framework**: Angular 20+
- **Language**: TypeScript 5.8.3
- **Styling**: Tailwind CSS v4
- **Charting Libraries**: ApexCharts, AMCharts 5
- **UI Components**: Angular Material 20, FullCalendar
- **Build Tool**: Angular CLI with application builder

### UI/UX Decisions
- **Design System**: Tailwind CSS v4 for utility-first styling.
- **Color Schemes**: Custom color schemes for calendar items (blue for assignments, yellow for certifications).
- **Interactive Elements**: Hover effects, smooth transitions, and animations (fade-in, stagger, lift, scale) are used extensively for a modern and professional feel, especially in dashboard and calendar components.
- **Responsive Design**: CSS Grid-based layouts with breakpoints ensure responsiveness across devices.
- **Layout**: Dual-view architecture for Admin and Employee roles with distinct navigation menus.

### Technical Implementations
- **Authentication System**:
    - Complete role-based access control with `AuthService` for login, signup, logout, and session management.
    - `user.model.ts` defines admin/employee roles.
    - `auth.guard.ts` and `role.guard.ts` protect routes based on authentication status and user roles.
    - Session persistence via `localStorage` and reactive user state management using `BehaviorSubject`.
- **Role-Based Views and Navigation**:
    - Separate admin and employee dashboards and features.
    - Dynamic sidebar navigation (`app-sidebar/`) switches menu items based on the current route and user role.
    - Route prefixes (`/admin/*`, `/employee/*`) enforce clear separation.
- **Admin Dashboard**:
    - `admin-default-dashboard` component as the landing page for admin users.
    - Features stats cards, recent activity timeline, top performers leaderboard, and employee distribution chart (ApexCharts).
    - Quick actions panel for common admin tasks.
- **Calendar System**:
    - Dedicated `admin-calendar` and `employee-calendar` components.
    - `CalendarDataService` manages assessment and certification data.
    - Features include completion tracking, submission forms, dual-view (Timeline/Grid), advanced filtering, and rich animations.
    - Compact and modern card designs with hover effects.
- **Project Structure**: Organized into `src/app/pages`, `src/app/shared` (guards, layout, components, services, models), and `app.routes.ts`.

### Feature Specifications
- User login, signup with role selection, and logout.
- Protected routes for admin and employee roles.
- Dynamic sidebar navigation based on user role.
- Comprehensive admin dashboard with key metrics, activity feeds, and charts.
- Employee profile and a personal calendar for tracking assessments and certifications.
- Batch management (FastTrack, Advanced Track, Mastery Program) for admins.
- Full-featured assessment and certification tracking with submission workflows.
- 100+ UI elements, charts, form components.
- Dark mode support.
- Responsive design across all components.

## External Dependencies
- **Charting Libraries**:
    - ApexCharts
    - AMCharts 5
- **UI Components**:
    - Angular Material 20
    - FullCalendar
- **HTTP Server**:
    - http-server (for static file serving in deployment)